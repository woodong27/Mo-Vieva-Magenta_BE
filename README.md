# 최동우

#### Back-end 서버 사용 전 초기 설정
```markdown
1. git clone {현재 레포지토리}
2. python -m venv venv
3. source venv/Scripts/activate
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py loaddata accounts/grades.json accounts/users.json communities/articletags.json movies/genres.json movies/movies.json movies/videos.json movies/keywords.json
7. python manage.py runserver
```
<hr>

#### 업무 내역
- Back-end
- Django REST API 제작
- 영화 추천 알고리즘 제작
- heroku를 사용한 back-end 서버 배포

<hr>

#### 영화 추천 알고리즘 기반 커뮤니티 서비스 - 무 비바 마젠타
- 서비스 목표<br>
TMDB에서 수집한 영화 데이터를 바탕으로 영화 추천 알고리즘을 사용하여 사용자 마다 적절한 추천 영화 목록을 보여주고, 회원간 소통 및 영화 감상 모임을 모집할 수 있는 커뮤니티 사이트<br>
<br>

- 개발 환경(Back-end)
    - Python<br>
    - Django 3.2.18<br>
    - Django REST Framework

<hr>

#### URL

|App|Authentication|Method|URL|Description| 
|:---:|:---:|:---:|:---:|:---:|
|accounts/| X |POST|signup/|회원가입|
|accounts/| X |POST|login/|로그인|
|accounts/| O |POST|logout/|로그아웃|
|accounts/| O |POST|password/change/|비밀번호 변경|
|accounts/| O |POST|admin/|관리자 권한 토글|
|accounts/| O |POST|genre/|선호 장르 선택|
|accounts/| O |GET|genre/|선택한 선호 장르 목록|
|accounts/| O |POST|grade/&lt;int:grade_pk&gt;/|유저 등급 변경|
|accounts/| O |POST|follow/&lt;int:user_pk&gt;/|해당 유저 follow/unfollow|
|accounts/| O |GET|userinfo/|현재 로그인된 유저의 정보|
|accounts/| X |GET|&lt;int:user_pk&gt;/|해당 유저의 정보|
|community/| O |POST|create/|article 작성<br>data로 tag, movie 등을 받을 수 있음|
|community/| O |POST|notice/|공지글 작성|
|community/| X |GET|list/|전체 article 목록|
|community/| X |GET|tag/&lt;int:tag_pk&gt;/|태그별 article 목록|
|community/| X |GET|id/&lt;int:movieId&gt;/article/|해당 영화와 관련된 article 목록<br>query string으로 tag 선택 가능|
|community/| X |GET|&lt;int:article_pk&gt;/|article detail|
|community/| O |PUT|&lt;int:article_pk&gt;/|article 수정|
|community/| O |DELETE|&lt;int:article_pk&gt;/|article 삭제|
|community/| O |POST|&lt;int:article_pk&gt;/upvote/|article 추천|
|community/| O |POST|&lt;int:article_pk&gt;/downvote/|article 비추천|
|community/| O |POST|&lt;int:article_pk&gt;/comment/|article에 댓글 작성<br>isSecret에 따라서 비밀 댓글 작성 가능|
|community/| X |GET|&lt;int:article_pk&gt;/comment/|article의 댓글 목록|
|community/| X |GET|comment/&lt;int:articlecomment_pk&gt;/|댓글 가져오기|
|community/| O |PUT|comment/&lt;int:articlecomment_pk&gt;/|댓글 수정|
|community/| O |PUT|comment/&lt;int:articlecomment_pk&gt;/|댓글 삭제|
|community/| O |POST|comment/&lt;int:articlecomment_pk&gt;/upvote/|댓글 추천|
|community/| O |POST|comment/&lt;int:articlecomment_pk&gt;/downvote/|댓글 비추천|
|movie/| X |GET|list/|전체 영화 목록을 반환<br>query string으로 page, per_page, genre 설정 가능|
|movie/| X |GET|genre/list/|전체 장르 목록<br>TMDB에서 받아온 장르 목록(19가지)|
|movie/| X |GET|genre/&lt;int:genreId&gt;/|해당 장르가 포함된 영화 목록<br>사용하는 genreId는 TMDB의 genre 기반|
|movie/| X |GET|id/&lt;int:movieId&gt;/|movie detail|
|movie/| O |POST|id/&lt;int:movieId&gt;/love/|해당 영화 love 표시|
|movie/| O |POST|id/&lt;int:movieId&gt;/like/|해당 영화 like 표시|
|movie/| O |POST|id/&lt;int:movieId&gt;/hate/|해당 영화 hate 표시|
|movie/| X |POST|id/&lt;int:movieId&gt;/add/|DB에 영화 추가<br>입력받은 movieId로 TMDB에서 영화정보를 받아옴|
|movie/| O |POST|id/&lt;int:movieId&gt;/comment/|영화 한줄평 작성|
|movie/| X |GET|id/&lt;int:movieId&gt;/comment/|해당 영화의 한줄평 목록|
|movie/| X |GET|comment/&lt;int:moviecomment_pk&gt;/|한줄평 detail|
|movie/| O |PUT|comment/&lt;int:moviecomment_pk&gt;/|한줄평 수정|
|movie/| O |DELETE|comment/&lt;int:moviecomment_pk&gt;/|한줄평 삭제|
|movie/| O |POST|comment/&lt;int:moviecomment_pk&gt;/upvote/|한줄평 추천|
|movie/| O |POST|comment/&lt;int:moviecomment_pk&gt;/downvote/|한줄평 비추천|
|movie/| O |GET|recommend/|추천 영화 목록|

