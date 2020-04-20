from django.urls import path
from . import views

urlpatterns = [
        path('', views.gamelist_main),
        path('register/', views.RegisterFormView.as_view()),
        path('login/', views.LoginFormView.as_view()),
        path('logout/', views.LogoutView.as_view()),
        path('add/', views.AddReviewView.as_view()),
        path('<int:pk>/', views.ReviewView.as_view()),
        path('<int:id>/definition/', views.SearchGameView.as_view()),
        path('<int:review_id>/definition/<int:game_id>/', views.DefiniteGameView.as_view())
]