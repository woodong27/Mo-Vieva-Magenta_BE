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
- 개발 환경(Back-end)
    - Python<br>
    - Django 3.2.18<br>
    - Django REST Framework

<hr>

#### URL

|App|Authorization|Method|url|설명|
|:---:|:---:|:---:|:---:|:---:|
| accounts | X | POST | signup/ | 회원가입 |
| accounts | X | POST | login/ | 로그인 |
| accounts | O | POST | logout/ | 로그아웃 |
| accounts | O | POST | password/change/ | 회원가입 |
| accounts | O | POST | admin/ | 관리자 권한 토글 |
| accounts | O | POST | genre/ | 선호 장르 선택 |
| accounts | O | GET | genre/ | 선택한 선호 장르 목록 |
| accounts | O | POST | grade/<int:grade_pk>/ | 유저 등급 변경 |
| accounts | O | POST | follow/<int:user_pk>/ | 해당 유저 follow/unfollow |
| accounts | O | GET | userinfo/ | 현재 로그인된 유저의 정보 |
| accounts | X | GET | <int:user_pk>/ | 해당 유저의 정보 |
| community | O | POST | create/ | article 작성<br>data로 tag, movie 등을 받을 수 있음 |
| community | O | POST | notice/ | 공지글 작성 |
| community | X | GET | list/ | 전체 article 목록 |
| community | X | GET | tag/<int:tag_pk>/ | 태그별 article 목록 |
| community | X | GET | id/<int:movieId>/ | 해당 영화와 관련된 article 목록<br>query string으로 tag 선택 가능 |
| community | X | GET | <int:article_pk>/ | article detail |
| community | O | PUT | <int:article_pk>/ | article 수정 |
| community | O | DELETE | <int:article_pk>/ | article 삭제 |
| community | O | POST | <int:article_pk>/upvote/ | article 추천 |
| community | O | POST | <int:article_pk>/downvote/ | article 비추천 |
| community | O | POST | <int:article_pk>/comment/ | article에 댓글 작성<br>isSecret에 따라서 비밀 댓글 작성 가능 |
| community | X | GET | <int:article_pk>/comment/ | article의 댓글 목록 |
| community | X | GET | comment/<int:article_pk>/ | 댓글 가져오기 |
| community | O | PUT | comment/<int:article_pk>/ | 댓글 수정 |
| community | O | PUT | comment/<int:article_pk>/ | 댓글 삭제 |
| community | O | POST | comment/<int:article_pk>/upvote/ | 댓글 추천 |
| community | O | POST | comment/<int:article_pk>/downvote/ | 댓글 비추천 |


<hr>

#### ERD
![final-pjt-erd](https://github.com/woodong27/SSAFY_Final/assets/122415763/b24c2b42-2aa1-45d5-92f4-ddd90e97c20b)

<hr>

#### 추천 알고리즘
유저마다 선택한 선호 장르와 좋아요/싫어요 표시한 영화를 바탕으로 컨텐츠 기반 필터링을 사용하여 추천 영화 목록을 구성하는 알고리즘<br>
좋아요/싫어요 표시한 영화가 존재하면 자카드 유사도를 계산해서 해당 영화들과 비슷한 영화들의 목록을 만들어서 사용하였음<br>
<br>
선택한 선호 장르와 중복되는 것이 많은 영화일수록 더 높은 가중치를 가지게 됨<br>
해당 영화가 좋아요 표시한 영화와 유사한 영화 목록에 있다면 가중치를 더해주고, 싫어요 표시한 영화와 유사한 영화 목록에 있다면 가중치를 감소시켜 줌<br>
모든 영화에 대해서 가중치가 계산되고 나면, 가중치를 바탕으로 영화를 내림차순 정렬하여 추천 영화 목록을 구성

<hr>

#### 시행착오와 해결 과정

<hr>

#### 후기
