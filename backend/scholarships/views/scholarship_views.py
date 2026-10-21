from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Sum
from ..models import Scholarship, Application, StudentProfile, Document
from .utils import enrich_scholarships

def home(request):
    today = timezone.now().date()
    scholarships_qs = Scholarship.objects.filter(status='active', end_date__gte=today).order_by('-id')[:6]
    scholarships = enrich_scholarships(scholarships_qs, request.user)
    total_count = Scholarship.objects.filter(status='active', end_date__gte=today).count()
    active_count = total_count
    total_value = Scholarship.objects.filter(status='active', end_date__gte=today).aggregate(total=Sum('amount_per_semester'))['total'] or 0
    categories = [
        {'code': 'general', 'name': _('ทุนการศึกษาทั่วไป'), 'code_num': '01', 'desc': _('ทุนสนับสนุนการศึกษาสำหรับนักศึกษาทั่วไป ทุนขาดแคลนทุนทรัพย์'), 'count': Scholarship.objects.filter(category='general', status='active', end_date__gte=today).count()},
        {'code': 'exchange', 'name': _('ทุนศึกษาแลกเปลี่ยน'), 'code_num': '02', 'desc': _('ทุนสนับสนุนการแลกเปลี่ยนต่างประเทศและโครงการระดับนานาชาติ'), 'count': Scholarship.objects.filter(category='exchange', status='active', end_date__gte=today).count()},
        {'code': 'fee_waiver', 'name': _('ทุนยกเว้นค่าธรรมเนียม'), 'code_num': '03', 'desc': _('ทุนยกเว้นค่าธรรมเนียมการศึกษาตามเกณฑ์ผลการเรียนและกิจกรรม'), 'count': Scholarship.objects.filter(category='fee_waiver', status='active', end_date__gte=today).count()},
        {'code': 'lunch', 'name': _('ทุนอาหารกลางวัน'), 'code_num': '04', 'desc': _('ทุนสวัสดิการอาหารกลางวันเพื่อสุขภาวะและการใช้ชีวิตในรั้วมหาวิทยาลัย'), 'count': Scholarship.objects.filter(category='lunch', status='active', end_date__gte=today).count()},
    ]
    
    expiring_qs = Scholarship.objects.filter(
        status='active', 
        end_date__gte=today,
        end_date__month=today.month,
        end_date__year=today.year
    ).order_by('end_date')[:6]
    expiring_soon = enrich_scholarships(expiring_qs, request.user)
    
    return render(request, 'index.html', {
        'featured_scholarships': scholarships,
        'expiring_soon': expiring_soon,
        'total_count': total_count,
        'active_count': active_count,
        'total_value': total_value,
        'categories': categories,
    })

def scholarships(request):
    return render(request, 'scholarships/category.html', {})

def scholarship_list(request, category):
    query = request.GET.get('q', '')
    today = timezone.now().date()

    if category == 'all':
        items = Scholarship.objects.filter(status='active', end_date__gte=today).order_by('-id')
    else:
        items = Scholarship.objects.filter(category=category, status='active', end_date__gte=today).order_by('-id')

    if query:
        items = items.filter(title__icontains=query)

    items = enrich_scholarships(items, request.user)

    category_names = {
        'all': 'ทุนการศึกษาทั้งหมด',
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
    scholarship = get_object_or_404(Scholarship, pk=pk)
    already_applied = False

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            already_applied = Application.objects.filter(
                student=profile, scholarship=scholarship).exists()
        except:
            pass
        from ..models import FavoriteScholarship
        is_favorited = FavoriteScholarship.objects.filter(user=request.user, scholarship=scholarship).exists()
    else:
        is_favorited = False

    return render(request, 'scholarships/detail.html', {
        'scholarship': scholarship,
        'already_applied': already_applied,
        'is_expired': scholarship.is_expired,
        'is_favorited': is_favorited,
    })

@login_required
def apply_form(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)

    if scholarship.is_expired:
        messages.error(request, 'ขออภัย ทุนการศึกษานี้ปิดรับสมัครหรือหมดเขตแล้ว')
        return redirect('scholarship_detail', pk=pk)

    approved_count = Application.objects.filter(
        scholarship=scholarship, status__in=['pending', 'approved']).count()
    if approved_count >= scholarship.capacity:
        scholarship.status = 'closed'
        scholarship.save()
        messages.error(request, 'ขออภัย ทุนนี้รับสมัครครบตามจำนวนแล้ว')
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
            
        # Send confirmation email
        from ..emails import send_application_received_email
        try:
            send_application_received_email(application)
        except Exception as e:
            # We don't want the application process to fail if email fails
            print(f"Failed to send email: {e}")

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

@login_required
def toggle_favorite(request, pk):
    from django.http import JsonResponse
    scholarship = get_object_or_404(Scholarship, pk=pk)
    from ..models import FavoriteScholarship
    
    favorite, created = FavoriteScholarship.objects.get_or_create(
        user=request.user, 
        scholarship=scholarship
    )
    
    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'is_favorited': is_favorited})
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def my_favorites(request):
    from ..models import FavoriteScholarship
    favorite_ids = FavoriteScholarship.objects.filter(user=request.user).values_list('scholarship_id', flat=True)
    today = timezone.now().date()
    qs = Scholarship.objects.filter(id__in=favorite_ids).order_by('end_date')
    favorites = enrich_scholarships(qs, request.user)
    
    return render(request, 'scholarships/favorites.html', {
        'favorites': favorites,
    })
