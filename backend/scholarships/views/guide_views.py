from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _

def student_guide(request):
    """
    Public and student user guide for scholarship application, eligibility,
    document uploads, and status tracking.
    """
    return render(request, 'guide/student_guide.html', {
        'page_title': _('Student Guide & Manual'),
    })

def admin_guide(request):
    """
    Protected guide strictly for staff and administrators covering review workflow,
    document verification, status transitions, additional document requests,
    and scholarship management.
    """
    if not request.user.is_authenticated:
        return redirect(f"/login/?next={request.path}")
    
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, _('Access denied. Administrator guide is restricted to staff members.'))
        return redirect('student_guide')

    return render(request, 'guide/admin_guide.html', {
        'page_title': _('Administrator System Guide'),
    })

def guide_redirect(request):
    """
    Smart guide router that directs users to the appropriate guide based on their role.
    """
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_guide')
    return redirect('student_guide')

