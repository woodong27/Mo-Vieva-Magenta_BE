"""final_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie/', include('movies.urls')),
    path('community/', include('communities.urls')),
    
    # dj_rest_auth 인증 사용
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    
    # user grade변경
    path('accounts/grade/<int:grade_pk>/', account_views.gradeChange),
    
    # isAdmin 변경
    path('accounts/admin/', account_views.admin),
    
    # user 전체 정보 보내기
    path('accounts/userinfo/', account_views.userInfo),
    
    # 선호하는 장르 고르기
    path('accounts/genre/', account_views.genres),
    
    # 팔로우
    path('accounts/follow/<int:user_pk>/', account_views.follow),
    
    # 프로필 이미지 추가
    path('accounts/image/', account_views.upload_profile_image),
    
    # 유저 프로필 정보 가져오기
    path('accounts/<int:user_pk>/', account_views.profile),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
