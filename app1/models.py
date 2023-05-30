from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT='Df','Draft'
        PUBLISHED='pb','Published'
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250,unique=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts',default=None, null=True)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    objects=models.Manager()
    published=PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering=['-publish']
        indexes=[models.Index(fields=['-publish'])]
    def get_absolute_url(self):
        return reverse("app1:post_details", args=[self.slug,self.id])
    


    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=25)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=['created']
    def __str__(self):
        return f'comment by {self.name}'
    
        

    
