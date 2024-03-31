"""
URL configuration for accounting_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", include("apps.login.urls")),
    path("requests/", include("apps.requests.urls")),
    path("teams/", include("apps.teams.urls")),
    path("registration/", include("apps.registration.urls")),
    path("emailContact/", include("apps.emailContact.urls")),
    path("permissions/", include("apps.permissions.urls")),
    path("error/", include("apps.errorHandler.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "apps.errorHandler.views.error_404_view"
