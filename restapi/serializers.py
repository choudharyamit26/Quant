from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import serializers

from .models import InquiryformModel, ElectricityProvider, CustomUser, ContactUs, NotifyMe, SubscribeNow


class InquiryFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryformModel
        fields = (
            'bussiness_name',
            'full_name',
            'email',
            'phone',
            'zip',
            'service_date',
            'amount_due',
            'due_date',
            'total_usages',
            'electric_heat',
            'balanced_bill',
            'current_electricity_provider',
            'user_type',
        )

    # def validate_email(self, email):
    #     allowedDomains = [
    #         "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
    #         "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
    #         "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
    #         "email.com", "games.com", "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
    #         "lavabit.com", "love.com", "outlook.com", "pobox.com", "rocketmail.com",
    #         "safe-mail.net", "wow.com", "ygm.com", "ymail.com", "zoho.com", "fastmail.fm",
    #         "yandex.com", "iname.com", "yopmail.com", "rediffmail.com",
    #     ]
    #     domain = email.split("@")[1].lower()
    #     if domain not in allowedDomains:
    #         raise ValidationError('Invalid email address')
    #     user_qs = User.objects.filter(email__iexact=email)
    #     if user_qs.exists():
    #         raise ValidationError('User with this Email already exists')
    #     return email

    def create(self, validate_data):
        instance = super().create(validate_data)
        email_template = 'sendMail.html'

        context = {
            'bussiness_name': validate_data["bussiness_name"],
            'full_name': validate_data["full_name"],
            'email': validate_data["email"],
            'phone': validate_data["phone"],
            'zip': validate_data["zip"],
            'service_date': validate_data["service_date"],
            'amount_due': validate_data["amount_due"],
            'due_date': validate_data["due_date"],
            'total_usages': validate_data["total_usages"],
            'electric_heat': validate_data["electric_heat"],
            'balanced_bill': validate_data["balanced_bill"],
            'current_electricity_provider': validate_data["current_electricity_provider"],
            'user_type': validate_data["user_type"],

        }

        email = render_to_string(email_template, context)
        msg = EmailMultiAlternatives('Business enquiry request', email, 'joelmathew.clix@gmail.com',
                                     ['amitkumar.clixlogix@gmail.com'])
        msg.content_subtype = "html"
        msg.send()
        return instance


# 'santosh@quant.energy',
# team@quant.energy ',

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    confirm_password = serializers.CharField(

        style={'input_type': 'password'},
        trim_whitespace=False
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name", "last_name", "street", "city", "state", "zip", "phone", 'email', 'password',
            'confirm_password')


class ContactUsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ("first_name", "last_name", "query_type", "contact_number", 'email', 'message')

    def create(self, validated_data):
        instance = super().create(validated_data)
        email_template = 'contactus-mail.html'

        context = {
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'email': validated_data['email'],
            'contact_number': validated_data['contact_number'],
            'query_type': validated_data['query_type'],
            'message': validated_data['message'],
        }

        email = render_to_string(email_template, context)
        msg = EmailMultiAlternatives("Contact Us Form", email, 'joelmathew.clix@gmail.com',
                                     ['amitkumar.clixlogix@gmail.com'])
        msg.content_subtype = "html"
        msg.send()
        return instance


class NotifyMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotifyMe
        fields = ("first_name", "last_name", "email", 'contact_no', "street", "city", "state", "zip")

    def create(self, validated_data):
        instance = super().create(validated_data)
        email_template = 'notifyme-mail.html'

        context = {
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'email': validated_data['email'],
            'contact_no': validated_data['contact_no'],
            'street': validated_data['street'],
            'city': validated_data['city'],
            'state': validated_data['state'],
            'zip': validated_data['zip'],
        }

        email = render_to_string(email_template, context)
        msg = EmailMultiAlternatives("Notify Me Form", email, 'joelmathew.clix@gmail.com',
                                     ['amitkumar.clixlogix@gmail.com'])

        msg.content_subtype = "html"
        msg.send()
        return instance


class ElectricityProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityProvider
        fields = ('electricity_provider_name', 'id')


class SubscribeNowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeNow
        fields = ('email',)
