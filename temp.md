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
| accounts | X | POST | logout/ | 로그아웃 |
| accounts | O | POST | password/change/ | 회원가입 |

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
