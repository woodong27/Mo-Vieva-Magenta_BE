from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import  Movie, MovieComment, Genre, Video, KeyWord
from .serializers import MovieSerializer, MovieCommentSerializer, AddMovieCdSerializer, GenreSerializer, AddMovieSerializer
import requests
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user


TMDB_TRENDING='https://api.themoviedb.org/3/trending/movie/day'
params={
    'api_key' : settings.TMDB_KEY,
    'language' : 'ko-kr',
    'region' : 'KR',
    }

TMDB_GENRES='https://api.themoviedb.org/3/genre/movie/list'
# DataBase 초기 설정을 위해 Genre들과 영화 목록을 가져와서 DB에 저장해주기 위한 함수들

# https://api.themoviedb.org/3/movie/:movie_id/videos?api_key=
TMDB='https://api.themoviedb.org/3/movie/'

# Create your views here.
# @api_view(['POST'])
# def getGenres(request):
#     response=requests.get(TMDB_GENRES, params=params).json()
#     print(response)
#     for genre in response['genres']:
#         Genre.objects.create(
#             genreId=genre['id'],
#             genreName=genre['name']
#         )
    
#     return JsonResponse(response['genres'], safe=False)
    # return Response({'됐나'})


# @api_view(['POST'])
# def initializingDB(request):
#     result=[]
#     params['page']=1
#     response=requests.get(TMDB_TRENDING, params=params).json()
#     pages=response['total_pages']
#     for page in range(1,pages+1):
#         params['page']=page
#         response=requests.get(TMDB_TRENDING, params=params).json()
#         result.extend(response['results'])
        
#     for movie in result:
#         saving=Movie.objects.create(
#             movieId=movie['id'],
#             title=movie['title'],
#             overview=movie['overview'],
#             popularity=movie['popularity'],
#             release_date=movie['release_date'],
#             vote_average=movie['vote_average'],
#             vote_count=movie['vote_count'],
#             poster_path=movie['poster_path'],
#             backdrop_path=movie['backdrop_path'],
#         )
#         if movie['genre_ids']:
#             for id in movie['genre_ids']:
#                 genre=Genre.objects.get(genreId=id)
#                 # genre=get_object_or_404(Genre, genreId=id)
#                 saving.genres.add(genre)

#         response=requests.get(f'{TMDB}/{movie["id"]}/videos?api_key={settings.TMDB_KEY}').json()
#         if 'results' in response.keys():
#             videos=response['results']
#             for video in videos:
#                 if (video['iso_639_1']=='en' or video['iso_639_1']=='ko') and video['site']=='YouTube' and video['official'] and (video['type']=='Teaser' or video['type']=='Trailer'):
#                     Video.objects.create(
#                         key=video['key'],
#                         videoType=video['type'],
#                         movie=saving
#                     )
        
#         response=requests.get(f'{TMDB}/{movie["id"]}/keywords?api_key={settings.TMDB_KEY}').json()
#         if 'keywords' in response.keys():
#             keywords=response['keywords']
#             for keyword in keywords:
#                 KeyWord.objects.create(
#                     keywordId=keyword['id'],
#                     keywordName=keyword['name'],
#                     movie=saving
#                 )
        
#     return Response({'default' : 'created'})


@api_view(['GET'])
def movies(request):
    page=1
    if 'page' in request.GET.keys():
        page=int(request.GET['page'])
    
    per_page=40
    if 'per_page' in request.GET.keys():
        per_page=int(request.GET['per_page'])
        
    total_page=Movie.objects.count()//per_page+1
    
    if 'genreId' in request.GET.keys():
        genre=Genre.objects.get(genreId=int(request.GET['genreId']))
        movies=genre.genre_movies.all()[(page-1)*per_page:page*per_page]
        serializer=MovieSerializer(movies, many=True)
        serializer.data[0]['total_page']=total_page
        return Response(serializer.data)

    else:
        movies=Movie.objects.all()[(page-1)*per_page:page*per_page]
        serializer=MovieSerializer(movies,many=True)
        serializer.data[0]['total_page']=total_page
        return Response(serializer.data)


