from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.template.context_processors import request
from .models import Book
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .forms import ReviewForm

class MainView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'first_project/library.html'

class ReviewView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'first_project/review.html'

class ProfileView(View):
    def get(self, request, id):
        userinfo = User.objects.get(id=id)
        likes = Book.objects.filter(likedone=id)
        books = Book.objects.filter(reviewer_id=id)
        return render(request, 'first_project/profile.html', {'userinfo': userinfo, 'books': books, 'likes': likes})

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/first_project/login"
    template_name = "first_project/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "first_project/login.html"
    success_url = '/first_project/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        redirect_to = request.GET.get('next','')
        logout(request)
        return HttpResponseRedirect(redirect_to)

class AddView(View):
    def post(self, request):
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                if request.user.is_authenticated:
                    book = Book()
                    book.title = request.POST.get("title")
                    book.author = request.POST.get("author")
                    book.review = request.POST.get("review")
                    book.reviewer = request.user
                    book.save()
                    return HttpResponseRedirect("/first_project")
                else:
                    return HttpResponseRedirect('/first_project/nt')
            else:
                return HttpResponseRedirect("/first_project/nt")
    def get(self, request):
        form = ReviewForm()
        return render(request, 'first_project/add.html', {'form': form})

class SecretView(View):
    def get(self, request):
        return render(request, 'first_project/nt.html')

class LikeView(View):
    def get(self, request, add_id):
        book_item = Book.objects.get(id = add_id)
        user_tags = User.objects.filter(users_likes = add_id)
        current_user = request.user
        if request.user.is_authenticated:
            if current_user not in user_tags:
                try:
                    book_item = Book.objects.get(id = add_id)
                    book_item.likenumber +=1
                    book_item.likedone.add(current_user)
                    book_item.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except ObjectDoesNotExist:
                    return HttpResponseRedirect("/first_project")
            else:
                try:
                    book_item = Book.objects.get(id=add_id)
                    book_item.likenumber -= 1
                    book_item.likedone.remove(current_user)
                    book_item.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except ObjectDoesNotExist:
                    return HttpResponseRedirect("/first_project")
        else:
            return HttpResponseRedirect("/first_project/nt")


