from django.urls import path
from . import views

urlpatterns = [
        path('', views.GameListView.as_view()),
        path('register/', views.RegisterFormView.as_view()),
        path('login/', views.LoginFormView.as_view()),
        path('logout/', views.LogoutView.as_view()),
        path('add/', views.AddReviewView.as_view()),
        path('delete/<int:review_id>/', views.DeleteGameReviewView.as_view()),
        path('<int:pk>/', views.ReviewView.as_view()),
        path('definition/<int:id>/', views.SearchGameView.as_view()),
        path('definition/<int:review_id>/<int:game_id>/', views.DefiniteGameView.as_view())
]