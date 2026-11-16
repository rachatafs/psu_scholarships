from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Scholarship, Application

def _get_standard_page_range(current_page, num_pages):
    """
    Standard compact pagination (elided):
    - Shows all pages if num_pages <= 5.
    - If num_pages > 5, shows 1 2 3 4 … [last] near start,
      and sliding window with ellipsis in middle/end.
    """
    if num_pages <= 5:
        return list(range(1, num_pages + 1))
    if current_page <= 3:
        return [1, 2, 3, 4, '…', num_pages]
    elif current_page >= num_pages - 2:
        return [1, '…', num_pages - 3, num_pages - 2, num_pages - 1, num_pages]
    else:
        return [1, '…', current_page - 1, current_page, current_page + 1, '…', num_pages]

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('home')

    apps = Application.objects.select_related(
        'student', 'scholarship', 'student__user'
    ).prefetch_related('documents').order_by('-submitted_at')

    total_scholarships = Scholarship.objects.count()
    total_applications = apps.count()
    pending_applications = Application.objects.filter(status='pending').count()
    in_progress_applications = Application.objects.filter(status__in=['in_progress', 'interview']).count()
    approved_applications = Application.objects.filter(status='approved').count()
    rejected_applications = Application.objects.filter(status='rejected').count()
    completed_applications = Application.objects.filter(status='completed').count()
    cancelled_applications = Application.objects.filter(status='cancelled').count()

    cat_counts = {
        'all': total_applications,
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
        'in_progress_applications': in_progress_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'completed_applications': completed_applications,
        'cancelled_applications': cancelled_applications,
        'applications': apps,
        'filtered_apps_count': total_applications,
        'scholarships_list': active_scholarships,
        'expired_scholarships': expired_scholarships,
        'expired_scholarships_count': len(expired_scholarships),
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
        
        if send_email and (custom_message or app.status in ('interview', 'in_progress', 'approved', 'rejected', 'completed', 'cancelled')):
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
            msg = _('Notification email sent to student successfully.') if not status_changed else _('Status updated to %(status)s and notification email sent.') % {'status': app.get_status_display()}
            messages.success(request, msg)
        elif send_email and email_error:
            messages.warning(request, _('Saved successfully (Email error: %(error)s)') % {'error': email_error})
        else:
            messages.success(request, _('Updated successfully.'))
            
    return redirect('admin_dashboard')

def _get_dashboard_analytics_data(request):
    now = timezone.now().date()

    # Scope & Filter flags
    scope = request.GET.get('scope', '').strip()
    is_all_scope = (scope == 'all' or request.GET.get('all') == '1')

    filter_term = '' if is_all_scope else request.GET.get('term', '').strip()
    filter_month = '' if is_all_scope else request.GET.get('month', '').strip()

    raw_year = request.GET.get('year')
    if is_all_scope:
        filter_year = 'all'
    elif raw_year is not None:
        filter_year = raw_year.strip()
    else:
        filter_year = str(now.year)

    # Base QuerySets
    s_qs = Scholarship.objects.all()

    # Apply Year Filter
    if filter_year.isdigit():
        s_qs = s_qs.filter(created_at__year=filter_year)
        thai_year = int(filter_year) + 543
    else:
        filter_year = 'all'
        thai_year = now.year + 543

    # Apply Month Filter
    if filter_month.isdigit():
        s_qs = s_qs.filter(created_at__month=filter_month)

    # Apply Term Filter (Term 1: 8-12, Term 2: 1-5, Summer: 6-7)
    if filter_term == '1':
        s_qs = s_qs.filter(created_at__month__in=[8, 9, 10, 11, 12])
    elif filter_term == '2':
        s_qs = s_qs.filter(created_at__month__in=[1, 2, 3, 4, 5])
    elif filter_term == '3':
        s_qs = s_qs.filter(created_at__month__in=[6, 7])

    filtered_scholarships = s_qs.order_by('-created_at')

    # Filter applications for the filtered scholarships (includes student profile info)
    a_qs = Application.objects.filter(scholarship__in=s_qs).select_related(
        'student', 'scholarship', 'student__user'
    ).order_by('-submitted_at')
    filtered_applications = a_qs

    total_scholarships = s_qs.count()
    total_value = s_qs.aggregate(
        total=Sum('amount_per_semester')
    )['total'] or 0
    open_scholarships = s_qs.filter(
        status='active', end_date__gte=now
    ).count()

    total_applications = a_qs.count()
    pending_applications = a_qs.filter(status='pending').count()
    in_progress_applications = a_qs.filter(status__in=['in_progress', 'interview']).count()
    approved_applications = a_qs.filter(status='approved').count()
    rejected_applications = a_qs.filter(status='rejected').count()
    completed_applications = a_qs.filter(status='completed').count()
    cancelled_applications = a_qs.filter(status='cancelled').count()

    general_count = s_qs.filter(category='general').count()
    exchange_count = s_qs.filter(category='exchange').count()
    waiver_count = s_qs.filter(category='fee_waiver').count()
    lunch_count = s_qs.filter(category='lunch').count()

    month_names = {
        '1': _('January'), '2': _('February'), '3': _('March'), '4': _('April'),
        '5': _('May'), '6': _('June'), '7': _('July'), '8': _('August'),
        '9': _('September'), '10': _('October'), '11': _('November'), '12': _('December')
    }
    filter_month_name = month_names.get(filter_month, '')

    term_names = {
        '1': _('Semester 1 (Aug-Dec)'),
        '2': _('Semester 2 (Jan-May)'),
        '3': _('Summer (Jun-Jul)'),
    }
    filter_term_name = term_names.get(filter_term, '')

    has_active_filter = bool(filter_term or filter_month or (filter_year and filter_year != str(now.year)))

    deadline_soon = Scholarship.objects.filter(
        status='active',
        end_date__gte=now
    ).order_by('end_date')[:5]

    return {
        'thai_year': thai_year,
        'total_scholarships': total_scholarships,
        'total_value': total_value,
        'open_scholarships': open_scholarships,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'in_progress_applications': in_progress_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'completed_applications': completed_applications,
        'cancelled_applications': cancelled_applications,
        'general_count': general_count,
        'exchange_count': exchange_count,
        'waiver_count': waiver_count,
        'lunch_count': lunch_count,
        'filtered_scholarships': filtered_scholarships,
        'filtered_applications': filtered_applications,
        'deadline_soon': deadline_soon,
        'today': now,
        'filter_year': filter_year,
        'filter_month': filter_month,
        'filter_month_name': filter_month_name,
        'filter_term': filter_term,
        'filter_term_name': filter_term_name,
        'has_active_filter': has_active_filter,
        'is_all_scope': is_all_scope or (filter_year == 'all' and not filter_term and not filter_month),
    }

@staff_member_required
def scholarship_dashboard(request):
    data = _get_dashboard_analytics_data(request)

    active_tab = request.GET.get('tab', 'overview')
    active_subtab = request.GET.get('subtab', 'sch')

    if 'page_sch' in request.GET and 'page_app' not in request.GET:
        active_tab = 'records'
        active_subtab = 'sch'
    elif 'page_app' in request.GET and 'page_sch' not in request.GET:
        active_tab = 'records'
        active_subtab = 'apps'
    elif 'page_sch' in request.GET or 'page_app' in request.GET:
        active_tab = 'records'
        if 'subtab' in request.GET:
            active_subtab = request.GET.get('subtab')
        elif 'page_sch' in request.GET:
            active_subtab = 'sch'
        elif 'page_app' in request.GET:
            active_subtab = 'apps'

    # Paginate Scholarships (10 per page)
    sch_paginator = Paginator(data['filtered_scholarships'], 10)
    page_sch = request.GET.get('page_sch', 1)
    try:
        sch_page = sch_paginator.page(page_sch)
    except PageNotAnInteger:
        sch_page = sch_paginator.page(1)
    except EmptyPage:
        sch_page = sch_paginator.page(sch_paginator.num_pages)

    # Paginate Applications (10 per page)
    app_paginator = Paginator(data['filtered_applications'], 10)
    page_app = request.GET.get('page_app', 1)
    try:
        app_page = app_paginator.page(page_app)
    except PageNotAnInteger:
        app_page = app_paginator.page(1)
    except EmptyPage:
        app_page = app_paginator.page(app_paginator.num_pages)

    sch_page_range = _get_standard_page_range(sch_page.number, sch_paginator.num_pages)
    app_page_range = _get_standard_page_range(app_page.number, app_paginator.num_pages)

    filter_term = data.get('filter_term', '')
    filter_month = data.get('filter_month', '')
    filter_year = data.get('filter_year', '')

    data['filtered_scholarships'] = sch_page
    data['filtered_applications'] = app_page
    data['sch_page_range'] = sch_page_range
    data['app_page_range'] = app_page_range
    data['sch_extra_query'] = f"term={filter_term}&month={filter_month}&year={filter_year}&tab=records&subtab=sch"
    data['app_extra_query'] = f"term={filter_term}&month={filter_month}&year={filter_year}&tab=records&subtab=apps"
    data['active_tab'] = active_tab
    data['active_subtab'] = active_subtab

    return render(request, 'scholarship_dashboard.html', data)

@staff_member_required
def export_dashboard_pdf(request):
    data = _get_dashboard_analytics_data(request)
    data['auto_print'] = (request.GET.get('auto_print') == '1')
    data['generated_by'] = request.user
    data['generated_at'] = timezone.now()
    return render(request, 'scholarship_export_pdf.html', data)

@staff_member_required
def delete_scholarship(request, pk):
    if request.method == 'POST':
        scholarship = get_object_or_404(Scholarship, pk=pk)
        title = scholarship.title
        scholarship.delete()
        messages.success(request, _('Scholarship "%(title)s" has been deleted.') % {'title': title})
    return redirect('scholarships')
