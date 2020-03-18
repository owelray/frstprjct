from django.shortcuts import render
from .forms import UrlForm
from django.views.generic.base import View
from .models import Url
from django.http import HttpResponseRedirect
import hashlib

class MainView(View):
    def post(self, request):
        if request.method == "POST":
            form = UrlForm(request.POST)
            if form.is_valid():
                url = Url()
                url.long_url = request.POST.get('url')
                url.use_bitly = request.POST.get('shortening_method')
                if url.use_bitly == None:
                    url.use_bitly = False
                if url.use_bitly == "on":
                    url.use_bitly = True
                print(url.use_bitly)
                url.short_url = hashlib.md5(url.long_url.encode())
                url.short_url = url.short_url.hexdigest()[:8]
                url.save()
                return HttpResponseRedirect('/second_project')
            else:
                return HttpResponseRedirect('/')
    def get(self, request):
        form = UrlForm()
        return render(request, 'second_project/url_shortener.html', {'form': form})
