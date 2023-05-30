from django.contrib import admin
from . models import Post,Comment
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','created','publish','updated','status']
    list_filter=['title','author','publish','created','updated']
    search_fields=['title','author__username']
    prepopulated_fields={'slug':('title',)}
    raw_id_fields=['author']
    date_hierarchy='publish'
    ordering=['-publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['post','name','email','body','created','active']
    list_filter=['name','created','post']
    search_fields=['name','post','body']
