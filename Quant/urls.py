"""Quant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from adminpanel.views import Login, PasswordResetConfirmView, PasswordResetView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('rest-api/', include('restapi.urls', namespace='rest')),
                  path('service-provider-rest-api/', include('serviceprovider.urls', namespace='serviceprovider')),
                  path('adminpanel/', include('adminpanel.urls', namespace='adminpanel')),
                  path('login/', Login.as_view(), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
                  path('password-reset/',
                       PasswordResetView.as_view(),
                       name='password_reset'),
                  path('password-reset-confirm/<uidb64>/<token>/',
                       PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),

                  path('password-reset-done/',
                       auth_views.PasswordResetDoneView.as_view(
                           template_name='password_reset_done.html'
                       ),
                       name='password_reset_done'),

                  path('password-reset-complete/',
                       auth_views.PasswordResetCompleteView.as_view(
                           template_name='password_reset_complete.html'
                       ),
                       name='password_reset_complete'),
                  path('cms/', include('cms.urls', namespace='cms')),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('change-password/',
                       auth_views.PasswordChangeView.as_view(template_name='change_password.html'),
                       name='change-password'),
                  path('password-change-done',
                       auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'),
                       name='password_change_done'),
                  # path('cadmin/', include('cadmin.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
