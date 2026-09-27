from django.contrib import admin
from . import models

@admin.register(models.Community)
class Community(admin.ModelAdmin):
    list_display = ['id','name','slug','created_by','description']


@admin.register(models.Membership)
class Membership(admin.ModelAdmin):
    list_display = ['id','user','community','role',]

@admin.register(models.Post)
class Post(admin.ModelAdmin):
    list_display = ['id','community','author','parent','title','slug']

@admin.register(models.Vote)
class Vote(admin.ModelAdmin):
    list_display = ['id', 'user','post']


@admin.register(models.Save)
class Save(admin.ModelAdmin):
    list_display = ['id','user','post']


@admin.register(models.Report)
class Report(admin.ModelAdmin):
    list_display = ['id','user','post','reason']





