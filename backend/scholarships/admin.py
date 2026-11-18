from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.db import models
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


# ─── Scholarship Filters & Admin ──────────────────────────────
class HasEnglishTranslationFilter(admin.SimpleListFilter):
    title = _('English Translation')
    parameter_name = 'has_en'

    def lookups(self, request, model_admin):
        return [
            ('yes', _('Has English Translation')),
            ('no', _('Missing English Translation')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(title_en__exact='').exclude(title_en__isnull=True)
        if self.value() == 'no':
            return queryset.filter(models.Q(title_en__exact='') | models.Q(title_en__isnull=True))
        return queryset


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'title_en_indicator', 'category', 'amount_per_semester', 'status', 'end_date']
    list_filter = ['category', 'status', HasEnglishTranslationFilter]
    search_fields = ['title', 'title_en', 'description', 'description_en', 'requirements', 'requirements_en']
    fieldsets = (
        (_('Primary Info (Thai / Default)'), {
            'fields': ('title', 'category', 'description', 'requirements')
        }),
        (_('English Translation (Optional / Recommended)'), {
            'fields': ('title_en', 'description_en', 'requirements_en'),
            'description': _('Enter the English version of title, description, and requirements for international students.')
        }),
        (_('Schedule & Award Details'), {
            'fields': ('amount_per_semester', 'capacity', 'start_date', 'end_date', 'status', 'created_by')
        }),
    )

    @admin.display(description=_('EN Translation'), boolean=True)
    def title_en_indicator(self, obj):
        return bool(obj.title_en and obj.title_en.strip())


# ─── Student Profile ──────────────────────────────────────────
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'faculty', 'gpax', 'preferred_language']
    list_filter = ['faculty', 'preferred_language']
    search_fields = ['student_id', 'full_name', 'phone_number']


# ─── Application ──────────────────────────────────────────────
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'scholarship', 'status', 'submitted_at']
    list_filter = ['status']


# ─── Document ─────────────────────────────────────────────────
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['application', 'doc_type', 'uploaded_at']
