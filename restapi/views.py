from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
import base64
from .models import ElectricityProvider, CustomUser
from .serializers import (InquiryFormSerializer,
                          ElectricityProviderSerializer,
                          UserSerializer,
                          ContactUsFormSerializer,
                          NotifyMeSerializer,
                          SubscribeNowSerializer)


class InquiryFormView(CreateAPIView):
    serializer_class = InquiryFormSerializer


class ListServiceProvider(ListAPIView):
    queryset = ElectricityProvider.objects.all()
    serializer_class = ElectricityProviderSerializer


class CreateUserView(CreateAPIView):
    model = CustomUser
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        first_name = self.request.data['first_name']
        last_name = self.request.data['last_name']
        phone = self.request.data['phone']
        street = self.request.data['street']
        city = self.request.data['city']
        zip = self.request.data['zip']
        state = self.request.data['state']
        email = self.request.data['email']
        password = self.request.data['password']
        confirm_password = self.request.data['confirm_password']
        user_qs = CustomUser.objects.filter(email__iexact=email)
        if user_qs.exists():
            serializer.is_valid(raise_exception=True)
            return Response({"Email": "User with this email already exists."}, status=HTTP_200_OK)
        context = {
            'first_name': self.request.data['first_name'],
            'last_name': self.request.data['last_name'],
            'street': self.request.data['street'],
            'city': self.request.data['city'],
            'zip': self.request.data['zip'],
            'state': self.request.data['state'],
            'phone': self.request.data['phone'],
            'email': self.request.data['email'],
        }
        if password == confirm_password:
            CustomUser.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                street=street,
                city=city,
                zip=zip,
                state=state,
                password=make_password(password),
                confirm_password=make_password(confirm_password)
            )
            email_template = 'signup-mail.html'
            email = render_to_string(email_template, context)
            msg = EmailMultiAlternatives("User Sign Up Form", email, 'joelmathew.clix@gmail.com',
                                         ['amitkumar.clixlogix@gmail.com'])
            msg.content_subtype = "html"
            msg.send()
            user_email = self.request.data['email']
            email_template2 = 'welcome.html'
            email2 = render_to_string(email_template2)
            msg2 = EmailMultiAlternatives("Thank you. Quant Energy has received your Quote Request", email2,
                                          'joelmathew.clix@gmail.com', [user_email])
            msg2.content_subtype = "html"
            msg2.send()
            serializer.is_valid(raise_exception=True)
            return Response({"Created": "User Created successfully"}, status=HTTP_201_CREATED)
        else:
            serializer.is_valid(raise_exception=True)
            return Response({"Passwords": "Password and Confirm Password must match."}, status=HTTP_400_BAD_REQUEST)


class NotifyMeView(CreateAPIView):
    serializer_class = NotifyMeSerializer


class ContactusFormView(CreateAPIView):
    serializer_class = ContactUsFormSerializer


class SubscribeNowView(CreateAPIView):
    serializer_class = SubscribeNowSerializer