# @api_view(['POST'])
# def addMovie(request, movieId):
#     movie=requests.get(f'{TMDB}/{movieId}', params=params).json()
#     saving=Movie.objects.create(
#         movieId=movie['id'],
#         title=movie['title'],
#         overview=movie['overview'],
#         popularity=movie['popularity'],
#         release_date=movie['release_date'],
#         vote_average=movie['vote_average'],
#         vote_count=movie['vote_count'],
#         poster_path=movie['poster_path'],
#         backdrop_path=movie['backdrop_path']
#     )
    
#     if "genres" in movie.keys():
#         for kind in movie["genres"]:
#             genre=Genre.objects.get(genreId=kind['id'])
#             saving.genres.add(genre)
    
#     videos=requests.get(f'{TMDB}/{movie["id"]}/videos?api_key={settings.TMDB_KEY}').json()['results']
#     for video in videos:
#         if (video['iso_639_1']=='en' or video['iso_639_1']=='ko') and video['site']=='YouTube' and video['official'] and (video['type']=='Teaser' or video['type']=='Trailer'):
#                 Video.objects.create(
#                     key=video['key'],
#                     videoType=video['type'],
#                     movie=saving
#                 )
    
#     keywords=requests.get(f'{TMDB}/{movie["id"]}/keywords?api_key={settings.TMDB_KEY}').json()['keywords']
#     for keyword in keywords:
#             KeyWord.objects.create(
#                 keywordId=keyword['id'],
#                 keywordName=keyword['name'],
#                 movie=saving
#             )
    
#     serializer=MovieSerializer(saving)
#     return Response(serializer.data)


@api_view(['GET'])
def movieID(request, movie_id):
    try:
        movie=get_object_or_404(Movie, movieId=movie_id)
        serializer=MovieSerializer(movie)
        return Response(serializer.data)
    except:
        movie=requests.get(f'{TMDB}/{movie_id}', params=params).json()
        saving=Movie.objects.create(
            movieId=movie['id'],
            title=movie['title'],
            overview=movie['overview'],
            popularity=movie['popularity'],
            release_date=movie['release_date'],
            vote_average=movie['vote_average'],
            vote_count=movie['vote_count'],
            poster_path=movie['poster_path'],
            backdrop_path=movie['backdrop_path']
        )
        
        if "genres" in movie.keys():
            for kind in movie["genres"]:
                genre=Genre.objects.get(genreId=kind['id'])
                saving.genres.add(genre)
        
        videos=requests.get(f'{TMDB}/{movie["id"]}/videos?api_key={settings.TMDB_KEY}').json()['results']
        for video in videos:
            if (video['iso_639_1']=='en' or video['iso_639_1']=='ko') and video['site']=='YouTube' and video['official'] and (video['type']=='Teaser' or video['type']=='Trailer'):
                    Video.objects.create(
                        key=video['key'],
                        videoType=video['type'],
                        movie=saving
                    )
        
        keywords=requests.get(f'{TMDB}/{movie["id"]}/keywords?api_key={settings.TMDB_KEY}').json()['keywords']
        for keyword in keywords:
                KeyWord.objects.create(
                    keywordId=keyword['id'],
                    keywordName=keyword['name'],
                    movie=saving
                )
        
        serializer=MovieSerializer(saving)
        return Response(serializer.data)
        
    
@api_view(['GET'])
def moviePK(request, movie_pk):
    try:
        movie=Movie.objects.get(pk=movie_pk)
        serializer=MovieSerializer(movie)
        return Response(serializer.data)
    except:
        return Response([])
    
    
@api_view(['GET'])
def movieCD(request, movieCd):
    try:
        movie=Movie.objects.get(movieCd=movieCd)
        serializer=MovieSerializer(movie)
        return Response(serializer.data)
    except:
        return Response([])