<hr>

#### ERD
![final-pjt-erd](https://github.com/woodong27/SSAFY_Final/assets/122415763/b24c2b42-2aa1-45d5-92f4-ddd90e97c20b)

<hr>

#### 추천 알고리즘
유저마다 선택한 선호 장르와 좋아요/싫어요 표시한 영화를 바탕으로 컨텐츠 기반 필터링을 사용하여 추천 영화 목록을 구성하는 알고리즘<br>
<br>
좋아요/싫어요 표시한 영화가 존재하면 자카드 유사도를 계산해서 해당 영화들과 비슷한 영화들의 목록을 만들어서 사용하였음<br>
<br>
선택한 선호 장르와 중복되는 것이 많은 영화일수록 더 높은 가중치를 가지게 됨<br>
해당 영화가 좋아요 표시한 영화와 유사한 영화 목록에 있다면 가중치를 더해주고, 싫어요 표시한 영화와 유사한 영화 목록에 있다면 가중치를 감소시켜 줌<br>
모든 영화에 대해서 가중치가 계산되고 나면, 가중치를 바탕으로 영화를 내림차순 정렬하여 추천 영화 목록을 구성

<hr>

#### 시행착오와 해결 과정
1. 추천 알고리즘 제작<br>
TMDB에서 영화의 리뷰와 키워드를 가져와서 Word2Vec 라이브러리를 사용해 임베딩 벡터로 가공하여 유사한 영화를 찾는데 사용하려고 했었지만, 리뷰나 키워드가 없는 영화도 많고 데이터의 양이 충분하지 않아 계속 오류가 발생했음<br>
그래서 임베딩 벡터를 사용하여 코사인 유사도를 측정하는 방법 대신 키워드 간의 자카드 유사도를 측정하여 유사한 영화를 찾아서 사용했음<br>
* 자카드 유사도 : 두 집합의 교집합 크기를 합집합 크기로 나눈 값으로 공통성을 측정하는 방법, 1에 가까울 수록 유사<br>

<br>

2. 백엔드 서버 배포<br>
SSAFY 공통 notion에 올라와 있는 aws를 사용한 서버 배포 방법을 사용했지만, 여러번 시도 했음에도 제대로 배포가 되지 않았음<br>
배포에 대해서 공부해본 적이 없기때문에 어떤 것이 문제인지도 파악이 되지 않아 aws를 사용한 배포를 포기함<br>
대신 좀 더 간단하게 배포가 가능하다는 heroku를 사용하고, 많은 자료들을 검색하며 하나씩 오류를 해결한 결과 배포에 성공할 수 있었음<br>

<hr>

#### 후기
프로젝트를 진행하며 어떻게 해야 좀 더 효율적으로 협업할 수 있을지 많은 고민을 하게 되었음<br>
기획했던 것을 중간에 수정하는 것은 이미 진행한 내용들을 변경하는데 많은 시간을 할애하게 만들기 때문에 처음부터 충분한 논의를 거쳐서 계획을 세우는 것의 중요성을 다시 한 번 느끼게 되었음<br>
모르는 것이나 해결하지 못하는 문제가 발생했을 때, 나의 상황에 맞는 해결방법을 찾기 위해서 어떤식으로 검색하고 자료를 찾아야 하는지 알게 되었음