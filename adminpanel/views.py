import csv

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView

from Quant import settings
from cms.forms import PostAdminForm
from cms.models import Post
from restapi.models import InquiryformModel, CustomUser, ContactUs, NotifyMe, SubscribeNow
from .forms import LoginForm

user = get_user_model()

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


class InquiryformListView(LoginRequiredMixin, View):
    model = InquiryformModel
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        formlist = InquiryformModel.objects.all()
        count = len(formlist)
        paginator = Paginator(formlist, 10)
        page = request.GET.get('page')
        formlist = paginator.get_page(page)
        context = {
            'formlist': formlist,
            'count': count
        }
        return render(self.request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        qs = self.request.POST.get('qs')
        if qs:
            search = InquiryformModel.objects.filter(Q(bussiness_name__icontains=qs) |
                                                     Q(full_name__icontains=qs) |
                                                     Q(email__icontains=qs) |
                                                     Q(zip__icontains=qs) |
                                                     Q(service_date__icontains=qs) |
                                                     Q(user_type__icontains=qs))

            search_count = len(search)
            context = {
                'search': search,
                'search_count': search_count
            }
            if search:
                messages.info(self.request, str(search_count) + ' matches found')
                return render(self.request, 'index.html', context)
            else:
                messages.info(self.request, 'No results found')
                return render(self.request, 'index.html', context)
        else:
            messages.info(self.request, 'Please enter some text  ')
            return redirect('adminpanel:form-list')


class Login(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm
        return render(self.request, 'login.html', {'form': form})

    def post(self, request):
        email = self.request.POST['email']
        password = self.request.POST['password']
        try:
            user_object = user.objects.get(email=email)
            if user_object.check_password(password):
                if user_object.is_superuser:
                    login(self.request, user_object)
                    messages.success(self.request, 'Logged in successfully')
                    return redirect('adminpanel:form-list')
                else:
                    messages.error(self.request, "You are not authorised")
                    return render(request, 'login.html')
            else:
                messages.error(self.request, "Incorrect Password")
                return render(request, 'login.html')
        except:
            messages.error(self.request, "Email doesn't exists")
            return render(self.request, 'login.html')


class InquiryFormDetails(LoginRequiredMixin, DetailView):
    model = InquiryformModel
    template_name = 'form-detail.html'


class InquiryFormDelete(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        request_kwargs = kwargs
        object_id = request_kwargs['pk']
        InquiryFormObject = InquiryformModel.objects.get(id=object_id)
        InquiryFormObject.delete()
        return HttpResponseRedirect('/adminpanel/inquiry-list/')


class InquiryFormDetailDownload(LoginRequiredMixin, View):
    model = InquiryformModel

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users-formdata.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['Bussiness Nname', 'Full Name', 'Email', 'Phone', 'Zip', 'Service Date', 'Amount Due', 'Due Date',
             'Total Usages', 'Electric Heat', 'Balanced Bill', 'Current Electricity Provider', 'User Type'])

        users = InquiryformModel.objects.filter(pk=self.kwargs.get('pk'))
        users_data = users.values_list('bussiness_name', 'full_name', 'email', 'phone', 'zip',
                                       'service_date', 'amount_due', 'due_date',
                                       'total_usages', 'electric_heat', 'balanced_bill',
                                       'current_electricity_provider', 'user_type')

        for user in users_data:
            writer.writerow(user)

        return response





class InquiryFormDetaillistDownload(LoginRequiredMixin, View):
    model = InquiryformModel

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users-formdata.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['Bussiness Nname', 'Full Name', 'Email', 'Phone', 'Zip', 'Service Date', 'Amount Due', 'Due Date',
             'Total Usages', 'Electric Heat', 'Balanced Bill', 'Current Electricity Provider', 'User Type'])

        users = InquiryformModel.objects.all().values_list('bussiness_name', 'full_name',
                                                           'email', 'phone', 'zip',
                                                           'service_date', 'amount_due',
                                                           'due_date',
                                                           'total_usages', 'electric_heat',
                                                           'balanced_bill',
                                                           'current_electricity_provider',
                                                           'user_type')
        for user in users:
            writer.writerow(user)

        return response


class PasswordResetConfirmView(View):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def get(self, request, *args, **kwargs):
        token = kwargs['token']
        user_id_b64 = kwargs['uidb64']
        uid = urlsafe_base64_decode(user_id_b64).decode()
        user_object = user.objects.get(id=uid)
        token_generator = default_token_generator
        if token_generator.check_token(user_object, token):
            return render(request, 'password_reset_confirm.html')
        else:
            messages.error(request, "Link is Invalid")
            return render(request, 'password_reset_confirm.html')

    def post(self, request, *args, **kwargs):

        token = kwargs['token']
        user_id_b64 = kwargs['uidb64']
        uid = urlsafe_base64_decode(user_id_b64).decode()
        user_object = user.objects.get(id=uid)
        token_generator = default_token_generator
        if not token_generator.check_token(user_object, token):
            messages.error(self.request, "Link is Invalid")
            return render(request, 'password_reset_confirm.html')

        password1 = self.request.POST.get('new_password1')
        password2 = self.request.POST.get('new_password2')

        if password1 != password2:
            messages.error(self.request, "Passwords do not match")
            return render(request, 'password_reset_confirm.html')
        elif len(password1) < 8:
            messages.error(self.request, "Password must be atleast 8 characters long")
            return render(request, 'password_reset_confirm.html')
        elif password1.isdigit() or password2.isdigit() or password1.isalpha() or password2.isalpha():
            messages.error(self.request, "Passwords must have a mix of numbers and characters")
            return render(request, 'password_reset_confirm.html')
        else:
            token = kwargs['token']
            user_id_b64 = kwargs['uidb64']
            uid = urlsafe_base64_decode(user_id_b64).decode()
            user_object = user.objects.get(id=uid)
            user_object.set_password(password1)
            user_object.save()
            return HttpResponseRedirect('/password-reset-complete/')


class PasswordResetView(View):
    template_name = 'password_reset.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'password_reset.html')

    def post(self, request, *args, **kwargs):
        user = get_user_model()
        email = request.POST.get('email')
        email_template = "password_reset_email.html"
        user_qs = user.objects.filter(email=email)
        if len(user_qs) == 0:
            messages.error(request, 'Email does not exists')
            return render(request, 'password_reset.html')

        elif len(user_qs) == 1:
            user_object = user_qs[0]
            email = user_object.email
            uid = urlsafe_base64_encode(force_bytes(user_object.id))
            token = default_token_generator.make_token(user_object)
            if request.is_secure():
                protocol = "https"
            else:
                protocol = "http"
            domain = request.META['HTTP_HOST']
            user = user_object
            site_name = "Quant Energy"

            context = {
                "email": email,
                "uid": uid,
                "token": token,
                "protocol": protocol,
                "domain": domain,
                "user": user,
                "site_name": site_name
            }
            subject = "Reset Password Link"
            email_body = render_to_string(email_template, context)
            send_mail(subject, email_body, DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            return redirect('/password-reset-done/')
        else:

            user_object = user_qs[0]
            email = user_object.email
            uid = urlsafe_base64_encode(force_bytes(user_object.id))
            token = default_token_generator.make_token(user_object)
            if request.is_secure():
                protocol = "https"
            else:
                protocol = "http"
            domain = request.META['HTTP_HOST']
            user = user_object
            site_name = "Quant Energy"

            context = {
                "email": email,
                "uid": uid,
                "token": token,
                "protocol": protocol,
                "domain": domain,
                "user": user,
                "site_name": site_name
            }

            subject = "Reset Password Link"
            email_body = render_to_string(email_template, context)
            send_mail(subject, email_body, DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            return redirect('/password-reset-done/')


class CustomUserView(LoginRequiredMixin, View):
    model = CustomUser
    template_name = 'customuser-list.html'

    def get(self, request, *args, **kwargs):
        userslist = CustomUser.objects.all()
        count = len(userslist)
        paginator = Paginator(userslist, 10)
        page = request.GET.get('page')
        userslist = paginator.get_page(page)
        context = {
            'userslist': userslist,
            'count': count
        }
        return render(self.request, 'customuser-list.html', context)

    def post(self, request, *args, **kwargs):
        qs = self.request.POST.get('qs')
        if qs:
            search = CustomUser.objects.filter(Q(first_name__icontains=qs) |
                                               Q(last_name__icontains=qs) |
                                               Q(email__icontains=qs) |
                                               Q(phone__icontains=qs) |
                                               Q(street__icontains=qs) |
                                               Q(city__icontains=qs) |
                                               Q(state__icontains=qs) |
                                               Q(zip__icontains=qs))

            search_count = len(search)
            context = {
                'search': search,
                'search_count': search_count
            }
            if search:
                messages.info(self.request, str(search_count) + ' matches found')
                return render(self.request, 'customuser-list.html', context)
            else:
                messages.info(self.request, 'No results found')
                return render(self.request, 'customuser-list.html', context)
        else:
            messages.info(self.request, 'Please enter some text  ')
            return redirect('adminpanel:customuser-list')


class CustomUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "customuser-detail.html"


class CustomUserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser

    def get(self, request, *args, **kwargs):
        request_kwargs = kwargs
        object_id = request_kwargs['pk']
        customuserObject = CustomUser.objects.get(id=object_id)
        customuserObject.delete()
        return HttpResponseRedirect('/adminpanel/customuser-list/')


class CustomUserDetailDownloadView(LoginRequiredMixin, View):
    model = CustomUser

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="formdata.csv"'
        writer = csv.writer(response)
        writer.writerow(['first_name', 'last_name', 'street', 'city', 'state', 'zip', 'phone', 'email',
                         'password'])
        users = CustomUser.objects.filter(pk=self.kwargs.get('pk'))
        users_data = users.values_list('first_name', 'last_name', 'street', 'city', 'state', 'zip', 'phone',
                                       'email',
                                       'password')
        for user in users_data:
            writer.writerow(user)
        return response


class CustomUserListDownloadView(LoginRequiredMixin, View):
    model = CustomUser

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user-formdata.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ['First Nname', 'Last Name', 'Address', 'Phone', 'Email', 'Password'])
        users = CustomUser.objects.all().values_list('first_name', 'last_name', 'address', 'phone', 'email',
                                                     'password')
        for user in users:
            writer.writerow(user)
        return response


class ContactusView(LoginRequiredMixin, ListView):
    model = ContactUs
    template_name = 'contactus-list.html'

    def get(self, request, *args, **kwargs):
        formlist = ContactUs.objects.all()
        count = len(formlist)
        paginator = Paginator(formlist, 10)
        page = request.GET.get('page')
        formlist = paginator.get_page(page)
        context = {
            'formlist': formlist,
            'count': count,
            # 'date_joined':date_joined
        }
        return render(self.request, 'contactus-list.html', context)

    def post(self, request, *args, **kwargs):
        qs = self.request.POST.get('qs')
        if qs:
            search = ContactUs.objects.filter(Q(first_name__icontains=qs) |
                                              Q(last_name__icontains=qs) |
                                              Q(email__icontains=qs) |
                                              Q(contact_number__icontains=qs) |
                                              Q(query_type__icontains=qs) |
                                              Q(message__icontains=qs))

            search_count = len(search)
            context = {
                'search': search,
                'search_count': search_count
            }
            if search:
                messages.info(self.request, str(search_count) + ' matches found')
                return render(self.request, 'contactus-list.html', context)
            else:
                messages.info(self.request, 'No results found')
                return render(self.request, 'contactus-list.html', context)
        else:
            messages.info(self.request, 'Please enter some text')
            return redirect('adminpanel:contactus-list')


class ContactusDetailDownloadView(LoginRequiredMixin, View):
    model = ContactUs

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="formdata.csv"'
        writer = csv.writer(response)
        writer.writerow(['first_name', 'last_name', 'email', 'contact_number', 'query_type', 'message',
                         'password'])
        users = ContactUs.objects.filter(pk=self.kwargs.get('pk'))
        users_data = users.values_list('first_name', 'last_name', 'email', 'contact_number', 'query_type',
                                       'message')
        for user in users_data:
            writer.writerow(user)
        return response


class ContactusListDownloadView(LoginRequiredMixin, View):
    model = ContactUs

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user-formdata.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ['first_name', 'last_name', 'email', 'contact_number', 'query_type', 'message',
             'password'])
        users = ContactUs.objects.all().values_list('first_name', 'last_name', 'email', 'contact_number',
                                                    'query_type',
                                                    'message', )
        for user in users:
            writer.writerow(user)
        return response


class ContactusDetailView(LoginRequiredMixin, DetailView):
    model = ContactUs
    template_name = 'contactus-detail.html'


class ContactusDeleteView(LoginRequiredMixin, DeleteView):
    model = ContactUs

    def get(self, request, *args, **kwargs):
        request_kwargs = kwargs
        object_id = request_kwargs['pk']
        contactusObject = ContactUs.objects.get(id=object_id)
        contactusObject.delete()
        return HttpResponseRedirect('/adminpanel/contactus-list/')


class NotifyMeView(LoginRequiredMixin, View):
    model = NotifyMe
    template_name = "notify-list.html"

    def get(self, request, *args, **kwargs):
        formlist = NotifyMe.objects.all()
        count = len(formlist)
        paginator = Paginator(formlist, 10)
        page = request.GET.get('page')
        formlist = paginator.get_page(page)
        context = {
            'formlist': formlist,
            'count': count
        }
        return render(self.request, 'notify-list.html', context)

    def post(self, request, *args, **kwargs):
        qs = self.request.POST.get('qs')
        if qs:
            search = NotifyMe.objects.filter(Q(first_name__icontains=qs) |
                                             Q(last_name__icontains=qs) |
                                             Q(email__icontains=qs) |
                                             Q(contact_no__icontains=qs) |
                                             Q(street__icontains=qs) |
                                             Q(city__icontains=qs) |
                                             Q(state__icontains=qs) |
                                             Q(zip__icontains=qs))

            search_count = len(search)
            context = {
                'search': search,
                'search_count': search_count
            }
            if search:
                messages.info(self.request, str(search_count) + ' matches found')
                return render(self.request, 'notify-list.html', context)
            else:
                messages.info(self.request, 'No results found')
                return render(self.request, 'notify-list.html', context)
        else:
            messages.info(self.request, 'Please enter some text')
            return redirect('adminpanel:notifyme-list')


class NotifyMeDetailDownloadView(LoginRequiredMixin, View):
    model = NotifyMe

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="formdata.csv"'
        writer = csv.writer(response)
        writer.writerow(['first_name', 'last_name', 'email', 'contact_no', 'address'])
        users = NotifyMe.objects.filter(pk=self.kwargs.get('pk'))
        users_data = users.values_list('first_name', 'last_name', 'email', 'contact_no', 'address')
        for user in users_data:
            writer.writerow(user)
        return response


class NotifyMeListDownloadView(LoginRequiredMixin, View):
    model = NotifyMe

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user-formdata.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ['first_name', 'last_name', 'email', 'contact_no', 'street', 'city', 'state', 'zip'])
        users = NotifyMe.objects.all().values_list('first_name', 'last_name', 'email', 'contact_no', 'street',
                                                   'city',
                                                   'state', 'zip')
        for user in users:
            writer.writerow(user)
        return response


