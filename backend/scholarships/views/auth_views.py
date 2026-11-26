import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from ..models import StudentProfile, Application

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest' or self.request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'success': True,
                'redirect_url': self.get_success_url()
            })
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest' or self.request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'success': False,
                'message': _('Invalid username or password. Please check and try again.')
            }, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url and next_url != '/':
            return next_url
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return '/admin-dashboard/'
        return '/'

@login_required
def auth_redirect(request):
    """
    Redirects user to the correct dashboard based on their role:
    - Staff / Superuser -> /admin-dashboard/
    - Regular Student   -> / (home)
    """
    next_url = request.GET.get('next')
    if next_url and next_url != '/':
        return redirect(next_url)
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('home')

@login_required
def profile(request):
    try:
        student_profile = request.user.profile
    except Exception:
        fallback_id = request.user.username
        if StudentProfile.objects.filter(student_id=fallback_id).exists():
            fallback_id = f"{request.user.username}_{request.user.id}"
        student_profile, _created = StudentProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'student_id': fallback_id,
                'full_name': request.user.get_full_name() or request.user.username,
                'faculty': 'computing',
                'major': '',
                'gpax': 0.0,
            }
        )

    if request.method == 'POST':
        try:
            full_name = request.POST.get('full_name', '').strip()
            student_id = request.POST.get('student_id', '').strip()
            faculty = request.POST.get('faculty', '').strip()
            major = request.POST.get('major', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
            gpax_raw = request.POST.get('gpax', '').strip()
            profile_image = request.FILES.get('profile_image')

            # Fallback student_id if empty
            if not student_id:
                student_id = student_profile.student_id if (student_profile and student_profile.student_id) else request.user.username

            # Parse GPAX safely (range 0.00 - 4.00)
            try:
                gpax = float(gpax_raw) if gpax_raw else (student_profile.gpax if student_profile else 0.0)
                gpax = max(0.0, min(4.0, round(gpax, 2)))
            except (ValueError, TypeError):
                gpax = student_profile.gpax if student_profile else 0.0

            # Prevent student_id duplicate conflict with other users
            conflict = StudentProfile.objects.filter(student_id=student_id).exclude(user=request.user).first()
            if conflict:
                messages.error(request, _('This Student ID (%(sid)s) is already in use by another account.') % {'sid': student_id})
                return redirect('profile')

            if student_profile:
                student_profile.full_name = full_name or student_profile.full_name or request.user.username
                student_profile.student_id = student_id
                student_profile.faculty = faculty or student_profile.faculty or 'computing'
                student_profile.major = major
                student_profile.phone_number = phone_number
                student_profile.gpax = gpax
                if profile_image:
                    student_profile.profile_image = profile_image
                student_profile.save()
            else:
                student_profile = StudentProfile.objects.create(
                    user=request.user,
                    full_name=full_name or request.user.get_full_name() or request.user.username,
                    student_id=student_id,
                    faculty=faculty or 'computing',
                    major=major,
                    phone_number=phone_number,
                    gpax=gpax,
                    profile_image=profile_image if profile_image else None,
                )

            # Sync User first/last name safely via QuerySet update
            if full_name:
                parts = full_name.split(' ', 1)
                User.objects.filter(pk=request.user.pk).update(
                    first_name=parts[0],
                    last_name=parts[1] if len(parts) > 1 else ''
                )

            messages.success(request, _('Profile updated successfully!'))
        except Exception as e:
            logger.error("Failed to update profile for %s: %s", request.user.username, e, exc_info=True)
            messages.error(request, _('Could not save profile: %(err)s') % {'err': str(e)})

        return redirect('profile')

    app_list = []
    status_counts = {
        'all': 0,
        'pending': 0,
        'in_progress': 0,
        'approved': 0,
        'completed': 0,
        'rejected': 0,
        'cancelled': 0,
    }
    selected_status = request.GET.get('status', 'all').strip().lower()
    page_obj = None
    page_range = None
    extra_query = ''

    if student_profile:
        all_apps = Application.objects.filter(
            student=student_profile
        ).select_related('scholarship').order_by('-submitted_at')

        total_count = all_apps.count()
        agg_counts = all_apps.aggregate(
            pending=Count('id', filter=Q(status='pending')),
            in_progress=Count('id', filter=Q(status__in=['in_progress', 'interview'])),
            approved=Count('id', filter=Q(status='approved')),
            completed=Count('id', filter=Q(status='completed')),
            rejected=Count('id', filter=Q(status='rejected')),
            cancelled=Count('id', filter=Q(status='cancelled')),
        )
        status_counts = {
            'all': total_count,
            'pending': agg_counts['pending'] or 0,
            'in_progress': agg_counts['in_progress'] or 0,
            'approved': agg_counts['approved'] or 0,
            'completed': agg_counts['completed'] or 0,
            'rejected': agg_counts['rejected'] or 0,
            'cancelled': agg_counts['cancelled'] or 0,
        }

        # Filter by selected status
        filtered_apps = all_apps
        if selected_status and selected_status != 'all':
            if selected_status == 'in_progress':
                filtered_apps = all_apps.filter(status__in=['in_progress', 'interview'])
            elif selected_status in ['pending', 'approved', 'completed', 'rejected', 'cancelled']:
                filtered_apps = all_apps.filter(status=selected_status)
            else:
                selected_status = 'all'

        if selected_status != 'all':
            extra_query = f"status={selected_status}"

        # Pagination: 10 applications per page
        paginator = Paginator(filtered_apps, 10)
        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)
        app_list = page_obj

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1':
        return render(request, 'accounts/partials/history_list.html', {
            'student_profile': student_profile,
            'applications': app_list,
            'page_obj': page_obj,
            'page_range': page_range,
            'status_counts': status_counts,
            'selected_status': selected_status,
            'extra_query': extra_query,
        })

    return render(request, 'accounts/profile.html', {
        'student_profile': student_profile,
        'applications': app_list,
        'page_obj': page_obj,
        'page_range': page_range,
        'status_counts': status_counts,
        'selected_status': selected_status,
        'extra_query': extra_query,
    })

