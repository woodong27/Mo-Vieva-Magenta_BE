from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Grade, User
from django.conf import settings
from movies.models import Movie, MovieComment, Genre
from communities.models import Article, ArticleComment


class GradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Grade
        fields='__all__'
    

class UserInfoSerializer(serializers.ModelSerializer):
    
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model=Movie
            fields=('movieId', 'movieCd', 'title', 'genres', 'popularity')
            
    class ArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model=Article
            fields=('id', 'title', 'tag')
            
    class FollowerSerializer(serializers.ModelSerializer):
        class Meta:
            model=get_user_model()
            fields=('id', 'username')
            
    class MovieCommentSerializer(serializers.ModelSerializer):
        class Meta:
            model=MovieComment
            fields=('id', 'content')
            
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model=Genre
            fields=('genreId', 'genreName')
    
    
    love_movies=MovieSerializer(read_only=True, many=True)
    like_movies=MovieSerializer(read_only=True, many=True)
    hate_movies=MovieSerializer(read_only=True, many=True)
    # love_movies_count=serializers.IntegerField(read_only=True, source='love_movies.count')
    articles=ArticleSerializer(read_only=True, many=True, source='article_set.all')
    followers=FollowerSerializer(read_only=True, many=True)
    moviecomments=MovieCommentSerializer(many=True, source='moviecomment_set.all')
    like_genres=GenreSerializer(many=True)
    
    class Meta:
        model=get_user_model()
        # fields='__all__'
        fields=('id', 'username', 'isAdmin', 'grade', 'love_movies', 'like_movies', 'hate_movies',
                'articles', 'moviecomments','last_login', 'date_joined', 'followings', 'followers', 'like_genres', 'profile_image')