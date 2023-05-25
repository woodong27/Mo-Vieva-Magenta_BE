from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import ArticleTag, Article, ArticleComment
from movies.models import Movie
from .serializers import ArticleTagSerializer, ArticleCommentSerializer, ArticleSerializer, MovieReviewSerializer, NoticeSerializer, TagArticleSerializer, ArticleUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse


# Create your views here.
@api_view(['GET'])
def articletag_list(request):
    articletags=get_list_or_404(ArticleTag)
    serializer=ArticleTagSerializer(articletags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def articles(request):
    articles=Article.objects.all()
    if articles:
        serializer=ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    else:
        return Response([])


# 태그 별 게시물 가져오기
@api_view(['GET'])
def tagArticles(request, tag_id):
    tag=get_object_or_404(ArticleTag, pk=tag_id)
    articles=tag.article_set.all()
    if articles:
        serializer=TagArticleSerializer(articles, many=True)
        return Response(serializer.data)
    else:
        return Response([])


# article tag : 1-자유, 2-영화후기, 3-모임모집, 4-모임후기, 5-공지(notice)
# 공지 작성하는 함수는 따로 있음
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def createArticle(request):
    tag_pk=request.data['tag_pk']
    tag=get_object_or_404(ArticleTag, pk=tag_pk)
    serializer=ArticleSerializer(data=request.data)
    
    if 'by' in request.data.keys():
        if request.data['by']=='id':
            try:
                movie=Movie.objects.get(movieId=int(request.data['key']))
                if serializer.is_valid(raise_exception=True):
                    serializer.save(movie=movie, tag=tag, author=request.user)
                    return Response(serializer.data)
            except:
                return Response({'error':'그런 영화는 없음'})
        
        elif request.data['by']=='cd':
            try:
                movie=Movie.objects.get(movieCd=int(request.data['key']))
                if serializer.is_valid(raise_exception=True):
                    serializer.save(movie=movie, author=request.user, tag=tag)
                    return Response(serializer.data)
            except:
                return Response({'error':'그런 영화는 없음'})
        
        elif request.data['by']=='pk':
            try:
                movie=Movie.objects.get(pk=int(request.data['key']))
                if serializer.is_valid(raise_exception=True):
                    serializer.save(movie=movie, author=request.user, tag=tag)
                    return Response(serializer.data)
            except:
                return Response({'error':'그런 영화는 없음'})
    
    else:
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, tag=tag)
            return Response(serializer.data)


# @api_view(['GET'])
# def idReview(request, movieId):
#     # 특정 영화에 달린 MovieReview글들만 다 가져오기
#     movie=get_object_or_404(Movie, movieId=movieId)
#     reviews=movie.article_set.filter(tag=2)
#     if reviews:
#         serializer=MovieReviewSerializer(reviews, many=True)
#         return Response(serializer.data)
    
#     else:
#         return Response([])


# @api_view(['GET'])
# def cdReview(request, movieCd):
#     movie=get_object_or_404(Movie, movieCd=movieCd)
#     reviews=movie.article_set.filter(tag=2)
#     if reviews:
#         serializer=MovieReviewSerializer(reviews, many=True)
#         return Response(serializer.data)
    
#     else:
#         return Response([])
      

# @api_view(['GET'])
# def pkReview(request, movie_pk):
#     movie=get_object_or_404(Movie, pk=movie_pk)
#     reviews=movie.article_set.filter(tag=2)
#     if reviews:
#         serializer=MovieReviewSerializer(reviews, many=True)
#         return Response(serializer.data)
    
#     else:
#         return Response([])
    

@api_view(['GET'])
def idArticle(request, movieId):
    # 특정 영화에 달린 MovieReview글들만 다 가져오기
    movie=get_object_or_404(Movie, movieId=movieId)
    
    if 'tag' in request.GET.keys():
        tag=ArticleTag.objects.get(pk=int(request.GET['tag']))
        articles=movie.article_set.filter(tag=tag)
    else:
        articles=movie.article_set.all()
        
    if articles:
        serializer=ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    else:
        return Response([])


@api_view(['GET'])
def cdArticle(request, movieCd):
    movie=get_object_or_404(Movie, movieCd=movieCd)
    
    if 'tag' in request.GET.keys():
        tag=ArticleTag.objects.get(pk=int(request.GET['tag']))
        articles=movie.article_set.filter(tag=tag)
    else:
        articles=movie.article_set.all()
        
    if articles:
        serializer=ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    else:
        return Response([])
      

