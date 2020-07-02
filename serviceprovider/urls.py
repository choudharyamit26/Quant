from django.urls import path
from .views import CreateServiceProvider

app_name = 'serviceprovider'

urlpatterns = [
    path('', CreateServiceProvider.as_view(), name='serviceprovider'),
]
