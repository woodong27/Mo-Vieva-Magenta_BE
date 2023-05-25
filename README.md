# 최동우

##### 사용 전 초기 설정
```markdown
git clone 후 가상환경 설치해서 requirements.txt install
migrate후에 fixtures폴더에 있는 json파일들 loaddata 해주고 사용하면 됨
fixtures폴더는 각 앱 마다 따로 존재

python manage.py loaddata accounts/grades.json accounts/users.json communities/articletags.json movies/genres.json movies/movies.json movies/videos.json movies/keywords.json
```

#### 현재 사용 가능한 URL 
##### accounts/
```markdown
유저 인증 필요
POST
password/change/ : 비밀번호 변경, data : new_password1, new_password2

logout/ : 로그아웃

password/reset/ : 비밀번호 재설정, data : email

grade/<int:grade_pk>/ : 유저 등급 변경(1, 2, 3)

admin/ : 유저 isAdmin True,False 토글

genre/ : data로 like_genres를 입력받아서 저장하고 해당 유저가 선택한 like_genre들을 반환

follow/ : 로그인 되어있는 상태에서 상대 유저를 팔로우, 언팔로우 가능
상대 유저의 followers, followings의 수와 현재 내가 follow했는지 안했는지를 반환

image/ : 프로필 이미지 추가

GET
userinfo/ : 유저 정보 받아오기
genre/ : 선택한 선호 장르받아오기
<int:user_pk>/ : 해당 유저의 정보 가져오기(프로필페이지)

유저 인증 필요 없음
POST
signup/ : 회원가입, data : username, password1, password2
login/ : 로그인, data : username, password
```

##### community/
```markdown
유저 인증 필요
POST
create/
tag-1(자유), tag-2(영화후기), tag-3(모임모집), tag-4(모임후기)
data : title, content, tag_pk, by(id, cd, pk) - by는 없을 수도 있음
by가 있을 때는 movieId, movieCd, movie_pk 등 각각에 맞는 key를 입력해야함
맞는 값이 오지 않으면 {'error':'그런 영화는 없음'}라고 반환 

notice/ : 공지글 작성, data : title, content

<int:article_pk>/comment/ : 게시글에 댓글 달기, data : content
받아오는 data에 isSecret이 있으면 확인해서 비밀댓글로 설정해줌

<int:article_pk>/upvote/ : 해당 게시글 upvote
<int:article_pk>/downvote/ : 해당 게시글 downvote

comment/<int:articlecomment_pk>/upvote/ : 댓글 upvote
comment/<int:articlecomment_pk>/downvote/ : 댓글 downvote


PUT
<int:article_pk>/ : 해당 게시글 수정, data : title, content
comment/<int:articlecomment_pk>/ : 댓글 수정

DELETE
<int:article_pk>/ : 해당 게시글 삭제
comment/<int:articlecomment_pk>/ : 댓글 삭제


유저 인증 필요 없음
GET
list/ : 전체 게시물 받아오기
tag/<int:tag_pk>/ : 태그별 게시물 받아오기
<int:article_pk>/ : 특정 게시글 하나만 가져오기

영화와 관련된 모든 게시물 불러오기
id/<int:movieId>/article/
cd/<int:movieCd>/article/
pk/<int:movie_pk>/article/
params: {'tag': 원하는 tag_pk} 를 넘겨줘서
params가 있으면 해당 태그의 게시글만 가져오고 없으면 전체 게시글 가져옴

<int:article_pk>/comment/ : 해당 게시글의 댓글 불러오기
comment/<int:articlecomment_pk>/ : 댓글 하나만 가져오기
```
##### movie/
```markdown
유저 인증 필요
POST

영화 추가하기
id/<int:movieId>/add/ : 해당 TMDBid의 영화를 추가해줌

영화 한줄평 작성 data : content
id/<int:movieId>/comment/
cd/<int:movieCd>/comment/ 
pk/<int:moviepk>/comment/

comment/<int:moviecomment_pk>/upvote/ : 한줄평 upvote
comment/<int:moviecomment_pk>/downvote/ : 한줄평 downvote

id로 영화 love, like, hate
id/<int:movieId>/love/
id/<int:movieId>/like/
id/<int:movieId>/hate/

cd로 영화 love, like, hate
cd/<int:movieCd>/love/
cd/<int:movieCd>/like/
cd/<int:movieCd>/hate/

pk로 영화 love, like, hate
pk/<int:movie_pk>/love/
pk/<int:movie_pk>/like/
pk/<int:movie_pk>/hate/

PUT
comment/<int:moviecomment_pk>/ : 한줄평 수정, data : content
DELETE
comment/<int:moviecomment_pk>/ : 한줄평 삭제


유저 인증 필요 없음
GET
list/ : 전체 영화 목록(DB에서)
data : page(default=1), per_page(default=40), genre(없어도 되는 옵션)
반환되는 목록에서 첫번째 영화에는 total_page를 추가해서 현재 입력한
per_page에 맞게 전체 페이지 목록이 반환되게 했음

genre/list/ : 전체 장르 종류 반환

영화 하나만 가져오기
id/<int:movieId>/
cd/<int:movieCd>/
pk/<int:movie_pk>/

해당 영화의 한줄 평 가져오기(영화 데이터 가져오기 안에 한줄평도 들어있긴 함)
id/<int:movieId>/comment/
cd/<int:movieCd>/comment/
pk/<int:movie_pk>/comment/

genre/<int:genreId>/ : TMDB의 genre id로 장르별 영화 검색

comment/<int:moviecomment_pk>/ : 한줄평 하나만 가져오기

recommend/ : 추천 영화가져오기(10개)
params로 page, per_page, total 을 받아서 첫번째 영화에 total_page를 추가해줬음

PUT
<int:movieId>/addCd/ : 영화에 KOFIC의 movieCd추가
```

