from django.urls import path
from . import views

urlpatterns = [
        # path('', views.main),
        path('register/', views.RegisterFormView.as_view()),
        path('login/', views.LoginFormView.as_view()),
        path('', views.main),
        path('logout/', views.LogoutView.as_view()),
        path('add/logout/', views.LogoutView.as_view()),
        path('add/', views.add),
        path('add/create/', views.create)
]