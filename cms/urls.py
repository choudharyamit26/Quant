from django.urls import path
from .views import *

app_name = 'cms'

urlpatterns = [
    path('content/', CMSView.as_view(), name='content')
]
