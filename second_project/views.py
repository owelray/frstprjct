from django.shortcuts import render
from .forms import UrlForm
from django.views.generic.base import View
from .models import Url
from django.http import HttpResponseRedirect, HttpRequest
import hashlib

HOST = 'localhost:8000/second_project/'

class MainView(View):
    def post(self, request):
        if request.method == "POST":
            form = UrlForm(request.POST)
            if form.is_valid():
                url = Url()
                url.creator = request.session.session_key
                url.long_url = request.POST.get('url')
                url.use_bitly = request.POST.get('shortening_method')
                if url.use_bitly == None:
                    url.use_bitly = False
                if url.use_bitly == "on":
                    url.use_bitly = True
                url.url_hash = hashlib.md5(url.long_url.encode())
                url.url_hash = url.url_hash.hexdigest()[:8]
                url_hash_exists = Url.objects.filter(url_hash=url.url_hash)
                while url_hash_exists:
                    url.url_hash = hashlib.md5(url.url_hash.encode())
                    url.url_hash = url.url_hash.hexdigest()[:8]
                    url_hash_exists = Url.objects.filter(url_hash=url.url_hash)
                    continue
                url.short_url = HOST + url.url_hash
                url.save()
                return HttpResponseRedirect('/second_project')
            else:
                return HttpResponseRedirect('/')
    def get(self, request):
        request.session.save()
        current_user = request.session.session_key
        users_urls = Url.objects.filter(creator=current_user)
        form = UrlForm()
        return render(request, 'second_project/url_shortener.html', {'form': form, 'user': users_urls})