# moviecomment 작성하는 메서드
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def idmoviecomments(request, movieId):
    movie=get_object_or_404(Movie, movieId=movieId)
    # movie_id 영화에 달린 moviecomment 작성하기
    if request.method=='POST':
        serializer=MovieCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, movie=movie)
            moviecomments=MovieComment.objects.all()
            serializer=MovieCommentSerializer(moviecomments, many=True)
            return Response(serializer.data)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    # movie_id 영화의 moviecomments 가져오기
    elif request.method=='GET':
        moviecomments=movie.moviecomment_set.all()
        serializer=MovieCommentSerializer(moviecomments, many=True)
        return Response(serializer.data)
    

@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def cdmoviecomments(request, movieCd):
    movie=get_object_or_404(Movie, movieCd=movieCd)
    # movie_id 영화에 달린 moviecomment 작성하기
    if request.method=='POST':
        serializer=MovieCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, movie=movie)
            moviecomments=MovieComment.objects.all()
            serializer=MovieCommentSerializer(moviecomments, many=True)
            return Response(serializer.data)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    # movie_id 영화의 moviecomments 가져오기
    elif request.method=='GET':
        moviecomments=movie.moviecomment_set.all()
        serializer=MovieCommentSerializer(moviecomments, many=True)
        return Response(serializer.data)
    

@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def pkmoviecomments(request, movie_pk):
    movie=get_object_or_404(Movie, pk=movie_pk)
    # movie_id 영화에 달린 moviecomment 작성하기
    if request.method=='POST':
        serializer=MovieCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, movie=movie)
            moviecomments=MovieComment.objects.all()
            serializer=MovieCommentSerializer(moviecomments, many=True)
            return Response(serializer.data)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    # movie_id 영화의 moviecomments 가져오기
    elif request.method=='GET':
        moviecomments=movie.moviecomment_set.all()
        serializer=MovieCommentSerializer(moviecomments, many=True)
        return Response(serializer.data)
        

