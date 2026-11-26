from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('scholarships.urls')),
    prefix_default_language=False,
) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
