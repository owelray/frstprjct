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
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .forms import ReviewForm
# from django import forms

def main(request):
    books = Book.objects.all()
    return render(request, "second_project/library.html", {"books": books})

def review(request, id):
    book = Book.objects.get(id=id)
    return render(request, "second_project/review.html", {"book": book})

def profile(request, id):
    userinfo = User.objects.get(id=id)
    likes = Book.objects.filter(likedone=id)
    books = Book.objects.filter(reviewer_id=id)
    return render(request, "second_project/profile.html", {"userinfo": userinfo, "books": books, "likes": likes})

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

def add(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            book = Book()
            book.title = request.POST.get("title")
            book.author = request.POST.get("author")
            book.review = request.POST.get("review")
            book.reviewer = request.user
            book.save()
            return HttpResponseRedirect("/second_project")
        else:
            return HttpResponseRedirect("/second_project/nt")
    else:
        form = ReviewForm()
    return render(request, 'second_project/add.html', {'form': form})

def nt(request):
    return render(request, 'second_project/nt.html')

def reviewlike(request, add_id):
    book_item = Book.objects.get(id = add_id)
    user_tags = User.objects.filter(users_likes = add_id)
    current_user = request.user
    if current_user not in user_tags:
        try:
            book_item = Book.objects.get(id = add_id)
            book_item.likenumber +=1
            book_item.likedone.add(current_user)
            book_item.save()
            return HttpResponseRedirect("/second_project/")
        except ObjectDoesNotExist:
            return HttpResponseRedirect("/second_project")
    else:
        return HttpResponseRedirect("/second_project")

