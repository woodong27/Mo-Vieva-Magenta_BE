from django.db import models
from django.conf import settings
from movies.models import Movie

# Create your models here.

# 영화이야기(자유), 영화후기, 모임모집, 모임후기
class ArticleTag(models.Model):
    tag=models.CharField(max_length=20)


class Article(models.Model):
    title=models.CharField(max_length=20)
    content=models.TextField()
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upvote_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvote_articles')
    downvote_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downvote_articles')
    isNotice=models.BooleanField(default=False)
    tag=models.ForeignKey(ArticleTag, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    

class ArticleComment(models.Model):
    content=models.CharField(max_length=200)
    article=models.ForeignKey(Article, on_delete=models.CASCADE)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upvote_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvote_articlecomments')
    downvote_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downvote_articlecomments')
    isSecret=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # replies=