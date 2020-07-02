from django.contrib import admin

from .models import ElectricityProvider, InquiryformModel, CustomUser, ContactUs, NotifyMe, SubscribeNow

admin.site.register(ElectricityProvider)
admin.site.register(InquiryformModel)
admin.site.register(CustomUser)
admin.site.register(ContactUs)
admin.site.register(NotifyMe)
admin.site.register(SubscribeNow)
