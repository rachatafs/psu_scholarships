from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import StudentProfile, Scholarship, Application, Document

# ซ่อน Groups ออกจาก Admin Panel (ไม่ได้ใช้ในระบบนี้)
admin.site.unregister(Group)

# ปรับแต่ง User Admin: เอา 'กลุ่ม' (groups) และ 'สิทธิ์ของผู้ใช้' (user_permissions) ออก
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ()

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


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