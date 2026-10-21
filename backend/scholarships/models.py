from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    FACULTY_CHOICES = [
        ('computing', 'วิทยาลัยการคอมพิวเตอร์'),
        ('engineering', 'วิศวกรรมศาสตร์'),
        ('science', 'วิทยาศาสตร์'),
        ('management', 'การจัดการ'),
        ('other', 'อื่นๆ'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    faculty = models.CharField(max_length=100, choices=FACULTY_CHOICES)
    major = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=True)
    gpax = models.FloatField(default=0.0)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"


class Scholarship(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'ทุนการศึกษาทั่วไป'),
        ('exchange', 'ทุนการศึกษาแลกเปลี่ยน'),
        ('fee_waiver', 'ทุนยกเว้นค่าธรรมเนียม'),
        ('lunch', 'ทุนอาหารกลางวัน'),
    ]
    STATUS_CHOICES = [
        ('active', 'เปิดรับสมัคร'),
        ('closed', 'ปิดรับสมัคร'),
        ('draft', 'ฉบับร่าง'),
    ]

    title = models.CharField(max_length=300)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    requirements = models.TextField()
    amount_per_semester = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        from django.utils import timezone
        return self.end_date < timezone.now().date() or self.status == 'closed'

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอพิจารณา'),
        ('interview', 'รอสัมภาษณ์'),
        ('approved', 'อนุมัติ'),
        ('rejected', 'ไม่อนุมัติ'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'scholarship')

    def __str__(self):
        return f"{self.student.full_name} → {self.scholarship.title}"


class Document(models.Model):
    TYPE_CHOICES = [
        ('transcript', 'ใบแสดงผลการเรียน'),
        ('recommendation', 'หนังสือแนะนำ'),
        ('other', 'อื่นๆ'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    doc_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_type} - {self.application}"
class FavoriteScholarship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_scholarships')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'scholarship')

    def __str__(self):
        return f"{self.user.username} - {self.scholarship.title}"
