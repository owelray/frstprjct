from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .forms import ReviewForm

def gamelist_main(request):
    return render (request, 'gamelist/gamelist.html')

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/gamelist/login"
    template_name = "gamelist/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "gamelist/login.html"
    success_url = '/gamelist/'

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
        return render(request, 'gamelist/add.html', {'form': form})

def test(request):
    return render(request, 'gamelist/test.html')