class NotifyMeDetailView(LoginRequiredMixin, DetailView):
    model = NotifyMe
    template_name = "notify-detail.html"


class NotifyMeDeleteView(LoginRequiredMixin, DeleteView):
    model = NotifyMe

    def get(self, request, *args, **kwargs):
        request_kwargs = kwargs
        object_id = request_kwargs['pk']
        notifymeObject = NotifyMe.objects.get(id=object_id)
        notifymeObject.delete()
        return HttpResponseRedirect('/adminpanel/notifyme-list/')


class SubscribeView(LoginRequiredMixin, View):
    model = SubscribeNow
    template_name = 'subscribenow.html'

    def get(self, request, *args, **kwargs):
        formlist = SubscribeNow.objects.all()
        count = len(formlist)
        paginator = Paginator(formlist, 10)
        page = request.GET.get('page')
        formlist = paginator.get_page(page)
        context = {
            'formlist': formlist,
            'count': count
        }
        return render(self.request, 'subscribenow.html', context)

    def post(self, request, *args, **kwargs):
        qs = self.request.POST.get('qs')
        if qs:
            search = SubscribeNow.objects.filter(Q(email__icontains=qs))

            search_count = len(search)
            context = {
                'search': search,
                'search_count': search_count
            }
            if search:
                messages.info(self.request, str(search_count) + ' matches found')
                return render(self.request, 'subscribenow.html', context)
            else:
                messages.info(self.request, 'No results found')
                return render(self.request, 'subscribenow.html', context)
        else:
            messages.info(self.request, 'Please enter some text')
            return redirect("adminpanel:subscribenow")


