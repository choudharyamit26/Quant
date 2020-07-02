from django.db import models
from django.shortcuts import reverse
from localflavor.us.us_states import STATE_CHOICES

# US_STATES = (("Alabama", "Alabama"), ("Alaska", "Alaska"), ("Arizona", "Arizona"), ("Arkansas", "Arkansas"),
#              ("California", "California"), ("Colorado", "Colorado"), ("Connecticut", "Connecticut"),
#              ("Delaware", "Delaware"), ("Florida", "Florida"), ("Georgia", "Georgia"), ("Hawaii", "Hawaii"),
#              ("Idaho", "Idaho"), ("Illinois", "Illinois"), ("Indiana", "Indiana"), ("Iowa", "Iowa"),
#              ("Kansas", "Kansas"), ("Kentucky", "Kentucky"), ("Louisiana", "Louisiana"), ("Maine", "Maine"),
#              ("Maryland", "Maryland"), ("Massachusetts", "Massachusetts"), ("Michigan", "Michigan"),
#              ("Minnesota", "Minnesota"), ("Mississippi", "Mississippi"), ("Missouri", "Missouri"),
#              ("Montana", "Montana"), ("Nebraska", "Nebraska"), ("Nevada", "Nevada"), ("New Hampshire", "New Hampshire"),
#              ("New Jersey", "New Jersey"), ("New Mexico", "New Mexico"), ("New York", "New York"),
#              ("North Carolina", "North Carolina"), ("North Dakota", "North Dakota"), ("Ohio", "Ohio"),
#              ("Oklahoma", "Oklahoma"), ("Oregon", "Oregon"), ("Pennsylvania", "Pennsylvania"),
#              ("Rhode Island", "Rhode Island"), ("South Carolina", "South Carolina"), ("South Dakota", "South Dakota"),
#              ("Tennessee", "Tennessee"), ("Texas", "Texas"), ("Utah", "Utah"), ("Vermont", "Vermont"),
#              ("Virginia", "Virginia"), ("Washington", "Washington"), ("West Virginia", "West Virginia"),
#              ("Wisconsin", "Wisconsin"), ("Wyoming", "Wyoming"))

CATEGORY_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

SERVICE_CHOICES = (
    ("Business has service currently but I want to compare rates",
     "Business has service currently but I want to compare rates"),
    ("Business has service currently but it's moving location",
     "Business has service currently but it's moving location"),
    ("Business is new and does not have service currently",
     "Business is new and does not have service currently"),
)

QUERY_TYPE = (
    ("Electricity for my Business", "Electricity for my Business"),
    ("Electricity for my residence", "Electricity for my residence"),
)


class ElectricityProvider(models.Model):
    electricity_provider_code = models.CharField(max_length=100)
    electricity_provider_name = models.CharField(max_length=100)

    def __str__(self):
        return self.electricity_provider_name

    class Meta:
        ordering = ('-electricity_provider_code',)


class InquiryformModel(models.Model):
    bussiness_name = models.CharField(max_length=256)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.BigIntegerField()
    zip = models.BigIntegerField()
    service_date = models.DateField()
    amount_due = models.BigIntegerField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    total_usages = models.BigIntegerField(null=True, blank=True)
    electric_heat = models.CharField(choices=CATEGORY_CHOICES, max_length=256, null=True, blank=True)
    balanced_bill = models.CharField(choices=CATEGORY_CHOICES, max_length=256, null=True, blank=True)
    current_electricity_provider = models.ForeignKey(ElectricityProvider, on_delete=models.CASCADE, null=True,
                                                     blank=True)
    user_type = models.CharField(choices=SERVICE_CHOICES, max_length=256, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    qs = models.CharField(max_length=100, default='search')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.bussiness_name

    def get_absolute_url(self):
        return reverse("adminpanel:form-detail", kwargs={'pk': self.pk})


class CustomUser(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street = models.CharField(max_length=256, default="")
    city = models.CharField(max_length=256, default="")
    state = models.CharField(max_length=256, default="", choices=STATE_CHOICES)
    zip = models.PositiveIntegerField(default=0)
    phone = models.BigIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=200, default='test')
    confirm_password = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("adminpanel:customuser-detail", kwargs={'pk': self.pk})


class ContactUs(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.BigIntegerField()
    query_type = models.CharField(choices=QUERY_TYPE, max_length=255)
    message = models.TextField(default='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("adminpanel:contactus-detail", kwargs={'pk': self.pk})


class NotifyMe(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    street = models.CharField(max_length=256, default="")
    city = models.CharField(max_length=256, default="")
    state = models.CharField(max_length=256, default="", choices=STATE_CHOICES)
    zip = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    contact_no = models.BigIntegerField(default=123)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("adminpanel:notify-detail", kwargs={'pk': self.pk})


class SubscribeNow(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.email
