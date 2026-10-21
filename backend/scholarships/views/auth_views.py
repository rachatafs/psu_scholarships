from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.models import User
from ..models import StudentProfile, Application

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return '/admin-dashboard/'
        return '/'

@login_required
def profile(request):
    try:
        student_profile = request.user.profile
    except:
        student_profile = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        student_id = request.POST.get('student_id', '')
        faculty = request.POST.get('faculty', '')
        major = request.POST.get('major', '')
        phone_number = request.POST.get('phone_number', '')
        profile_image = request.FILES.get('profile_image')

        if student_profile:
            student_profile.full_name = full_name
            student_profile.student_id = student_id
            student_profile.faculty = faculty
            student_profile.major = major
            student_profile.phone_number = phone_number
            if profile_image:
                student_profile.profile_image = profile_image
            student_profile.save()
        else:
            sp = StudentProfile(
                user=request.user,
                full_name=full_name,
                student_id=student_id or request.user.username,
                faculty=faculty,
                major=major,
                phone_number=phone_number,
            )
            if profile_image:
                sp.profile_image = profile_image
            sp.save()
            student_profile = sp

        messages.success(request, 'บันทึกข้อมูลเรียบร้อย!')
        return redirect('profile')

    app_list = []
    if student_profile:
        app_list = Application.objects.filter(
            student=student_profile).select_related('scholarship').order_by('-submitted_at')

    return render(request, 'accounts/profile.html', {
        'student_profile': student_profile,
        'applications': app_list,
    })

