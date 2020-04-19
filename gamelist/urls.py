from django.urls import path
from . import views

urlpatterns = [
        path('', views.gamelist_main),
        path('register/', views.RegisterFormView.as_view()),
        path('login/', views.LoginFormView.as_view()),
        path('logout/', views.LogoutView.as_view()),
        path('add/', views.AddView.as_view()),
        path('<int:id>/definition/', views.DefiniteGame.as_view())
]