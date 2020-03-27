from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpRequest, HttpResponseNotFound, HttpResponse

from .forms import UrlForm
from .models import Url, Visitor

from practice.local_settings import *

import hashlib, pyshorteners

HOST = 'localhost:8000/second_project/'

class MainView(View):
    def post(self, request):
        if request.method == "POST":
            form = UrlForm(request.POST)
            if form.is_valid():
                url = Url()
                url.use_bitly = request.POST.get('shortening_method')
                if url.use_bitly == None:
                    url.use_bitly = False
                if url.use_bitly == "on":
                    url.use_bitly = True
                url.creator = request.session.session_key
                url.long_url = request.POST.get('url')
                url.url_hash = hashlib.md5(url.long_url.encode())
                url.url_hash = url.url_hash.hexdigest()[:8]
                url_hash_exists = Url.objects.filter(url_hash=url.url_hash)
                while url_hash_exists:
                    url.url_hash = hashlib.md5(url.url_hash.encode())
                    url.url_hash = url.url_hash.hexdigest()[:8]
                    url_hash_exists = Url.objects.filter(url_hash=url.url_hash)
                    continue
                url.short_url = HOST + url.url_hash
                if url.use_bitly == True:
                    shortener = pyshorteners.Shortener(api_key=bitly_acces_token)
                    url.bitly_url = shortener.bitly.short('https://' + url.short_url)
                    url.bitly_url[:8]
                    url.save()
                url.save()
                return HttpResponseRedirect('/second_project')
            else:
                return HttpResponseRedirect('/second_project/nt')

    def get(self, request):
        request.session.save()
        current_user = request.session.session_key
        users_urls = Url.objects.filter(creator=current_user)
        form = UrlForm()
        return render(request, 'second_project/url_shortener.html', {'form': form, 'user': users_urls})

class RedirectView(View):
        def get(self, request, hash):
            try:
                visitor = Visitor()
                request.session.save()
                current_session_key = request.session.session_key
                url = Url.objects.get(url_hash=hash)
                visitor.url_id = url.id
                visitor_exist = Visitor.objects.filter(session_key=current_session_key, url_id=url.id)
                if visitor_exist:
                    pass
                else:
                    visitor.session_key = current_session_key
                    visitor.save()
                    url.unique_visitors += 1
                url.clicks_counter += 1
                url.save()
                url = url.long_url
                return HttpResponseRedirect(url)
            except Url.DoesNotExist:
                return HttpResponseNotFound('<h2>Url not found</h2>')

class ClearStatsView(View):
    def get(self, request, hash):
        try:
            current_session_key = request.session.session_key
            url = Url.objects.get(url_hash=hash)
            if current_session_key == url.creator:
                url.clicks_counter = 0
                url.unique_visitors = 0
                url.save()
                visitors = Visitor.objects.filter(url_id=url.id)
                visitors.delete()
                return HttpResponseRedirect('/second_project')
            else:
                return HttpResponseRedirect('/second_project/nt')
        except Url.DoesNotExist:
            return HttpResponseNotFound('<h2>Url not found</h2>')

class DeleteUrlView(View):
    def get(self, request, hash):
        try:
            current_session_key = request.session.session_key
            url = Url.objects.get(url_hash=hash)
            if current_session_key == url.creator:
                url.delete()
                return HttpResponseRedirect('/second_project')
            else:
                return HttpResponseRedirect('/second_project/nt')
        except Url.DoesNotExist:
            return HttpResponseNotFound('<h2>Url not found</h2>')

class SecretView(View):
    def get(self, request):
        return render(request, 'second_project/nt.html')


