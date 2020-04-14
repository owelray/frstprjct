from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.contrib.auth import forms


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    path('second_project/', include('second_project.urls')),
    path('gamelist/', include('gamelist.urls')),
]
