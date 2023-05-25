from django.urls import path
from . import views

urlpatterns = [
    path('articletags/', views.articletag_list),
    # path('list/', views.articles),
    # path('<int:article_pk>/', views.article),
    
    # 태그 상관 없이 모든 리뷰 가져오기
    path('list/', views.articles),
    
    # article 수정, 삭제, 해당 pk의 게시글 가져오기
    path('<int:article_pk>/', views.updateArticle),
    
    # 공지글 제외 나머지 글 작성
    path('create/', views.createArticle),
    
    # 공지글 작성
    path('notice/', views.createNotice),
    
    # 게시물 추천/비추천
    path('<int:article_pk>/upvote/', views.upvoteArticle),
    path('<int:article_pk>/downvote/', views.downvoteArticle),
    
    # 영화 리뷰 관련 url
    # path('id/<int:movieId>/review/', views.idReview),
    # path('cd/<int:movieCd>/review/', views.cdReview),
    # path('pk/<int:movie_pk>/review/', views.pkReview),
    
    # movieId로 연관된 계시물 모두 가져오기
    path('id/<int:movieId>/article/', views.idArticle),
    path('cd/<int:movieCd>/article/', views.cdArticle),
    path('pk/<int:movie_pk>/article/', views.pkArticle),
    
    # 해당 태그가 달린 게시물 다 가져오기
    path('tag/<int:tag_id>/', views.tagArticles),
    
    # articlecomment 관련
    # 해당 게시글의 댓글들 가져오기 + 댓글 작성
    path('<int:article_pk>/comment/', views.comments),
    # 댓글 하나만 불러오기, 수정, 삭제
    path('comment/<int:articlecomment_pk>/', views.comment),
    
    # 댓글 추천/비추천
    path('comment/<int:articlecomment_pk>/upvote/', views.upvoteArticleComment),
    path('comment/<int:articlecomment_pk>/downvote/', views.downvoteArticleComment),
]
