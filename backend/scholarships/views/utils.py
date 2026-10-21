from django.utils import timezone
from ..models import Application

def enrich_scholarships(scholarships_qs, user):
    """
    Enriches scholarship objects with user-specific and deadline status:
    - s.is_closed: True if expired or status != 'active'
    - s.has_applied: True if logged-in student has submitted application
    - s.gpax_unmet: True if logged-in student's GPAX is lower than scholarship min_gpax
    - s.student_gpax: student's GPAX value
    - s.is_favorited: True if user has favorited this scholarship
    """
    from ..models import Application, FavoriteScholarship
    
    student_profile = None
    applied_ids = set()
    favorited_ids = set()
    if user.is_authenticated:
        try:
            student_profile = getattr(user, 'profile', None)
            if student_profile:
                applied_ids = set(
                    Application.objects.filter(student=student_profile).values_list('scholarship_id', flat=True)
                )
            favorited_ids = set(
                FavoriteScholarship.objects.filter(user=user).values_list('scholarship_id', flat=True)
            )
        except Exception:
            pass

    today = timezone.now().date()
    items = list(scholarships_qs)
    for s in items:
        s.is_closed = (s.status == 'closed' or s.end_date < today)
        s.has_applied = (s.id in applied_ids)
        s.is_favorited = (s.id in favorited_ids)
        
        # Determine GPAX eligibility
        s.gpax_unmet = False
        s.student_gpax = None
        min_gpax = getattr(s, 'min_gpax', None)
        if student_profile:
            s.student_gpax = student_profile.gpax
            if min_gpax and s.student_gpax:
                s.gpax_unmet = s.student_gpax < min_gpax

    return items

CATEGORY_NAMES = {
    'all': 'ทุนการศึกษาทั้งหมด',
    'general': 'ทุนการศึกษาทั่วไป',
    'exchange': 'ทุนการศึกษาแลกเปลี่ยน',
    'fee_waiver': 'ทุนยกเว้นค่าธรรมเนียม',
    'lunch': 'ทุนอาหารกลางวัน',
}
