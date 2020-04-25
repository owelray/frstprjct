from urllib.error import HTTPError
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .forms import ReviewForm
from .models import GameReview
from .game_info_request import igdbapi_search, igdbapi_getinfo

def validate_form_checkbox(checkbox):
    if checkbox == None:
        checkbox = False
    if checkbox == "on":
        checkbox = True
    return checkbox

class GameListView(ListView):
    model = GameReview
    context_object_name = 'reviews'
    template_name = 'gamelist/gamelist.html'
    queryset = GameReview.objects.filter(show_in_feed=True).order_by('-date')

class ProfileView(View):
    def get(self, request, user_name):
        try:
            userinfo = User.objects.get(username=user_name)
            likes = GameReview.objects.filter(likedone=userinfo.id)
            reviews = GameReview.objects.filter(reviewer_id=userinfo.id).order_by('-date')
            return render(request, 'gamelist/profile.html', {'userinfo': userinfo, 'reviews': reviews, 'likes': likes})
        except User.DoesNotExist:
            return HttpResponseNotFound('<h2>User not found</h2>')

class IDProfileView(View):
    def get(self, requets, user_id):
        try:
            userinfo = User.objects.get(id=user_id)
            return HttpResponseRedirect('/gamelist/' + str(userinfo.username))
        except User.DoesNotExist:
            return HttpResponseNotFound('<h2>User not found</h2>')

class ReviewView(DetailView):
    model = GameReview
    context_object_name = 'game'
    template_name = 'gamelist/review.html'

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
    success_url = "/gamelist"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        redirect_to = request.GET.get('next','')
        logout(request)
        return HttpResponseRedirect(redirect_to)

class SecretView(View):
    def get(self, request):
        return render(request, 'gamelist/nt.html')

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
                    game.show_in_feed = request.POST.get("feed")
                    game.show_in_feed = validate_form_checkbox(game.show_in_feed)
                    game.reviewer = request.user
                    game.save()
                    return HttpResponseRedirect("/gamelist/definition/" + str(game.id))
                else:
                    return HttpResponseRedirect('/gamelist/nt/nt')
            else:
                return HttpResponseRedirect("/gamelist/nt/nt")
    def get(self, request):
        form = ReviewForm()
        return render(request, 'gamelist/add.html', {'form': form})


class SearchGameView(View):
    def get(self, request, id):
        try:
            game = GameReview.objects.get(id=id)
            current_user = request.user
            if request.user.is_authenticated and current_user.id == game.reviewer_id:
                try:
                    results = igdbapi_search(game.title)
                    return render(request, 'gamelist/game-definition.html', {'results': results, 'game': game})
                except:
                    return render(request, 'gamelist/game-definition.html', {'game': game})
            else:
                return HttpResponseRedirect("/gamelist/nt/nt")
        except GameReview.DoesNotExist:
            return HttpResponseNotFound('<h2>Review not found</h2>')

class DefiniteGameView(View):
    def get(self, request, game_id, review_id):
        try:
            review = GameReview.objects.get(id=review_id)
            current_user = request.user
            if request.user.is_authenticated and current_user.id == review.reviewer_id:
                game_info = igdbapi_getinfo(game_id)
                for game in game_info:
                    review.title = game['name']
                    review.game_url = game['url']
                    review.save()
                return HttpResponseRedirect("/gamelist/review/" + str(review.id))
            else:
                return HttpResponseRedirect("/gamelist/nt/nt")
        except GameReview.DoesNotExist:
            return HttpResponseNotFound('<h2>Review not found</h2>')


class DeleteGameReviewView(View):
    def get(self, request, review_id):
        try:
            review = GameReview.objects.get(id=review_id)
            current_user = request.user
            if request.user.is_authenticated and current_user.id == review.reviewer_id:
                review.delete()
                return HttpResponseRedirect('/gamelist/' + str(current_user.username))
            else:
                return HttpResponseRedirect("/gamelist/nt/nt")
        except GameReview.DoesNotExist:
            return HttpResponseNotFound('<h2>Review not found</h2>')

class EditGameReviewView(View):
    def get(self, request, review_id):
        try:
            review = GameReview.objects.get(id=review_id)
            current_user = request.user
            if request.user.is_authenticated and current_user.id == review.reviewer_id:
                form_data = {'title': review.title, 'review': review.review}
                form = ReviewForm(form_data)
                return render(request, 'gamelist/edit.html', {'form':form, 'review':review})
            else:
                return render(request, 'gamelist/nt.html')
        except GameReview.DoesNotExist:
            return HttpResponseNotFound('<h2>Review not found</h2>')
    def post(self, request, review_id):
        if request.method == "POST":
            form = ReviewForm(request.POST)
            try:
                review = GameReview.objects.get(id=review_id)
                current_user = request.user
                if form.is_valid():
                    if request.user.is_authenticated and current_user.id == review.reviewer_id:
                        is_changed = 0
                        if review.title != request.POST.get("title"):
                            is_changed = 1
                            review.title = request.POST.get("title")
                        review.review = request.POST.get("review")
                        review.rating = request.POST.get("rating")
                        if review.rating == None:
                            review.rating = 0
                        review.show_in_feed = request.POST.get("feed")
                        review.show_in_feed = validate_form_checkbox(review.show_in_feed)
                        review.reviewer = request.user
                        review.save()
                        if is_changed == 1:
                            return HttpResponseRedirect("/gamelist/definition/" + str(review.id))
                        else:
                            return HttpResponseRedirect("/gamelist/review/" + str(review.id))
                    else:
                        return HttpResponseRedirect('/gamelist/nt/nt')
                else:
                    return HttpResponseRedirect("/gamelist/nt/nt")
            except GameReview.DoesNotExist:
                return HttpResponseNotFound('<h2>Review not found</h2>')

class LikeView(View):
    def get(self, request, add_id):
        try:
            review_item = GameReview.objects.get(id = add_id)
            user_tags = User.objects.filter(users_likes = add_id)
            current_user = request.user
            if request.user.is_authenticated:
                if current_user not in user_tags:
                    try:
                        review_item = GameReview.objects.get(id = add_id)
                        review_item.likenumber +=1
                        review_item.likedone.add(current_user)
                        review_item.save()
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    except ObjectDoesNotExist:
                        return HttpResponseRedirect("/gamelist")
                else:
                    try:
                        review_item = GameReview.objects.get(id=add_id)
                        review_item.likenumber -= 1
                        review_item.likedone.remove(current_user)
                        review_item.save()
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    except ObjectDoesNotExist:
                        return HttpResponseRedirect("/gamelist")
            else:
                return HttpResponseRedirect("/gamelist/nt/nt")
        except GameReview.DoesNotExist:
            return HttpResponseNotFound('<h2>Review not found</h2>')