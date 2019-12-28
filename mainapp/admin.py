from django.contrib import admin
from second_project .models import Book

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'likenumber',)
admin.site.register(Book, ReviewAdmin)
