# Heroku 서버 배포 방법

1. manage.py파일이 있는 위치에 Procfile, runtime.txt 생성<br>

    ##### Procfile
    ```markdown
    web: gunicorn {프로젝트 이름}.wsgi --log-file -
    ```

    ##### runtime.txt
    ```markdown
    python-{프로젝트에서 사용한 버전}

    e.g
    python-3.9.13
    ```

    <br>


2. django 라이브러리 설치
    ```markdown
    pip install django-heroku

    pip install whitenoise

    pip install dj-database-url

    pip install gunicorn
    ```
    <br>

3. settings.py 추가 작성<br>
    `DEBUG=True` 에서 `Debug=False`로 변경<br>

    DATABASES 변경
    ```python
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config(default='sqlite:///:memory:')
    }
    ```

    <br>

    MIDDLEWARE에 항목 추가<br>
    securityMiddleWare항목 밑에 추가해줘야 함
    `'whitenoise.middleware.WhiteNoiseMiddleware',`
    <br>

    `STATIC_ROOT = BASE_DIR / 'staticfiles'` 항목 추가 후<br>
    `python manage.py collectstatic`으로 staticfiles 디렉토리 생성<br>
    <br>

4. heroku-cli 설치<br>
    <https://devcenter.heroku.com/articles/heroku-cli>
    <br>

5. heroku 회원가입<br>

6. 터미널 창에서 명령어 입력<br>
    ```markdown
    heroku login : 회원가입 한 계정으로 로그인 진행

    heroku create {앱 이름} : 해당 앱 이름으로 도메인 생성됨

    heroku git:remote -a {앱 이름} : 생성한 앱의 이름을 입력

    git push heroku master 또는 main : 둘중 에러가 발생하지 않는 곳으로 push

    heroku run python manage.py migrate

    heroku run python manage.py loaddata : loaddata할 json파일이 있을 경우 진행

    heroku open : 404페이지나 ''주소에서의 api가 나온다면 배포 성공
    ```

    만약 프로젝트에서 .env파일을 사용해서 api key들을 관리하고 있다면
    heroku에서 생성한 app의 settings에서 Config Vars항목에서 key와 value를 입력해줌
    그러지 않을 경우 제대로 push되지 않고 에러가 발생
    <br>

7. 추가 명령어<br>
    ```markdown
    heroku ps:scale web=0 : 배포한 서버 종료

    heroku ps:scale web=1 : 서버 다시 열기

    heroku destroy : 서버 삭제(앱 삭제)
    ```