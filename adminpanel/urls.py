from django.conf.urls.static import static
from django.urls import path

from .views import *

app_name = 'adminpanel'

urlpatterns = [
                  path('', Login.as_view(), name='login'),
                  path('inquiry-list/', InquiryformListView.as_view(), name='form-list'),
                  path('form-detail/<int:pk>/', InquiryFormDetails.as_view(), name='form-detail'),
                  path('form-delete/<int:pk>/', InquiryFormDelete.as_view(), name='form-delete'),
                  path('form-download/<int:pk>/', InquiryFormDetailDownload.as_view(), name='form-download'),
                  path('form-list-download/', InquiryFormDetaillistDownload.as_view(), name='form-list-download'),
                  path('contactus-list/', ContactusView.as_view(), name='contactus-list'),
                  path('contactus-detail/<int:pk>/', ContactusDetailView.as_view(), name='contactus-detail'),
                  path('contactus-delete/<int:pk>/', ContactusDeleteView.as_view(), name='contactus-delete'),
                  path('contactus-detail-download/<int:pk>/', ContactusDetailDownloadView.as_view(),
                       name='contactus-detail-download'),
                  path('contactus-list-download/', ContactusListDownloadView.as_view(), name='contactus-list-download'),
                  path('customuser-list/', CustomUserView.as_view(), name='customuser-list'),
                  path('customuser-detail/<int:pk>/', CustomUserDetailView.as_view(), name='customuser-detail'),
                  path('customuser-delete/<int:pk>/', CustomUserDeleteView.as_view(), name='customuser-delete'),
                  path('customuser-detail-download/<int:pk>/', CustomUserDetailDownloadView.as_view(),
                       name='customuser-download'),
                  path('customuser-detail-list/', CustomUserListDownloadView.as_view(),
                       name='customuser-detail-listdownload'),
                  path('notifyme-list/', NotifyMeView.as_view(), name='notifyme-list'),
                  path('notify-detail/<int:pk>/', NotifyMeDetailView.as_view(), name='notify-detail'),
                  path('notify-delete/<int:pk>/', NotifyMeDeleteView.as_view(), name='notify-delete'),
                  path('notify-detail-download/<int:pk>/', NotifyMeDetailDownloadView.as_view(),
                       name='notify-detail-download'),
                  path('notify-list-download/', NotifyMeListDownloadView.as_view(), name='notify-list-download'),
                  path('subscribenow/', SubscribeView.as_view(), name='subscribenow'),
                  path('subscribenow-delete/<int:pk>/', SubscribenowDeleteView.as_view(), name='subscribenow-delete'),
                  path('subscriber-list-download/', SubscriberlistDownloadView.as_view(),
                       name='subscriber-list-download'),
                  path('post-create/', CmsCreate.as_view(), name='post-create'),
                  path('post-list/', CmsList.as_view(), name='post-list'),
                  path('post-detail/<int:pk>/', CmsDetail.as_view(), name='post-detail'),
                  path('post-update/<int:pk>/', CmsUpdate.as_view(), name='post-update'),
                  path('post-delete/<int:pk>/', CmsDelete.as_view(), name='post-delete'),

                  # path('import/', ImportCSVData.as_view(), name='import-data'),
                  # path('test/', Elecdata.as_view(), name='elec'),
              ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