@api_view(['GET'])
def pkArticle(request, movie_pk):
    movie=get_object_or_404(Movie, pk=movie_pk)
    if 'tag' in request.GET.keys():
        tag=ArticleTag.objects.get(pk=int(request.GET['tag']))
        articles=movie.article_set.filter(tag=tag)
    else:
        articles=movie.article_set.all()
    
    if articles:
        serializer=ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    else:
        return Response([])
    

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def createNotice(request):
    tag=get_object_or_404(ArticleTag, pk=5)
    serializer=NoticeSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(tag=tag, author=request.user, isNotice=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@permission_classes([IsAuthenticated])
@api_view(['PUT', 'DELETE', 'GET'])
def updateArticle(request, article_pk):
    article=get_object_or_404(Article, pk=article_pk)
    print(article)
    if request.method=='PUT':
        serializer=ArticleUpdateSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method=='DELETE':
        article.delete()
        return Response({'detail' : f'{article_pk}번째 article 삭제'},status=status.HTTP_204_NO_CONTENT)

    elif request.method=='GET':
        serializer=ArticleUpdateSerializer(article)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upvoteArticle(request, article_pk):
    article=Article.objects.get(pk=article_pk)
    
    isDownvote=False
    if article.downvote_users.filter(pk=request.user.pk).exists():
        article.downvote_users.remove(request.user)
        article.upvote_users.add(request.user)
        isUpvote=True
    
    else:
        if article.upvote_users.filter(pk=request.user.pk).exists():
            article.upvote_users.remove(request.user)
            isUpvote=False
        else:
            article.upvote_users.add(request.user)
            isUpvote=True
    
    context={
        'isUpvote': isUpvote,
        'isDownvote': isDownvote,
        'upvoteCnt': article.upvote_users.count(),
        'downvoteCnt': article.downvote_users.count()
    }
    return Response(context)
        


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def downvoteArticle(request, article_pk):
    article=Article.objects.get(pk=article_pk)
    
    isUpvote=False
    if article.upvote_users.filter(pk=request.user.pk).exists():
        article.upvote_users.remove(request.user)
        article.downvote_users.add(request.user)
        isDownvote=True
    
    else:
        if article.downvote_users.filter(pk=request.user.pk).exists():
            article.downvote_users.remove(request.user)
            isDownvote=False
        else:
            article.downvote_users.add(request.user)
            isDownvote=True
    
    context={
        'isUpvote': isUpvote,
        'isDownvote': isDownvote,
        'upvoteCnt': article.upvote_users.count(),
        'downvoteCnt': article.downvote_users.count()
    }
    return Response(context)


@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET'])
def comments(request, article_pk):
    article=get_object_or_404(Article, pk=article_pk)
        
    if request.method=='POST':
        serializer=ArticleCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if 'isSecret' in request.data.keys():
                serializer.save(article=article, author=request.user, isSecret=request.data['isSecret'])
                return Response(serializer.data)
            else:
                serializer.save(article=article, author=request.user)
                return Response(serializer.data)
        
    elif request.method=='GET':
        articlecomments=article.articlecomment_set.all()
        serializer=ArticleCommentSerializer(articlecomments, many=True)
        return Response(serializer.data)


# 댓글 수정/삭제하기
@permission_classes([IsAuthenticated])
@api_view(['PUT', 'DELETE', 'GET'])
def comment(request, articlecomment_pk):
    comment=get_object_or_404(ArticleComment, pk=articlecomment_pk)
    if request.method=='PUT':
        serializer=ArticleCommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method=='DELETE':
        comment.delete()
        return Response({'detail' : f'{articlecomment_pk}번째 articlecomment 삭제'},status=status.HTTP_204_NO_CONTENT)
    
    elif request.method=='GET':
        serializer=ArticleCommentSerializer(comment)
        return Response(serializer.data)
    
    
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upvoteArticleComment(request, articlecomment_pk):
    articlecomment=ArticleComment.objects.get(pk=articlecomment_pk)
    
    isDownvote=False
    if articlecomment.downvote_users.filter(pk=request.user.pk).exists():
        articlecomment.downvote_users.remove(request.user)
        articlecomment.upvote_users.add(request.user)
        isUpvote=True
    
    else:
        if articlecomment.upvote_users.filter(pk=request.user.pk).exists():
            articlecomment.upvote_users.remove(request.user)
            isUpvote=False
        else:
            articlecomment.upvote_users.add(request.user)
            isUpvote=True
    
    context={
        'isUpvote': isUpvote,
        'isDownvote': isDownvote,
        'upvoteCnt': articlecomment.upvote_users.count(),
        'downvoteCnt': articlecomment.downvote_users.count()
    }
    return Response(context)
        


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def downvoteArticleComment(request, articlecomment_pk):
    articlecomment=ArticleComment.objects.get(pk=articlecomment_pk)
    
    isUpvote=False
    if articlecomment.upvote_users.filter(pk=request.user.pk).exists():
        articlecomment.upvote_users.remove(request.user)
        articlecomment.downvote_users.add(request.user)
        isDownvote=True
    
    else:
        if articlecomment.downvote_users.filter(pk=request.user.pk).exists():
            articlecomment.downvote_users.remove(request.user)
            isDownvote=False
        else:
            articlecomment.downvote_users.add(request.user)
            isDownvote=True
    
    context={
        'isUpvote': isUpvote,
        'isDownvote': isDownvote,
        'upvoteCnt': articlecomment.upvote_users.count(),
        'downvoteCnt': articlecomment.downvote_users.count()
    }
    return Response(context)