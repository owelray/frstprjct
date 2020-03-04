from django.urls import path
from . import views

urlpatterns = [
        path('', views.MainView.as_view()),
        path('register/', views.RegisterFormView.as_view()),
        path('login/', views.LoginFormView.as_view()),
        path('logout/', views.LogoutView.as_view()),
        path('user/<int:id>/', views.ProfileView.as_view()),
        path('nt', views.SecretView.as_view()),
        path('add/', views.AddView.as_view()),
        path('add/logout/', views.LogoutView.as_view()),
        path('review/<int:pk>/', views.ReviewView.as_view()),
        path('rate/<int:add_id>/', views.LikeView.as_view()),
]