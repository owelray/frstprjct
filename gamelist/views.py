from django.views.generic import DetailView
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
from .models import GameReview
from .game_info_request import igdbapi_search, igdbapi_getinfo


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

class AddReviewView(View):
    def post(self, request):
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                if request.user.is_authenticated:
                    game = GameReview()
                    game.title = request.POST.get("title")
                    game.review = request.POST.get("review")
                    game.rating = request.POST.get("rating")
                    if game.rating == None:
                        game.rating = 0
                    game.reviewer = request.user
                    game.save()
                    return HttpResponseRedirect("/gamelist/" + str(game.id) + "/definition")
                else:
                    return HttpResponseRedirect('/gamelist/nt')
            else:
                return HttpResponseRedirect("/gamelist/nt")
    def get(self, request):
        form = ReviewForm()
        return render(request, 'gamelist/add.html', {'form': form})

class ReviewView(DetailView):
    model = GameReview
    context_object_name = 'game'
    template_name = 'gamelist/review.html'

class SearchGameView(View):
    def get(self, request, id):
        game = GameReview.objects.get(id=id)
        current_user = request.user
        if request.user.is_authenticated and current_user.id == game.reviewer_id:
            results = igdbapi_search(game.title)
            return render(request, 'gamelist/game-definition.html', {'results': results, 'game': game})
        else:
            return HttpResponseRedirect("/gamelist/nt")

class DefiniteGameView(View):
    def get(self, request, game_id, review_id):
        review = GameReview.objects.get(id=review_id)
        current_user = request.user
        if request.user.is_authenticated and current_user.id == review.reviewer_id:
            game_info = igdbapi_getinfo(game_id)
            for game in game_info:
                review.title = game['name']
                review.game_url = game['url']
                review.save()
            return HttpResponseRedirect("/gamelist/" + str(review.id))
        else:
            return HttpResponseRedirect("/gamelist/nt")
