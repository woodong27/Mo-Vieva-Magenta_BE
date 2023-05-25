from rest_framework import serializers
from .models import ArticleTag,Article, ArticleComment
from django.contrib.auth import get_user_model
from movies.models import Movie, Genre


class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model=ArticleTag
        fields='__all__'


class UserInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model=get_user_model()
            fields=('pk', 'username')

class ArticleCommentSerializer(serializers.ModelSerializer):
      
    class ArticleAuthorSerializer(serializers.ModelSerializer):
        author=UserInfoSerializer(read_only=True)
        
        class Meta:
            model=Article
            fields=('pk', 'author')
         
    author=UserInfoSerializer(read_only=True)
    article=ArticleAuthorSerializer(read_only=True)
    
    class Meta:
        model=ArticleComment
        fields='__all__'
        read_only_fields=('article', 'author', 'upvote_users', 'downvote_users')      
        
      

class GenreSerializer(serializers.ModelSerializer):
    
        class Meta:
            model=Genre
            fields=('genreId', 'genreName')

class ArticleSerializer(serializers.ModelSerializer):
    
    class MovieSerializer(serializers.ModelSerializer):
        genres=GenreSerializer(many=True, read_only=True)
        
        class Meta:
            model=Movie
            fields=('pk','title' ,'movieId', 'movieCd', 'genres')
            
    class AuthorSerializer(serializers.ModelSerializer):
        class Meta:
            model=get_user_model()
            fields=('pk', 'username')
    
    commentCnt=serializers.IntegerField(read_only=True, source='articlecomment_set.count')
    articlecomments=ArticleCommentSerializer(read_only=True, many=True, source='articlecomment_set.all')
    movie=MovieSerializer(read_only=True)
    author=AuthorSerializer(read_only=True)
    
    class Meta:
        model=Article
        fields='__all__'
        read_only_fields=('author', 'tag', 'upvote_users', 'downvote_users')
        

class ArticleUpdateSerializer(serializers.ModelSerializer):
    commentCnt=serializers.IntegerField(read_only=True, source='articlecomment_set.count')
    articlecomments=ArticleCommentSerializer(read_only=True, many=True, source='articlecomment_set.all')
    
    class Meta:
        model=Article
        fields='__all__'
        read_only_fields=('author', 'tag', 'upvote_users', 'downvote_users')


# 해당 태그가 달린 모든 게시물 가져오는 serializer
class TagArticleSerializer(serializers.ModelSerializer):
    commentCnt=serializers.IntegerField(read_only=True, source='articlecomment_set.count')
    articlecomments=ArticleCommentSerializer(read_only=True, many=True, source='articlecomment_set.all')
    
    class Meta:
        model=Article
        fields='__all__'


class MovieReviewSerializer(serializers.ModelSerializer):
    # upvoteCnt=serializers.IntegerField(read_only=True, source='upvote_users.count')
    # downvoteCnt=serializers.IntegerField(read_only=True, source='downvote_users.count')
    commentCnt=serializers.IntegerField(read_only=True, source='articlecomment_set.count')
    articlecomments=ArticleCommentSerializer(read_only=True, many=True, source='articlecomment_set.all')
    
    class Meta:
        model=Article
        fields='__all__'
        read_only_fields=('upvote_users', 'downvote_users', 'author', 'tag')


class NoticeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Article
        fields='__all__'
        read_only_fields=('author', 'tag', 'upvote_users', 'downvote_users')