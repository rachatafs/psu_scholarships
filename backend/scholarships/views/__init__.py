from .auth_views import CustomLoginView, profile, auth_redirect
from .scholarship_views import home, scholarships, scholarship_list, scholarship_detail, apply_form, apply_success, toggle_favorite, my_favorites
from .admin_views import admin_dashboard, scholarship_dashboard, export_dashboard_pdf, update_application, delete_scholarship
from .misc_views import jobs, payment_form, about, team, contact, news, faq
from .guide_views import student_guide, admin_guide, guide_redirect

__all__ = [
    'CustomLoginView',
    'profile',
    'auth_redirect',
    'home',
    'scholarships',
    'scholarship_list',
    'scholarship_detail',
    'apply_form',
    'apply_success',
    'toggle_favorite',
    'my_favorites',
    'admin_dashboard',
    'scholarship_dashboard',
    'export_dashboard_pdf',
    'update_application',
    'delete_scholarship',
    'jobs',
    'payment_form',
    'about',
    'team',
    'contact',
    'news',
    'faq',
    'student_guide',
    'admin_guide',
    'guide_redirect',
]

