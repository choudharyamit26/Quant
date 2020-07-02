from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import (InquiryFormView,
                    ListServiceProvider,
                    CreateUserView,
                    ContactusFormView,
                    NotifyMeView,
                    SubscribeNowView)

app_name = 'restapi'

schema_view = get_schema_view(
    openapi.Info(
        title="Quant Energy API",
        default_version='v1',
        description="APIs for Quant Energy Electricity Provider List and Inquiryform.",
        terms_of_service="https://www.quantenergy.com",
        contact=openapi.Contact(email="amitkuamr.clixlogix@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('inquiryform/', InquiryFormView.as_view(), name='inquiryform'),
    path('contactus-residential/', ContactusFormView.as_view(), name='contactus-residential'),
    path('notifyme/', NotifyMeView.as_view(), name='notifyme'),
    path('createuser/', CreateUserView.as_view(), name='createuser'),
    path('serviceprovider/', ListServiceProvider.as_view(), name='serviceprovider'),
    path('subscribenow/', SubscribeNowView.as_view(), name='subscribenow'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('openapi/', get_schema_view(), name='openapi-schema'),

    # path('test/api',TestAPi.as_view(),name="Test API")

]
