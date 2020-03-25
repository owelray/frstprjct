from django.urls import path
from . import views


urlpatterns = [
        path('', views.MainView.as_view()),
        path('<hash>', views.RedirectView.as_view()),
        path('clear/<hash>', views.ClearStatsView.as_view()),
        path('delete/<hash>', views.DeleteUrlView.as_view())
]