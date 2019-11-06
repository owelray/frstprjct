from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Person

def index(request):
    return render(request, "index.html")

def info(request):
    people = Person.objects.all()
    return render(request, "first_project.html", {"people": people})

def create(request):
    if request.method == "POST":
        person = Person()
        person.name = request.POST.get("name")
        person.age = request.POST.get("age")
        person.save()
    return HttpResponseRedirect("/")