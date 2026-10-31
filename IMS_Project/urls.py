"""
URL configuration for IMS_Project project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # =====================================
    # ADMIN
    # =====================================

    path('admin/', admin.site.urls),

    # =====================================
    # MAIN APPLICATION URLS
    # =====================================

    path('', include('app_name.urls')),

]


# =====================================
# MEDIA FILES - PRODUCT IMAGES
# =====================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )