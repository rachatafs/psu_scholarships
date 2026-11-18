from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class StudentProfile(models.Model):
    FACULTY_CHOICES = [
        ('computing', _('College of Computing')),
        ('engineering', _('Faculty of Engineering')),
        ('science', _('Faculty of Science')),
        ('management', _('Faculty of Management Sciences')),
        ('other', _('Other')),
    ]

    LANGUAGE_CHOICES = [
        ('th', _('Thai')),
        ('en', _('English')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    faculty = models.CharField(max_length=100, choices=FACULTY_CHOICES)
    major = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=True)
    gpax = models.FloatField(default=0.0)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='th')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"


class Scholarship(models.Model):
    CATEGORY_CHOICES = [
        ('general', _('General Scholarships')),
        ('exchange', _('Exchange Scholarships')),
        ('fee_waiver', _('Fee Waiver Scholarships')),
        ('lunch', _('Lunch Scholarships')),
    ]
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('closed', _('Closed')),
        ('draft', _('Draft')),
    ]

    title = models.CharField(max_length=300, help_text="Scholarship title in Thai (or default)")
    title_en = models.CharField(max_length=300, blank=True, default='', help_text="Scholarship title in English")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(help_text="Scholarship description in Thai (or default)")
    description_en = models.TextField(blank=True, default='', help_text="Scholarship description in English")
    requirements = models.TextField(help_text="Scholarship requirements in Thai (or default)")
    requirements_en = models.TextField(blank=True, default='', help_text="Scholarship requirements in English")
    amount_per_semester = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def localized_title(self):
        from django.utils.translation import get_language
        lang = (get_language() or 'en').lower()
        if lang.startswith('en') and self.title_en:
            return self.title_en
        return self.title or self.title_en

    @property
    def localized_description(self):
        from django.utils.translation import get_language
        lang = (get_language() or 'en').lower()
        if lang.startswith('en') and self.description_en:
            return self.description_en
        return self.description or self.description_en

    @property
    def localized_requirements(self):
        from django.utils.translation import get_language
        lang = (get_language() or 'en').lower()
        if lang.startswith('en') and self.requirements_en:
            return self.requirements_en
        return self.requirements or self.requirements_en

    @property
    def is_expired(self):
        from django.utils import timezone
        return self.end_date < timezone.now().date() or self.status == 'closed'

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('interview', _('Interview')),
        ('approved', _('Approve')),
        ('rejected', _('Reject')),
        ('completed', _('Complete')),
        ('cancelled', _('Cancel')),
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
        ('transcript', _('Academic Transcript')),
        ('recommendation', _('Recommendation Letter')),
        ('other', _('Other')),
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
