from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q, Count
from ..models import Scholarship, Application

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('home')

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'all')
    status_filter = request.GET.get('status', 'all')

    apps = Application.objects.select_related(
        'student', 'scholarship', 'student__user'
    ).prefetch_related('documents').order_by('-submitted_at')

    if q:
        apps = apps.filter(
            Q(student__full_name__icontains=q) |
            Q(student__student_id__icontains=q) |
            Q(scholarship__title__icontains=q) |
            Q(student__major__icontains=q)
        )

    if category and category != 'all':
        apps = apps.filter(scholarship__category=category)

    if status_filter and status_filter != 'all':
        apps = apps.filter(status=status_filter)

    total_scholarships = Scholarship.objects.count()
    total_applications = Application.objects.count()
    pending_applications = Application.objects.filter(status='pending').count()
    approved_applications = Application.objects.filter(status='approved').count()
    rejected_applications = Application.objects.filter(status='rejected').count()

    cat_counts = {
        'all': Application.objects.count(),
        'general': Application.objects.filter(scholarship__category='general').count(),
        'exchange': Application.objects.filter(scholarship__category='exchange').count(),
        'fee_waiver': Application.objects.filter(scholarship__category='fee_waiver').count(),
        'lunch': Application.objects.filter(scholarship__category='lunch').count(),
    }

    all_scholarships = Scholarship.objects.annotate(
        apps_count=Count('applications')
    ).order_by('-id')

    active_scholarships = [s for s in all_scholarships if not s.is_expired]
    expired_scholarships = [s for s in all_scholarships if s.is_expired]

    sch_cat_counts = {
        'all': len(active_scholarships),
        'general': len([s for s in active_scholarships if s.category == 'general']),
        'exchange': len([s for s in active_scholarships if s.category == 'exchange']),
        'fee_waiver': len([s for s in active_scholarships if s.category == 'fee_waiver']),
        'lunch': len([s for s in active_scholarships if s.category == 'lunch']),
    }

    context = {
        'total_scholarships': total_scholarships,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'applications': apps,
        'scholarships_list': active_scholarships,
        'expired_scholarships': expired_scholarships,
        'q': q,
        'selected_category': category,
        'selected_status': status_filter,
        'cat_counts': cat_counts,
        'sch_cat_counts': sch_cat_counts,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
def update_application(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('home')
    app = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        status_changed = False
        
        # Only update status if provided and not explicitly told to keep current
        if new_status and new_status not in ('keep', 'current', ''):
            if app.status != new_status:
                app.status = new_status
                status_changed = True
        
        # Save note / remarks if provided
        custom_note = request.POST.get('note', '').strip()
        if custom_note:
            app.note = custom_note
        app.save()
        
        # Check if email notification was requested
        # 'send_email' can be 'true', '1', 'on'
        send_email_raw = request.POST.get('send_email', 'true')
        send_email = send_email_raw in ('true', '1', 'on', True)
        
        custom_subject = request.POST.get('email_subject', '').strip()
        custom_message = request.POST.get('email_message', '').strip()
        is_notice = request.POST.get('is_notice') == 'true' or not status_changed
        
        email_sent = False
        email_error = None
        
        if send_email and (custom_message or app.status in ('interview', 'approved', 'rejected')):
            from scholarships.emails import send_status_update_email
            try:
                send_status_update_email(
                    app, 
                    custom_subject=custom_subject, 
                    custom_message=custom_message,
                    is_notice=is_notice
                )
                email_sent = True
            except Exception as e:
                email_error = str(e)
                print(f"Failed to send email to {app.student.user.email}: {e}")
                
        # Check if AJAX / JSON request
        if request.headers.get('Accept') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({
                'success': True, 
                'status': app.status, 
                'status_display': app.get_status_display(),
                'status_changed': status_changed,
                'email_sent': email_sent,
                'email_error': email_error,
                'note': app.note,
            })
            
        if email_sent:
            msg = f'ส่งอีเมลแจ้งนักศึกษาเรียบร้อยแล้ว' if not status_changed else f'อัพเดทสถานะเป็น {app.get_status_display()} และส่งอีเมลแจ้งนักศึกษาเรียบร้อยแล้ว'
            messages.success(request, msg)
        elif send_email and email_error:
            messages.warning(request, f'บันทึกข้อมูลสำเร็จ (แต่ไม่สามารถส่งอีเมลได้: {email_error})')
        else:
            messages.success(request, f'อัพเดทข้อมูลเรียบร้อยแล้ว')
            
    return redirect('admin_dashboard')

@staff_member_required
def scholarship_dashboard(request):
    now = timezone.now().date()
    
    # Get filters
    filter_year = request.GET.get('year', str(now.year))
    filter_month = request.GET.get('month', '')
    filter_term = request.GET.get('term', '')

    thai_year = int(filter_year) + 543 if filter_year.isdigit() else now.year + 543

    # Base QuerySets
    s_qs = Scholarship.objects.all()
    a_qs = Application.objects.all()

    # Apply Year Filter
    if filter_year.isdigit():
        s_qs = s_qs.filter(created_at__year=filter_year)
        a_qs = a_qs.filter(submitted_at__year=filter_year)

    # Apply Month Filter
    if filter_month.isdigit():
        s_qs = s_qs.filter(created_at__month=filter_month)
        a_qs = a_qs.filter(submitted_at__month=filter_month)

    # Apply Term Filter (Term 1: 8-12, Term 2: 1-5, Summer: 6-7)
    if filter_term == '1':
        s_qs = s_qs.filter(created_at__month__in=[8, 9, 10, 11, 12])
        a_qs = a_qs.filter(submitted_at__month__in=[8, 9, 10, 11, 12])
    elif filter_term == '2':
        s_qs = s_qs.filter(created_at__month__in=[1, 2, 3, 4, 5])
        a_qs = a_qs.filter(submitted_at__month__in=[1, 2, 3, 4, 5])
    elif filter_term == '3':
        s_qs = s_qs.filter(created_at__month__in=[6, 7])
        a_qs = a_qs.filter(submitted_at__month__in=[6, 7])

    total_scholarships = s_qs.count()
    total_value = s_qs.aggregate(
        total=Sum('amount_per_semester')
    )['total'] or 0
    open_scholarships = s_qs.filter(
        status='active', end_date__gte=now
    ).count()

    total_applications    = a_qs.count()
    pending_applications  = a_qs.filter(status='pending').count()
    approved_applications = a_qs.filter(status='approved').count()
    rejected_applications = a_qs.filter(status='rejected').count()

    general_count  = s_qs.filter(category='general').count()
    exchange_count = s_qs.filter(category='exchange').count()
    waiver_count   = s_qs.filter(category='fee_waiver').count()
    lunch_count    = s_qs.filter(category='lunch').count()

    recent_scholarships = s_qs.order_by('-id')[:5]

    deadline_soon = Scholarship.objects.filter(
        status='active',
        end_date__gte=now
    ).order_by('end_date')[:5]

    context = {
        'thai_year':             thai_year,
        'total_scholarships':    total_scholarships,
        'total_value':           total_value,
        'open_scholarships':     open_scholarships,
        'total_applications':    total_applications,
        'pending_applications':  pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'general_count':         general_count,
        'exchange_count':        exchange_count,
        'waiver_count':          waiver_count,
        'lunch_count':           lunch_count,
        'recent_scholarships':   recent_scholarships,
        'deadline_soon':         deadline_soon,
        'today':                 now,
        'filter_year':           filter_year,
        'filter_month':          filter_month,
        'filter_term':           filter_term,
    }
    return render(request, 'scholarship_dashboard.html', context)

@staff_member_required
def delete_scholarship(request, pk):
    if request.method == 'POST':
        scholarship = get_object_or_404(Scholarship, pk=pk)
        title = scholarship.title
        scholarship.delete()
        messages.success(request, f'ลบทุนการศึกษา "{title}" เรียบร้อยแล้ว')
    return redirect('scholarships')
