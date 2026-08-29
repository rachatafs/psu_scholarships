from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.utils import timezone
from .models import Scholarship, Application, StudentProfile, Document


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return '/admin-dashboard/'
        return '/'


def home(request):
    return render(request, 'index.html', {})


def scholarships(request):
    return render(request, 'scholarships/category.html', {})


def scholarship_list(request, category):
    query = request.GET.get('q', '')

    items = Scholarship.objects.filter(category=category, status='active')

    if query:
        items = items.filter(title__icontains=query)

    category_names = {
        'general': 'ทุนการศึกษาทั่วไป',
        'exchange': 'ทุนการศึกษาแลกเปลี่ยน',
        'fee_waiver': 'ทุนยกเว้นค่าธรรมเนียม',
        'lunch': 'ทุนอาหารกลางวัน',
    }
    return render(request, 'scholarships/list.html', {
        'scholarships': items,
        'category_title': category_names.get(category, 'ทุนการศึกษา'),
        'category': category,
        'query': query,
    })


def scholarship_detail(request, pk):
    scholarship = Scholarship.objects.get(pk=pk)
    already_applied = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            already_applied = Application.objects.filter(
                student=profile, scholarship=scholarship).exists()
        except:
            pass
    return render(request, 'scholarships/detail.html', {
        'scholarship': scholarship,
        'already_applied': already_applied,
    })


@login_required
def apply_form(request, pk):
    scholarship = Scholarship.objects.get(pk=pk)

    approved_count = Application.objects.filter(
        scholarship=scholarship, status__in=['pending', 'approved']).count()
    if approved_count >= scholarship.capacity:
        scholarship.status = 'closed'
        scholarship.save()
        messages.error(request, 'ขออภัย ทุนนี้รับสมัครครบแล้ว')
        return redirect('scholarship_detail', pk=pk)

    try:
        student_profile = request.user.profile
    except:
        student_profile = None

    if request.method == 'POST':
        if student_profile and Application.objects.filter(
                student=student_profile, scholarship=scholarship).exists():
            messages.warning(request, 'คุณได้สมัครทุนนี้แล้ว')
            return redirect('scholarship_detail', pk=pk)

        if not student_profile:
            student_profile = StudentProfile.objects.create(
                user=request.user,
                student_id=request.POST.get('student_id', request.user.username),
                full_name=request.POST.get('full_name', request.user.username),
                faculty='other',
                major=request.POST.get('faculty_major', ''),
                phone_number=request.POST.get('phone', ''),
            )
        else:
            student_profile.phone_number = request.POST.get('phone', student_profile.phone_number)
            student_profile.save()

        application = Application.objects.create(
            student=student_profile,
            scholarship=scholarship,
            status='pending'
        )

        for doc_type in ['transcript', 'recommendation']:
            file = request.FILES.get(doc_type)
            if file:
                Document.objects.create(
                    application=application,
                    file=file,
                    doc_type=doc_type
                )

        total = Application.objects.filter(
            scholarship=scholarship, status__in=['pending', 'approved']).count()
        if total >= scholarship.capacity:
            scholarship.status = 'closed'
            scholarship.save()

        return redirect('apply_success', pk=pk)

    return render(request, 'scholarships/apply.html', {
        'scholarship': scholarship,
        'student_profile': student_profile,
    })


def apply_success(request, pk):
    scholarship = Scholarship.objects.get(pk=pk)
    application = None
    try:
        profile = request.user.profile
        application = Application.objects.filter(
            student=profile, scholarship=scholarship).last()
    except:
        pass
    return render(request, 'scholarships/apply_success.html', {
        'scholarship': scholarship,
        'application': application,
    })


def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('home')
    context = {
        'total_scholarships': Scholarship.objects.count(),
        'total_applications': Application.objects.count(),
        'pending_applications': Application.objects.filter(status='pending').count(),
        'approved_applications': Application.objects.filter(status='approved').count(),
        'applications': Application.objects.select_related(
            'student', 'scholarship').order_by('-submitted_at')[:20],
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def update_application(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('home')
    app = Application.objects.get(pk=pk)
    if request.method == 'POST':
        app.status = request.POST.get('status', 'pending')
        app.save()
        messages.success(request, f'อัพเดทสถานะเป็น {app.get_status_display()} แล้ว')
    return redirect('admin_dashboard')


@staff_member_required
def scholarship_dashboard(request):
    now = timezone.now().date()

    # คำนวณปี พ.ศ. อัตโนมัติ
    thai_year = now.year + 543

    # สถิติทุน
    total_scholarships = Scholarship.objects.count()
    total_value = Scholarship.objects.aggregate(
        total=Sum('amount_per_semester')
    )['total'] or 0
    open_scholarships = Scholarship.objects.filter(
        status='active', end_date__gte=now
    ).count()

    # สถิติการสมัคร
    total_applications    = Application.objects.count()
    pending_applications  = Application.objects.filter(status='pending').count()
    approved_applications = Application.objects.filter(status='approved').count()
    rejected_applications = Application.objects.filter(status='rejected').count()

    # ข้อมูลสำหรับ Donut Chart
    general_count  = Scholarship.objects.filter(category='general').count()
    exchange_count = Scholarship.objects.filter(category='exchange').count()
    waiver_count   = Scholarship.objects.filter(category='fee_waiver').count()
    lunch_count    = Scholarship.objects.filter(category='lunch').count()

    # รายชื่อทุนล่าสุด
    recent_scholarships = Scholarship.objects.order_by('-id')[:5]

    # ทุนที่ใกล้หมดเขต (30 วัน)
    deadline_soon = Scholarship.objects.filter(
        status='active',
        end_date__gte=now,
        end_date__lte=now + timezone.timedelta(days=30)
    ).order_by('end_date')[:5]

    context = {
        'thai_year':             thai_year,           # ← เพิ่มใหม่
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
    }
    return render(request, 'admin_dashboard.html', context)


def jobs(request):
    return render(request, 'jobs/list.html', {})


def payment_form(request):
    return render(request, 'payment/form.html', {})


def about(request):
    return render(request, 'about/index.html', {})


def team(request):
    return render(request, 'about/team.html', {})


def contact(request):
    return render(request, 'about/contact.html', {})


def news(request):
    return render(request, 'news/list.html', {})


def faq(request):
    return render(request, 'faq/index.html', {})

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
        gpax = request.POST.get('gpax', 0.0)
        profile_image = request.FILES.get('profile_image')

        if student_profile:
            student_profile.full_name = full_name
            student_profile.student_id = student_id
            student_profile.faculty = faculty
            student_profile.major = major
            student_profile.phone_number = phone_number
            student_profile.gpax = gpax
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
                gpax=gpax,
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
            student=student_profile).select_related('scholarship')

    return render(request, 'accounts/profile.html', {
        'student_profile': student_profile,
        'applications': app_list,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        from django.contrib.auth.models import User

        if password1 != password2:
            messages.error(request, 'รหัสผ่านไม่ตรงกัน')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'ชื่อผู้ใช้นี้มีอยู่แล้ว')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, f'สมัครสมาชิกสำเร็จ! ยินดีต้อนรับ {username}')
        return redirect('profile')

    return render(request, 'accounts/register.html', {})