## 05/18/2023

### Back-end

ERD 바탕으로 model 제작<br>
makemigrations, migrate해서 table만들어지는 것 까지 확인하였음<br>
accounts관련은 바로 사용 가능<br>
test 계정(일반) : username - test1 / password - pass12!!<br>

##### 회원 인증 URL / 사용법
로그인이 되어있어야 로그아웃과 비밀번호 변경을 할 수 있음<br>
로그아웃하고 새로 로그인하면 Token이 바뀌기 때문에 바뀐 토큰을 사용해줘야함<br>
##### urls
```markdown
accounts/login/ : username, password
accounts/signup/ : username, password1, password2
accounts/logout/ : headers: {Authorization : Token 회원토큰}
accounts/password/change/ : headers: {Authorization : Token 회원토큰}
```

<hr>

## 05/19/2023

### Back-end

#### ~ 18:00

유저 등급 변경 완성<br>
urls<br>
accounts/grade/<변경하려는 등급의 id><br>
1 : 씨앗 , 2 : 새싹, 3: 꽃<br>

BaseMovie<br>
영화 추천에 사용하기 위해서 TMDB의 trending 영화들을 가져온 뒤
id, title, popularity, vote_average, vote_count를 저장<br>
TMDB의 genre목록을 가져와서 Genre테이블에 저장 한 후 BaseMovie에
ManyToManyField로 연결해서 각 영화마다 가지고 있는 장르들을 추가해주었음<br>
Video테이블을 만들어서 영화를 저장 할 때 관련된 영상들을 검색하여
언어가 영어, 한글이고, official=True, YouTube영상 중 트레일러나 티저인 것만
key와 type을 저장하는 코드 완성하였음<br>

~~집 가서 전체 트렌딩 영화에 대해서 돌려서 DB에 저장하고 dumpdata해둘 예정~~
<br>


#### ~ 23:19

movies<br>
Movie 테이블 필드 수정 및 데이터 수집해서 dumpdata로 정리해둠<br>
GET / movies/list/ : movie table의 모든 정보 보내줌<br>
GET / movies/<int:movie_pk>/ : 해당 영화의 정보를 보내줌<br>

##### 보내주는 정보들
```markdown
lovesCnt : love표시한 유저들의 수
likesCnt : like표시한 유저들의 수
hatesCnt : hate표시한 유저들의 수
genres : 해당 영화의 genreId, genreName 전부
videos : 해당 영화의 id로 TMDB에서 관련 영상을 검색했을 때 나오는 유튜브 공식영상들의 key와 type
movidId : TMDB movie id
movieCd : KOFIC movieCd - 현재 모두 null인 상태
title : 해당 영화의 한글 제목
poster_path : TMDB의 poster 주소
backdrop_path : TMDB의 backdrop 주소
popularity : TMDB의 popularity
vote_average : TMDB의 vote_average
vote_count : TMDB의 vote_count
love_users : love표시한 유저들의 id
like_users : like표시한 유저들의 id
hate_users : hate표시한 유저들의 id
```

<hr>

## 05/20/2023

### Back-end

#### ~ 10:20
movie 정보 보낼 때 moviecomments도 같이 보내줄 수 있게 serializer 수정<br>

##### 추가한 url
```markdown
유저 인증 필요 - headers: {Authorization : Token 회원토큰}
POST / <int:movieId>/comment/ : 해당 영화에 moviecomment 작성하기
PUT / comment/<int:moviecomment_pk>/ : movicomment 수정하기
DELETE / comment/<int:moviecomment_pk>/ : movicomment 삭제하기
POST / comment/<int:moviecomment_pk>/upvote/ : 해당 moviecomment upvote하기
POST / comment/<int:moviecomment_pk>/downvote/ : 해당 moviecomment downvote 하기

유저 인증 필요 없음
GET / comment/<int:moviecomment_pk>/ : movicomment 보여줌
```

