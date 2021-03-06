from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
        path('', views.GameListView.as_view()),
        path('logout/', views.LogoutView.as_view()),
        path('register/', views.RegisterFormView.as_view()),
        path('login/', views.LoginFormView.as_view()),
        path('add/', views.AddReviewView.as_view()),
        path('remove_url/<int:review_id>/', views.RemoveGameUrlView.as_view()),
        path('edit/<int:review_id>/', views.EditGameReviewView.as_view()),
        path('delete/<int:review_id>/', views.DeleteGameReviewView.as_view()),
        path('review/<int:pk>/', views.ReviewView.as_view()),
        path('nt/nt', views.SecretView.as_view()),
        path('rate/<int:add_id>/', views.LikeView.as_view()),
        path('user/<slug:slug>/', views.ProfileView.as_view()),
        url(r'^ajax/search/$', views.AjaxSearchGameView.as_view()),
]
