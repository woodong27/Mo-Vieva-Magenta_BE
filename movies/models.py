from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    genreId=models.IntegerField()
    genreName=models.CharField(max_length=20)
    description=models.CharField(max_length=50, null=True)
    

class Movie(models.Model):
    movieId=models.IntegerField()
    # movieCd를 받는 url필요
    movieCd=models.IntegerField(null=True)
    title=models.CharField(max_length=100)
    overview=models.TextField()
    poster_path=models.CharField(max_length=200, null=True)
    backdrop_path=models.CharField(max_length=200, null=True)
    popularity=models.FloatField(null=True)
    release_date=models.CharField(null=True, max_length=20)
    vote_average=models.FloatField(null=True)
    vote_count=models.IntegerField(null=True)
    genres=models.ManyToManyField(Genre, related_name='genre_movies')
    
    # 좋아요/싫어요
    love_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='love_movies')
    like_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    hate_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='hate_movies')
    

# 영어, 한글, official=True, site=Youtube 인 것의 key, videoType을 저장
class Video(models.Model):
    key=models.CharField(max_length=200)
    videoType=models.CharField(max_length=20)
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE)


class KeyWord(models.Model):
    keywordId=models.IntegerField()
    keywordName=models.CharField(max_length=50)
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE)

  
class MovieComment(models.Model):
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE)
    content=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upvote_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvote_moviecomments')
    downvote_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downvote_moviecomments')