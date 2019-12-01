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
from .models import Book
# from django import forms

def main(request):
    books = Book.objects.all()
    return render(request, "second_project/library.html", {"books": books})

def review(request, id):
    books = Book.objects.get(id=id)
    return render(request, "second_project/review.html", {"books": books})

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/second_project"
    template_name = "second_project/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "second_project/login.html"
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

def create(request):
    if request.method == "POST":
        book = Book()
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.review = request.POST.get("review")
        book.reviewer = request.user
        book.save()
    return HttpResponseRedirect("/second_project")

def add(request):
    books = Book.objects.all()
    return render(request, "second_project/add.html", {"books": books})