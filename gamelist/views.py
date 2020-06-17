from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse, Http404
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .forms import ReviewForm
from .models import GameReview
from .game_info_request import igdbapi_search, igdbapi_getinfo


class GameListView(ListView):
    model = GameReview
    context_object_name = 'reviews'
    template_name = 'gamelist/gamelist.html'
    queryset = GameReview.objects.filter(show_in_feed=True).order_by('-date')


class ProfileView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'gamelist/profile.html'

    def get_context_data(self, **kwargs):
        userinfo = User.objects.get(username=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['userinfo'] = User.objects.get(username=userinfo)
        context['likes'] = GameReview.objects.filter(likedone=userinfo.id)
        context['reviews'] = GameReview.objects.filter(reviewer_id=userinfo.id)
        return context


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
        redirect_to = request.GET.get('next', '')
        logout(request)
        return HttpResponseRedirect(redirect_to)


class SecretView(View):
    def get(self, request):
        return render(request, 'gamelist/nt.html')


def validate_form_checkbox(checkbox):
    if checkbox is None:
        checkbox = False
    if checkbox == "on":
        checkbox = True
    return checkbox


class AddReviewView(View):
    def post(self, request):
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                if request.user.is_authenticated:
                    game = GameReview()
                    game.title = request.POST.get("title")
                    if request.POST.get("game_api_id") != "":
                        # gets the new url of the game
                        game_api_info = igdbapi_getinfo(request.POST.get("game_api_id"))
                        game.game_url = game_api_info[0]["url"]
                    game.review = request.POST.get("review")
                    game.rating = request.POST.get("rating")
                    if game.rating is None:
                        game.rating = 0
                    game.show_in_feed = validate_form_checkbox(request.POST.get("feed"))
                    game.reviewer = request.user
                    game.save()
                    return HttpResponseRedirect("/gamelist/review/" + str(game.id))
                else:
                    return HttpResponseRedirect('/gamelist/nt/nt')
            else:
                return HttpResponseRedirect("/gamelist/nt/nt")

    def get(self, request):
        form = ReviewForm()
        return render(request, 'gamelist/add.html', {'form': form})


class EditGameReviewView(View):
    def get(self, request, review_id):
        try:
            review = GameReview.objects.get(id=review_id)
            current_user = request.user
            if request.user.is_authenticated and current_user.id == review.reviewer_id:
                form_data = {'title': review.title, 'review': review.review}
                form = ReviewForm(form_data)
                return render(request, 'gamelist/edit.html', {'form': form, 'review': review})
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
                        if review.title != request.POST.get("title"):
                            if request.POST.get("game_api_id") != "":
                                # also gets the new url of the game
                                game_api_info = igdbapi_getinfo(request.POST.get("game_api_id"))
                                review.game_url = game_api_info[0]["url"]
                            else:
                                review.game_url = None
                        review.title = request.POST.get("title")
                        review.review = request.POST.get("review")
                        review.rating = request.POST.get("rating")
                        if review.rating is None:
                            review.rating = 0
                        review.show_in_feed = validate_form_checkbox(request.POST.get("feed"))
                        review.reviewer = request.user
                        review.save()
                        return HttpResponseRedirect("/gamelist/review/" + str(review.id))
                    else:
                        return HttpResponseRedirect('/gamelist/nt/nt')
                else:
                    return HttpResponseRedirect("/gamelist/nt/nt")
            except GameReview.DoesNotExist:
                return HttpResponseNotFound('<h2>Review not found</h2>')


class AjaxSearchGameView(View):
    def get(self, request):
        if request.is_ajax():
            data = request.GET.get('data', None)
            # igdbapi_search() gets a json search_data and sorting it | more info in game_info_request.py
            response = {'results': igdbapi_search(data)}
            return JsonResponse(response)
        else:
            raise Http404


class RemoveGameUrlView(View):
    def get(self, request, review_id):
        try:
            review = GameReview.objects.get(id=review_id)
            current_user = request.user
            if request.user.is_authenticated and current_user.id == review.reviewer_id:
                review.game_url = None
                review.save()
                return HttpResponseRedirect('/gamelist/review/' + str(review_id))
            else:
                return HttpResponseRedirect('/gamelist/nt/nt')
        except GameReview.DoesNotExist:
            return HttpResponseNotFound('<h2>Review not found</h2>')


class DeleteGameReviewView(View):
    def get(self, request, review_id):
        try:
            review = GameReview.objects.get(id=review_id)
            current_user = request.user
            if request.user.is_authenticated and current_user.id == review.reviewer_id:
                review.delete()
                return HttpResponseRedirect('/gamelist/user/' + str(current_user.username))
            else:
                return HttpResponseRedirect("/gamelist/nt/nt")
        except GameReview.DoesNotExist:
            return HttpResponseNotFound('<h2>Review not found</h2>')


class LikeView(View):
    def get(self, request, add_id):
        try:
            review_item = GameReview.objects.get(id=add_id)
            user_tags = User.objects.filter(users_likes=add_id)
            current_user = request.user
            if request.user.is_authenticated:
                if current_user not in user_tags:
                    try:
                        review_item = GameReview.objects.get(id = add_id)
                        review_item.likedone.add(current_user)
                        review_item.save()
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    except ObjectDoesNotExist:
                        return HttpResponseRedirect("/gamelist")
                else:
                    try:
                        review_item = GameReview.objects.get(id=add_id)
                        review_item.likedone.remove(current_user)
                        review_item.save()
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    except ObjectDoesNotExist:
                        return HttpResponseRedirect("/gamelist")
            else:
                return HttpResponseRedirect("/gamelist/nt/nt")
        except GameReview.DoesNotExist:
            return HttpResponseNotFound('<h2>Review not found</h2>')