@permission_classes([IsAuthenticated])
@api_view(['DELETE', 'PUT', 'GET'])
def moviecomment(request, moviecomment_pk):
    moviecomment=get_object_or_404(MovieComment, pk=moviecomment_pk)
    # moviecomment 수정
    if request.method=='PUT':
        if request.user==moviecomment.author:
            serializer=MovieCommentSerializer(moviecomment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            return JsonResponse({'error': '댓글 작성자가 아님'})
    
    # moviecomment 삭제
    elif request.method=='DELETE':
        if request.user==moviecomment.author:
            moviecomment.delete()
            return Response({'detail': f'{moviecomment_pk}번째 moviecomment 삭제되었음'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'error':'댓글 작성자가 아님'})
    
    elif request.method=='GET':
        serializer=MovieCommentSerializer(moviecomment)
        return Response(serializer.data)
    
    
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upvote(request, moviecomment_pk):
    moviecomment=get_object_or_404(MovieComment, pk=moviecomment_pk)
    
    # 1. downvote 투표한 유저가 upvote버튼을 누르면 downvote를 취소하고 upvote 해줌
    isDownvoted=False
    if moviecomment.downvote_users.filter(pk=request.user.pk).exists():
        moviecomment.downvote_users.remove(request.user)
        moviecomment.upvote_users.add(request.user)
        isUpvoted=True
    
    # 2. downvote 안한 유저가 upvote누를 시 토글
    else:
        if moviecomment.upvote_users.filter(pk=request.user.pk).exists():
            moviecomment.upvote_users.remove(request.user)
            isUpvoted=False
        else:
            moviecomment.upvote_users.add(request.user)
            isUpvoted=True
    
    context={
        'isUpvoted': isUpvoted,
        'isDownvoted': isDownvoted,
        'upvoteCnt': moviecomment.upvote_users.count(),
        'downvoteCnt': moviecomment.downvote_users.count()
    }
    return JsonResponse(context)
    

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def downvote(request, moviecomment_pk):
    moviecomment=get_object_or_404(MovieComment, pk=moviecomment_pk)
    
    # 1. upvote한 유저가 downvote누를 시 upvote취소하고  downvote 해줌
    isUpvoted=False
    if moviecomment.upvote_users.filter(pk=request.user.pk).exists():
        moviecomment.upvote_users.remove(request.user)
        moviecomment.downvote_users.add(request.user)
        isDownvoted=True
    
    # 2. upvote안한 유저가 downvote하면 토글
    else:
        if moviecomment.downvote_users.filter(pk=request.user.pk).exists():
            moviecomment.downvote_users.remove(request.user)
            isDownvoted=False
        else:
            moviecomment.downvote_users.add(request.user)
            isDownvoted=True
    
    context={
        'isDownvoted':isDownvoted,
        'isUpvoted':isUpvoted,
        'downvoteCnt':moviecomment.downvote_users.count(),
        'upvoteCnt':moviecomment.upvote_users.count()
    }
    
    return JsonResponse(context)


# 장르별 영호 가져오기
@api_view(['GET'])
def genre_movies(request, genre_id):
    genre=get_object_or_404(Genre, genreId=genre_id)
    movies=genre.genre_movies.all()
    serializer=MovieSerializer(movies, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def love_movieId(request, movie_id):
    movie=get_object_or_404(Movie, movieId=movie_id)
    isLike=False
    isHate=False
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        movie.love_users.add(request.user)
        isLove=True
    
    elif movie.hate_users.filter(pk=request.user.pk).exists():
        movie.hate_users.remove(request.user)
        movie.love_users.add(request.user)
        isLove=True
    
    else:
        if movie.love_users.filter(pk=request.user.pk).exists():
            movie.love_users.remove(request.user)
            isLove=False
        else:
            movie.love_users.add(request.user)
            isLove=True
    
    context={
        'isLove': isLove,
        'isLike': isLike,
        'isHate': isHate,
        'loveCnt': movie.love_users.count(),
        'likeCnt': movie.like_users.count(),
        'hateCnt': movie.hate_users.count(),
    }
    
    return JsonResponse(context)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def like_movieId(request, movie_id):
    movie=get_object_or_404(Movie, movieId=movie_id)
    isLove=False
    isHate=False
    if movie.love_users.filter(pk=request.user.pk).exists():
        movie.love_users.remove(request.user)
        movie.like_users.add(request.user)
        isLike=True
    
    elif movie.hate_users.filter(pk=request.user.pk).exists():
        movie.hate_users.remove(request.user)
        movie.like_users.add(request.user)
        isLike=True
    
    else:
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            isLike=False
        else:
            movie.like_users.add(request.user)
            isLike=True
    
    context={
        'isLove': isLove,
        'isLike': isLike,
        'isHate': isHate,
        'loveCnt': movie.love_users.count(),
        'likeCnt': movie.like_users.count(),
        'hateCnt': movie.hate_users.count(),
    }
    
    return JsonResponse(context)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def hate_movieId(request, movie_id):
    movie=get_object_or_404(Movie, movieId=movie_id)
    isLike=False
    isLove=False
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        movie.hate_users.add(request.user)
        isHate=True
    
    elif movie.love_users.filter(pk=request.user.pk).exists():
        movie.love_users.remove(request.user)
        movie.hate_users.add(request.user)
        isHate=True
    
    else:
        if movie.hate_users.filter(pk=request.user.pk).exists():
            movie.hate_users.remove(request.user)
            isHate=False
        else:
            movie.hate_users.add(request.user)
            isHate=True
    
    context={
        'isLove': isLove,
        'isLike': isLike,
        'isHate': isHate,
        'loveCnt': movie.love_users.count(),
        'likeCnt': movie.like_users.count(),
        'hateCnt': movie.hate_users.count(),
    }
    
    return JsonResponse(context)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def love_moviepk(request, movie_pk):
    movie=get_object_or_404(Movie, pk=movie_pk)
    isLike=False
    isHate=False
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        movie.love_users.add(request.user)
        isLove=True
    
    elif movie.hate_users.filter(pk=request.user.pk).exists():
        movie.hate_users.remove(request.user)
        movie.love_users.add(request.user)
        isLove=True
    
    else:
        if movie.love_users.filter(pk=request.user.pk).exists():
            movie.love_users.remove(request.user)
            isLove=False
        else:
            movie.love_users.add(request.user)
            isLove=True
    
    context={
        'isLove': isLove,
        'isLike': isLike,
        'isHate': isHate,
        'loveCnt': movie.love_users.count(),
        'likeCnt': movie.like_users.count(),
        'hateCnt': movie.hate_users.count(),
    }
    
    return JsonResponse(context)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def like_moviepk(request, movie_pk):
    movie=get_object_or_404(Movie, pk=movie_pk)
    isLove=False
    isHate=False
    if movie.love_users.filter(pk=request.user.pk).exists():
        movie.love_users.remove(request.user)
        movie.like_users.add(request.user)
        isLike=True
    
    elif movie.hate_users.filter(pk=request.user.pk).exists():
        movie.hate_users.remove(request.user)
        movie.like_users.add(request.user)
        isLike=True
    
    else:
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            isLike=False
        else:
            movie.like_users.add(request.user)
            isLike=True
    
    context={
        'isLove': isLove,
        'isLike': isLike,
        'isHate': isHate,
        'loveCnt': movie.love_users.count(),
        'likeCnt': movie.like_users.count(),
        'hateCnt': movie.hate_users.count(),
    }
    
    return JsonResponse(context)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def hate_moviepk(request, movie_pk):
    movie=get_object_or_404(Movie, pk=movie_pk)
    isLike=False
    isLove=False
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        movie.hate_users.add(request.user)
        isHate=True
    
    elif movie.love_users.filter(pk=request.user.pk).exists():
        movie.love_users.remove(request.user)
        movie.hate_users.add(request.user)
        isHate=True
    
    else:
        if movie.hate_users.filter(pk=request.user.pk).exists():
            movie.hate_users.remove(request.user)
            isHate=False
        else:
            movie.hate_users.add(request.user)
            isHate=True
    
    context={
        'isLove': isLove,
        'isLike': isLike,
        'isHate': isHate,
        'loveCnt': movie.love_users.count(),
        'likeCnt': movie.like_users.count(),
        'hateCnt': movie.hate_users.count(),
    }
    
    return JsonResponse(context)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def love_movieCd(request, movieCd):
    movie=get_object_or_404(Movie, movieCd=movieCd)
    isLike=False
    isHate=False
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        movie.love_users.add(request.user)
        isLove=True
    
    elif movie.hate_users.filter(pk=request.user.pk).exists():
        movie.hate_users.remove(request.user)
        movie.love_users.add(request.user)
        isLove=True
    
    else:
        if movie.love_users.filter(pk=request.user.pk).exists():
            movie.love_users.remove(request.user)
            isLove=False
        else:
            movie.love_users.add(request.user)
            isLove=True
    
    context={
        'isLove': isLove,
        'isLike': isLike,
        'isHate': isHate,
        'loveCnt': movie.love_users.count(),
        'likeCnt': movie.like_users.count(),
        'hateCnt': movie.hate_users.count(),
    }
    
    return JsonResponse(context)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def like_movieCd(request, movieCd):
    movie=get_object_or_404(Movie, movieCd=movieCd)
    isLove=False
    isHate=False
    if movie.love_users.filter(pk=request.user.pk).exists():
        movie.love_users.remove(request.user)
        movie.like_users.add(request.user)
        isLike=True
    
    elif movie.hate_users.filter(pk=request.user.pk).exists():
        movie.hate_users.remove(request.user)
        movie.like_users.add(request.user)
        isLike=True
    
    else:
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            isLike=False
        else:
            movie.like_users.add(request.user)
            isLike=True
    
    context={
        'isLove': isLove,
        'isLike': isLike,
        'isHate': isHate,
        'loveCnt': movie.love_users.count(),
        'likeCnt': movie.like_users.count(),
        'hateCnt': movie.hate_users.count(),
    }
    
    return JsonResponse(context)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def hate_movieCd(request, movieCd):
    movie=get_object_or_404(Movie, movieCd=movieCd)
    isLike=False
    isLove=False
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        movie.hate_users.add(request.user)
        isHate=True
    
    elif movie.love_users.filter(pk=request.user.pk).exists():
        movie.love_users.remove(request.user)
        movie.hate_users.add(request.user)
        isHate=True
    
    else:
        if movie.hate_users.filter(pk=request.user.pk).exists():
            movie.hate_users.remove(request.user)
            isHate=False
        else:
            movie.hate_users.add(request.user)
            isHate=True
    
    context={
        'isLove': isLove,
        'isLike': isLike,
        'isHate': isHate,
        'loveCnt': movie.love_users.count(),
        'likeCnt': movie.like_users.count(),
        'hateCnt': movie.hate_users.count(),
    }
    
    return JsonResponse(context)



@api_view(['PUT'])
def add_movieCd(request, movieId):
    movie=get_object_or_404(Movie, movieId=movieId)
    serializer=AddMovieCdSerializer(movie, data=request.data)
    if request.data:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        return Response({'error' : 'movieCd를 입력'})
    

@api_view(['GET'])
def genres(request):
    genres=Genre.objects.all()
    serializer=GenreSerializer(genres, many=True)
    return Response(serializer.data)


def calculating_jaccard_similarity(set1, set2):
    intersection_set=set1.intersection(set2)
    union_set=set1.union(set2)
    similarity=len(intersection_set)/len(union_set)
    return similarity

def find_similar_movies(list):
    result=[]

    for movie in list:
        target_keywords=set([keyword.keywordName for keyword in movie.keyword_set.all()])
        
        for movie in Movie.objects.all():
            keywords=movie.keyword_set.all()
            movie_keywords=set([keyword.keywordName for keyword in keywords])
            
            similarity=calculating_jaccard_similarity(target_keywords, movie_keywords)
            if similarity>=0.15:
                result.append(movie)
    
    return result

# params : page, per_page, total 받아서 사용
# 기본 : page=1, per_page=40, total=40
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def recommend(request):
    user=request.user
    
    love_movies=user.love_movies.all()
    love_movies_similar=(find_similar_movies(love_movies) if love_movies else [])

    like_movies=user.like_movies.all()
    like_movies_similar=(find_similar_movies(like_movies) if like_movies else [])
    
    hate_movies=user.hate_movies.all()
    hate_movies_similar=(find_similar_movies(hate_movies) if hate_movies else [])
    
    like_genres=user.like_genres.all()
    
    recommends=[]
    for movie in Movie.objects.all():
        movie_genres=movie.genres.all()
        overlaps=like_genres.intersection(movie_genres)
        weight=len(overlaps)
        
        if love_movies and movie in love_movies_similar:
            weight+=2
        if like_movies and movie in like_movies_similar:
            weight+=1
        if hate_movies:
            if movie in hate_movies:
                continue
            if movie in hate_movies_similar:
                weight-=2
        
        recommends.append((movie, weight))
    
    page=1
    if 'page' in request.GET.keys():
        page=int(request.GET['page'])
    
    per_page=40
    if 'per_page' in request.GET.keys():
        per_page=int(request.GET['per_page'])
        
    total=40
    if 'total' in request.GET.keys():
        total=int(request.GET['total'])
        
    total_page=total//per_page+1
    
    recommends.sort(key=lambda x:(x[1], x[0].popularity, x[0].vote_average), reverse=True)
    recommends=recommends[:total]
    recommends=recommends[(page-1)*per_page:page*per_page]
    recommends=[movie[0] for movie in recommends]
    serializer=MovieSerializer(recommends, many=True)
    serializer.data[0]['total_page']=total_page
    return Response(serializer.data)