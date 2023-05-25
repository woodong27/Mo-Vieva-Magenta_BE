from rest_framework import serializers
from .models import Movie, MovieComment, Genre, Video
from django.contrib.auth import get_user_model


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields=('genreId', 'genreName')
        read_only_fields=('genreId', 'genreName')
   
   
class VideoSerilaizer(serializers.ModelSerializer):
    class Meta:
        model=Video
        fields=('key', 'videoType')
        read_only_fields=('key', 'videoType', 'movie')
 
 
class MovieCommentSerializer(serializers.ModelSerializer):
    class UserInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model=get_user_model()
            fields=('id', 'username')
            
    author=UserInfoSerializer(read_only=True)
    upvoteCnt=serializers.IntegerField(read_only=True, source='upvote_users.count')
    downvoteCnt=serializers.IntegerField(read_only=True, source='downvote_users.count')
    
    class Meta:
        model=MovieComment
        fields=('id', 'author', 'content', 'upvoteCnt', 'downvoteCnt', 'created_at', 'updated_at')
        read_only_fields=('created_at', 'updated_at')

 
class MovieSerializer(serializers.ModelSerializer):
    lovesCnt=serializers.IntegerField(read_only=True, source='love_users.count')
    likesCnt=serializers.IntegerField(read_only=True, source='like_users.count')
    hatesCnt=serializers.IntegerField(read_only=True, source='hate_users.count')
    genres=GenreSerializer(many=True, read_only=True)
    videos=VideoSerilaizer(many=True, read_only=True, source='video_set.all')
    moviecomments=MovieCommentSerializer(many=True, read_only=True, source='moviecomment_set.all')
    
    class Meta:
        model=Movie
        fields='__all__'
        read_only_fields=('love_users', 'like_users', 'hate_users')


class AddMovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Movie
        fields='__all__'


class AddMovieCdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Movie
        fields=('movieCd',)