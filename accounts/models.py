from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Genre

# Create your models here.

# Grade : 씨앗 / 새싹 / 꽃 or 브 / 실 / 골
class Grade(models.Model):
    title=models.CharField(max_length=30)
    # description=models.TextField()
    # icon=models.FileField()
    
    
class User(AbstractUser):
    # 추후에 필요한 컬럼 있으면 추가해서 새로 마이그레이션 해서 사용
    followings=models.ManyToManyField('self', symmetrical=False, related_name='followers')
    grade=models.ForeignKey(Grade, on_delete=models.CASCADE, default=1)
    like_genres=models.ManyToManyField(Genre, related_name='genre_like_users')
    isAdmin=models.BooleanField(default=False)
    profile_image=models.ImageField(blank=True, null=True)