class SubscribenowDeleteView(LoginRequiredMixin, DeleteView):
    model = SubscribeNow

    def get(self, request, *args, **kwargs):
        request_kwargs = kwargs
        object_id = request_kwargs['pk']
        subscribenowObject = SubscribeNow.objects.get(id=object_id)
        subscribenowObject.delete()
        return HttpResponseRedirect('/adminpanel/subscribenow/')


class SubscriberlistDownloadView(LoginRequiredMixin, View):
    model = SubscribeNow

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user-formdata.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ['email', 'created_at'])
        users = SubscribeNow.objects.all().values_list('email', 'created_at')
        for user in users:
            writer.writerow(user)
        return response


class CmsCreate(CreateView):
    model = Post
    form_class = PostAdminForm
    template_name = 'content-management.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request, 'Post created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CmsList(ListView):
    model = Post
    template_name = 'content-management.html'

    def get(self, request, *args, **kwargs):
        post = Post.objects.all()
        count = len(post)
        paginator = Paginator(post, 3)
        page = request.GET.get('page')
        post = paginator.get_page(page)

        context = {
            'post': post,
            'count': count,

        }
        return render(self.request, "content-management.html", context)


class CmsDetail(DetailView):
    model = Post
    template_name = 'content-detail.html'


class CmsUpdate(UpdateView):
    model = Post
    form_class = PostAdminForm
    template_name = 'postupdate.html'
    success_url = reverse_lazy('adminpanel:post-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.info(self.request, 'Post updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CmsDelete(DeleteView):
    model = Post
    template_name = 'content-management.html'
    success_url = reverse_lazy('adminpanel:post-list')







#     ('1', '4Change Energy'),
#     ('16', 'Acacia Energy'),
#     ('202', 'Agera Energy'),
#     ('2', 'Ambit Energy'),
#     ('2', 'Ambit Energy'),
#     ('18', 'American Light'),
#     ('72', 'Ameripower'),
#     ('3', 'Amigo Energy'),
#     ('3', 'Amigo Energy'),
#     ('5', 'AP Gas'),
#     ('198', 'Axon Power'),
#     ('7', 'Bounce Energy'),
#     ('9', 'Brilliant Energy'),
#     ('145', 'Brooklet Energy'),
#     ('11', 'Champion Energy Services'),
#     ('197', 'Chariot Energy'),
#     ('197', 'Chariot Energy'),
#     ('160', 'Circular Energy'),
#     ('160', 'Circular Energy'),
#     ('12', 'Cirro Energy'),
#     ('61', 'Clearview Energy'),
#     ('13', 'Compassion Energy'),
#     ('62', 'Conservice Energy'),
#     ('14', 'Constellation New Energy'),
#     ('15', 'CPL Retail Energy'),
#     ('17', 'Direct Energy'),
#     ('201', 'Discount Power (formerly Life Energy)'),
#     ('35', 'Discount Power (formerly Pennywise Power)'),
#     ('168', 'Eligo Energy'),
#     ('149', 'Energy Rewards'),
#     ('63', 'Enertrade Electric'),
#     ('21', 'Entrust Energy'),
#     ('22', 'Everything Energy'),
#     ('161', 'Express Energy'),
#     ('23', 'First Choice Power'),
#     ('169', 'Freepoint Energy Solutions'),
#     ('24', 'Frontier Utilities'),
#     ('200', 'G-Power Energy'),
#     ('59', 'Gexa Energy'),
#     ('199', 'Green Energy Exchange'),
#     ('25', 'Green Mountain Energy Company'),
#     ('170', 'Griddy Energy'),
#     ('196', 'GridPlus Energy'),
#     ('162', 'Hello Energy'),
#     ('171', 'Heritage Power'),
#     ('90', 'Hudson Energy Services'),
#     ('27', 'IGS Energy'),
#     ('28', 'Infinite Energy'),
#     ('150', 'Infuse Energy'),
#     ('29', 'Just Energy'),
#     ('96', 'Liberty Power Corp'),
#     ('163', 'LifeEnergy'),
#     ('156', 'MidAmerican Energy Services'),
#     ('102', 'MP2 Energy Texas'),
#     ('164', 'My Quest Energy'),
#     ('32', 'NEC Retail'),
#     ('33', 'New Leaf Energy'),
#     ('34', 'Our Energy'),
#     ('116', 'Payless Power'),
#     ('117', 'Penstar Power'),
#     ('166', 'Pogo Energy'),
#     ('122', 'Power Express'),
#     ('36', 'Power House Energy'),
#     ('125', 'Pronto Power'),
#     ('38', 'Reliant'),
#     ('157', 'Shyne Energy'),
#     ('39', 'Smart Prepaid Electric'),
#     ('40', 'Source Power & Gas'),
#     ('41', 'Southwest Power & Light'),
#     ('42', 'Spark Energy'),
#     ('43', 'StarTex Power'),
#     ('44', 'Stream Energy'),
#     ('45', 'Summer Energy'),
#     ('46', 'Tara Energy'),
#     ('188', 'Taylor Co-Op'),
#     ('146', 'Texans Energy'),
#     ('48', 'Texpo Energy'),
#     ('151', 'Think Energy'),
#     ('49', 'Trieagle Energy'),
#     ('51', 'Trusmart Energy'),
#     ('52', 'TXU Energy'),
#     ('53', 'V247 Power Corporation'),
#     ('152', 'Verde Energy'),
#     ('54', 'Veteran Energy'),
#     ('153', 'Viridian Energy'),
#     ('140', 'Vital Power'),
#     ('182', 'Windrose Energy'),
#     ('55', 'WTU Retail Energy'),
#     ('141', 'Xoom Energy Texas'),
#     ('57', 'YEP'),
#     ('58', 'ZIP Energy'),
#     ('189', 'Energy to Go'),
#     ('190', 'Lone Star Energy'),
#     ('191', 'New Power Texas'),
#     ('192', 'Power of Texas'),
#     ('193', 'PowerNext'),
#     ('194', 'Pulse Power'),
# ]
#
#
# class Elecdata(View):
#     model = ElectricityProvider
#
#     def get(self, *args, **kwargs):
#         for x in elec:
#             electricity_provider_code = x[0]
#             electricity_provider_name = x[1]
#             data = ElectricityProvider.objects.create(
#                 electricity_provider_code=electricity_provider_code,
#                 electricity_provider_name=electricity_provider_name)
#         return HttpResponse("printed successfully")



# class ImportCSVData(View):
#     model = NotifyMe
#
#     def get(self, request, *args, **kwargs):
#         with open('user-formdata (10).csv', 'r')as f:
#             csv_reader = csv.reader(f, delimiter=',')
#             next(f)
#             for row in csv_reader:
#                 print(row)
#                 data = NotifyMe.objects.create(
#                     first_name=row[0],
#                     last_name=row[1],
#                     email=row[2],
#                     contact_no=row[3],
#                     street=row[4],
#                     city=row[5],
#                     state=row[6],
#                     zip=row[7],
#                 )
#             return HttpResponse("Data Uploaded successfully")