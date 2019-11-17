from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.template.context_processors import request
from django.http.request import HttpRequest
# from django import forms

def main (request):
    return render(request, 'library.html')

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/second_project"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/second_project"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        redirect_to = request.GET.get('next','')
        logout(request)
        return HttpResponseRedirect(redirect_to)


