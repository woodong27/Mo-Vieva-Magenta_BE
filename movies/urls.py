from django.urls import path
from . import views

urlpatterns = [
    # DB 초기화
    # path('init/', views.initializingDB),
    
    # DB에 영화 추가하기
    path('id/<int:movieId>/add/', views.addMovie),
    
    # path('getGenres/', views.getGenres),
    # 전체 영화 목록
    path('list/', views.movies),
    # movieId로 가져오기
    path('id/<int:movie_id>/', views.movieID),
    # movieCd로 가져오기
    path('cd/<int:movieCd>/', views.movieCD),
    # pk로 가져오기
    path('pk/<int:movie_pk>/', views.moviePK),
    
    # movie love / like / hate
    # id
    path('id/<int:movie_id>/love/', views.love_movieId),
    path('id/<int:movie_id>/like/', views.like_movieId),
    path('id/<int:movie_id>/hate/', views.hate_movieId),
    # pk
    path('pk/<int:movie_pk>/love/', views.love_moviepk),
    path('pk/<int:movie_pk>/like/', views.like_moviepk),
    path('pk/<int:movie_pk>/hate/', views.hate_moviepk),
    # cd
    path('cd/<int:movieCd>/love/', views.love_movieCd),
    path('cd/<int:movieCd>/like/', views.like_movieCd),
    path('cd/<int:movieCd>/hate/', views.hate_movieCd),
    
    # 해당 영화에 moviecomment 작성 및 영화의 moviecomment 불러오기
    path('id/<int:movieId>/comment/', views.idmoviecomments),
    path('cd/<int:movieCd>/comment/', views.cdmoviecomments),
    path('pk/<int:movie_pk>/comment/', views.pkmoviecomments),
    
    # moviecomment 수정 및 삭제
    path('comment/<int:moviecomment_pk>/', views.moviecomment),
    
    # moviecomment 추천/비추천
    path('comment/<int:moviecomment_pk>/upvote/', views.upvote),
    path('comment/<int:moviecomment_pk>/downvote/', views.downvote),
    
    # 해당 장르의 영화들 가져오기
    path('genre/<int:genre_id>/', views.genre_movies),
    
    # 페이지별 영화 가져오기
    # path('page/<int:page>/', views.page_movies),
    
    # movie love / like / hate
    # path('<int:movie_id>/love/', views.love_movie),
    # path('<int:movie_id>/like/', views.like_movie),
    # path('<int:movie_id>/hate/', views.hate_movie),
    
    # KOFIC
    path('<int:movieId>/addCd/', views.add_movieCd),
    
    # 전체 장르 반환
    path('genre/list/', views.genres),
    
    # 영화 추천
    # path('training/', views.train),
    path('recommend/', views.recommend),
]