#### ~ 12:04
moviecomment 수정, 삭제시 댓글을 작성한 유저가 아니면<br>
error : 댓글 작성자가 아님 이라는 메세지를 보내도록 수정했음<br>
추후에 다른 문구나 기능으로 수정할 수 있음<br>

##### 추가한 url
```markdown 
유저 인증 필요 - headers: {Authorization : Token 회원토큰} 필요
POST / accounts/admin : 해당 유저의 isAdmin 토글
```

#### ~ 16:30

##### 추가한 url
```markdown
유저 인증 필요
~~ GET / accounts/user/ : 현재 로그인된 유저의 정보 가져오기 ~~
POST / communities/review/<int:movie_id>/ : 특정 영화 관련 리뷰게시글 작성

유저 인증 필요 없음
GET / communities/reviews/<int:movie_id>/ : 영화 관련된 모든 리뷰게시글 불러오기
GET / communities/tag/<int:tag_id>/ : 해당 태그가 달린 모든 게시글 불러오기
```

#### ~17:40

##### 추가한 url
```markdown
유저 인증 필요 없음
GET / movies/genre/<int:genre_id>/ : 장르별 영화 목록 가져오기
GET / movies/page/1/ : 50개씩 페이지별 영화 가져옴
```

<hr>

## 05/21/2023

### Back-end

#### ~ 13:08
userinfo를 보여주는 url 수정<br>
id, username, isAdmin, grade 네가지를 보여주도록 변경<br>
게시글 작성 url 완성<br>
영화 리뷰 작성 / 자유, 모임모집, 모임후기 / 공지글 세가지 url이 따로 구분되어 있음<br>
태그별 게시물을 가져오는 url이 있기 때문에 영화관련 리뷰글 가져오기 이외에는 POST말고 GET url은 만들지 않았음<br>
5번째 articletag 추가 : tag = 공지
##### 추가한 url 
```markdown
유저 인증 필요
GET / accounts/userinfo/
POST / communities/review/<int:movie_id>/ : 해당 영화의 리뷰게시글 작성
POST / communities/create/<int:tag_id>/ : 태그 별 게시글 작성하기(자유, 모임모집, 모임후기)
POST / communities/notice/ : 공지글 작성하기

유저 인증 필요 없음
GET / communities/<int:movie_id>/reviews/ : 해당 영화의 리뷰게시글 전체 불러오기
GET / communities/tag/<int:tag_id>/ : 해당 태그가 달린 게시물 전체 불러오기
GET / communities/list/ : 태그 상관없이 전체 게시글 가져오기
```


#### ~11:45
##### 추가한 url
```markdown
유저 인증 필요
PUT / communities/update/<int:article_pk>/ : 해당 게시글 수정
DELETE / communities/update/<int:article_pk>/ : 해당 게시글 삭제
POST / communities/<int:article_pk>/comment/ : 해당 글에 댓글 작성
PUT / communities/<int:articlecomment_pk>/ : 해당 댓글 수정
DELETE / communities/<int:articlecomment_pk>/ : 해당 댓글 삭제

유저 인증 필요 없음
GET / communities/list/ : 전체 article목록
GET / communities/comments/<int:article_pk>/ : 해당 글의 모든 댓글 목록
```

##### 내일 해야할 것
~~영화 love, like, hate 체크~~<br>
~~-> 완성하고 나면 userinfo를 불렀을 때 love, like, hate표시한 영화목록도 같이 띄워줄 수 있게 수정~~<br>
글을 불러올 때 해당 글에 달린 댓글도 받아올 수 있게 수정해볼 예정

<hr>

## 05/22/2023

#### ~ 18:00

##### 추가한 url
```markdown
유저 인증 필요
POST / movies/<int:movie_id>/love/ : 영화 love
POST / movies/<int:movie_id>/like/ : 영화 like
POST / movies/<int:movie_id>/hate/ : 영화 hate
```

##### 한 것
userinfo 불러올 시 followings, followers, love_movies, like_movies, hate_movies,<br>
articles, last_login, date_joined를 불러오도록 수정<br>
Movie 테이블에 overview 필드 추가<br>
KOFIC Cd, movie_pk로 영화 검색하기<br>
article, movie가져올 때 db에 없는 거면 404에러 대신 빈 리스트 보내도록 수정<br>
moviecomment 보낼 때 id도 보내도록 수정<br>
moviereview 작성 url 변경<br>
article조회 시 articlecomments까지 나오도록 수정<br>
article조회 시 articlecomments에 username까지 나오도록 수정<br>
movie조회 시 moviecomments에서도 username까지 나오게 수정<br>
article 작성 url 수정 및 통합<br>
movieId, movie_pk, movieCd 각각 love, like, hate url추가<br>
url정리<br>
userinfo에서 내가 작성한 영화 한줄평도 같이 나오게 수정<br>
movietable에 release_date추가<br>


