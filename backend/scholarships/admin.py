from django.contrib import admin
from django.contrib.auth.models import Group
from .models import StudentProfile, Scholarship, Application, Document

# ซ่อน Groups ออกจาก Admin Panel (ไม่ได้ใช้ในระบบนี้)
admin.site.unregister(Group)


# ─── Scholarship ──────────────────────────────────────────────
@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'amount_per_semester', 'status', 'end_date']
    list_filter = ['category', 'status']
    search_fields = ['title']


# ─── Student Profile ──────────────────────────────────────────
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'faculty', 'gpax']
    search_fields = ['student_id', 'full_name']


# ─── Application ──────────────────────────────────────────────
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'scholarship', 'status', 'submitted_at']
    list_filter = ['status']


# ─── Document ─────────────────────────────────────────────────
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['application', 'doc_type', 'uploaded_at']