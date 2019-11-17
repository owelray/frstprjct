from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Person

def info(request):
    people = Person.objects.all()
    return render(request, "first_project.html", {"people": people})

def create(request):
    if request.method == "POST":
        person = Person()
        person.name = request.POST.get("name")
        person.age = request.POST.get("age")
        person.save()
    return HttpResponseRedirect("/first_project")


def edit(request, id):
    try:
        person = Person.objects.get(id=id)
        if request.method == "POST":
            person.name = request.POST.get("name")
            person.age = request.POST.get("age")
            person.save()
            return HttpResponseRedirect("/first_project")
        else:
            return render(request, "edit.html", {"person":person})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")

def delete(request, id):
    try:
        person = Person.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("/first_project/")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")
