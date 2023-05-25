from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Grade
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse
from .serializers import UserInfoSerializer
from movies.models import Genre
from movies.serializers import GenreSerializer
from django.contrib.auth import get_user_model

# Create your views here.
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def gradeChange(request, grade_pk):
    if request.method=='POST':
        grade=get_object_or_404(Grade, pk=grade_pk)
        user=request.user
        user.grade=grade
        user.save()
        
        context={
            'grade':user.grade.title,
        }
        return JsonResponse(context)
    

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def admin(request):
    user=request.user
    if user.isAdmin:
        user.isAdmin=False
    else:
        user.isAdmin=True
    user.save()
    
    context={
        'isAdmin': user.isAdmin
    }
    return JsonResponse(context)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def userInfo(request):
    user=request.user
    serializer=UserInfoSerializer(user)
    return Response(serializer.data)
    
    
@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET'])
def genres(request):
    user=request.user
    
    if request.method=='POST':
        user.like_genres.clear()
        like_genres=list(set(request.data['like_genres']))
        for genreId in like_genres:
            genre=Genre.objects.get(genreId=genreId)
            if not genre.genre_like_users.filter(pk=user.pk).exists():
                user.like_genres.add(genre)
        user.save()
        like_genres=user.like_genres.all()
        serializer=GenreSerializer(like_genres, many=True)
        return Response(serializer.data)

    elif request.method=='GET':
        like_genres=user.like_genres.all()
        serializer=GenreSerializer(like_genres, many=True)
        return Response(serializer.data)
    

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def follow(request, user_pk):
    me=request.user
    you=get_user_model().objects.get(pk=user_pk)
    if me!=you:
        if you.followers.filter(pk=me.pk).exists():
            you.followers.remove(me)
            isFollowed=False
        else:
            you.followers.add(me)
            isFollowed=True
        
        context={
            'isFollowed': isFollowed,
            'followersCnt': you.followers.count(),
            'followingsCnt': you.followings.count()
        }
        
        return Response(context)
    
    return ({'내가 나를 팔로우할 수는 없습니다'})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upload_profile_image(request):
    user=request.user
    user.profile_image=request.data['profile_image']
    user.save()
    serializer=UserInfoSerializer(user)
    return Response(serializer.data)
    
    
@api_view(['GET'])
def profile(request, user_pk):
    user=get_user_model().objects.get(pk=user_pk)
    serializer=UserInfoSerializer(user)
    return Response(serializer.data)