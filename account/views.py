from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as account_login
from django.contrib.auth import logout as account_logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView
from django import forms
from django.conf import settings
from account.forms import UserForm, RegistrationForm


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))


def login(request):
    c = RequestContext(request)
    c.update(csrf(request))
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    next_page = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            account_login(request, user)
            return redirect(next_page)
        else:
            return HttpResponse("Your account has been disabled!", c)
    else:
        c['login_form'] = LoginForm()
        return render_to_response("account/login.html", c)


def logout(request):
    account_logout(request)
    return redirect('account.views.login')


def registration_success(request):
    c = RequestContext(request)
    return render_to_response("account/registration_success.html", c)


class UserView(UpdateView):

    form_class = UserForm
    model = User
    template_name = "account/user_form.html"
    success_url = "account.views.profile"

    def get_object(self, queryset=None):
        obj = User.objects.get(username=self.request.user)
        return obj

    def form_valid(self, form):
        if form.is_valid():
            # if password1 exists, change password, otherwise
            # leave it
            if form.cleaned_data['password1']:
                self.object = form.save(commit=False)
                self.object.set_password(form.cleaned_data['password1'])
            self.object.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class RegistrationView(CreateView):

    form_class = RegistrationForm
    model = User
    template_name = "account/registration_form.html"
    success_url = "account.views.registration_success"

    def get_object(self, queryset=None):
        obj = User.objects.get(username=self.request.user)
        return obj

    def form_valid(self, form):
        if form.is_valid():
            # if password1 exists, change password, otherwise
            # leave it
            if form.cleaned_data['password1']:
                self.object = form.save(commit=False)
                self.object.set_password(form.cleaned_data['password1'])
            self.object.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


profile = login_required(UserView.as_view())
registration = RegistrationView.as_view()