##### 집 가서 해야할 것
~~page(전체 목록 중 선택된 페이지를 보여줌), per_page(페이지당 보여줄 영화의 수), 
genreId(없어도 되는 옵션, 해당 장르의 영화를 페이지별로 보여줌) data를 받아서 페이지로 영화목록을 주는 url 만들기~~
<br>
영화 한줄 평 작성하는거 by랑 key로 id, cd, pk url 추가하기<br>
~~movie_id로 영화 후기 게시글만 가져오는게 아니라 영화 id가 달린 모든 게시물 가져오기~~<br>


#### ~ 자기 전
movieId로 영화 후기 말고도 관련된 모든 게시물 가져오는 url 추가했음<br>
data : page, per_page, genreId를 받으면 그에 맞는 영화를 보여주는 페이지 url 추가<br>

<hr>

## 05/23/2023

#### ~18:00

movie list불러올 때 첫번째 영화에만
현재 per_page에 맞게 전체 페이지 수를 보여줄 수 있게 수정<br>
기존 댓글 작성 url에 isSecret을 data로 받을 수 있게 해서 비밀댓글 설정이 가능하게 함<br>
전체 장르 목록을 보여주는 url과 user가 선호 장르를 선택하면 받아와서 저장하는 url 추가<br>
게시글 upvote, downvote url 추가<br>
게시글의 댓글 upvote, downvote url 추가<br>
movieId, movieCd, movie_pk 사용하는 url들 추가<br>
get으로 통신할 때는 data를 받지 못하기 때문에 params를 써서 query string으로 받고
쓸때는 request.GET[key]로 써야함<br>
moviecomment 하나만 가져오는 GET method url 추가<br>
article create시 영화가 등록 되면 영화의 pk, movieId, movieCd까지 반환하도록 수정<br>
articlecomment에서 comment가 달린 article과 그 article의 author정보까지 나오도록 수정<br>
추천 알고리즘 간단하게 만들었는데 한번 더 잘만들어보자<br>


#### 집 가서 할일
~~영화 관련 게시물 불러올 때 params로 tag_pk를 받아서
해당 태그의 게시물만 가져오게 할 것(tag_pk가 없으면 그냥 전체 게시물들)~~<br>
~~장르 선택하고 받아올 때 새로 선택하면 장르 목록 초기화 시키고
받아오는거 에러뜸~~<br>
멋진 추천알고리즘 생각해보기<br>


#### ~ 자기 전
선호 장르 선택할 때 genreId를 리스트(배열)로 받아와서<br>
배열에 중복되는 장르가 있으면 제거해주고, 이미 유저가 선택한 장르가 있다면<br>
해당 장르와 중복되지 않는 장르만 추가되게 해주었음<br>
id/pk/cd로 영화 관련 게시물 검색할 때 params로 'tag'를 받아서 해당 태그를 가진 게시물만 보여주는기능 추가<br>
<br>


## 05/24/2023

#### ~ 12:20
장르 선택 url로 가면 기존에 선택해둔 선호 장르 목록을 초기화 시키고<br>
새로 장르를 선택하도록 변경<br>
article 가져올 때 username까지 보여주게 변경<br>
추천 영화<br>
기본 page=1, per_page=40, total=40<br>
유저 팔로우기능 추가<br>
Article을 작성하거나 가져올 때 관련된 영화가 있으면 그 영화의 장르까지 가져오도록 추가<br>
DB에 영화 추가하는 url 추가<br>


##### 추천 영화 알고리즘
```markdown
유저가 선택한 love_movies, like_movies, hate_movies가 존재하면
해당 영화들의 키워드와 전체 영화들의 키워드 사이의 자카드 유사도를 계산하여
유사도가 일정 이상인 영화만 유사한 영화로 저장했음

1순위
유저가 선택한 선호 장르와 겹치는 장르가 많고
love_movies, like_movies, hate_movies와 유사한 영화에 포함되어있으면
각각에 따라 가중치를 다르게 줌
총 가중치에 따라서 영화들을 내림차순 정렬
2순위
정렬된 영화 중에서 popularity가 높은 순으로 내림차순 정렬
3순위
그 중에서도 vote_average가 높은 순으로 내림차순 정렬
```


##### 해야할 것
~~프로필 사진 추가하기~~<br>
~~게시글 영화 정보 보여줄 때 title도 추가해서 보여주기~~<br>

#### ~ 자기 전
db에 새로 영화 받아옴 총 8795개의 영화와 그것과 관련된 유튜브 video, keyword들<br>
백엔드 배포 해봄
