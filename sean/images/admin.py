from django.contrib import admin
from . import models # 같은 폴더에서 model을 import 한다
# Register your models here.
# class는 모델들이 어드민 패널에서 어떻게 보이는지 결정

@admin.register(models.Image) #위아래 간격을 비워두면 에러발생(꼭 붙여서 사용!)
class ImageAdmin(admin.ModelAdmin):
    
    list_display_links = (
        'location', #loaction 을 click 함으로써 이미지 편집을 가능하게 해준다.
        'caption' #caption 도 마찬가지
    )

    search_fields = (
        'loaction', #location으로 검색하고 싶다면, 검색바가 생성
        'caption' #caption 도 마찬가지
    )

    list_filter = (
        'location', #filter 작업
        'creator'
    )

    list_display = (
        'file', #쉼표가 없으면 error 가 발생할 수 있다.
        'location',
        'caption',
        'creator',
        'created_at',
        'updated_at'
    )

@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    
    list_display = (
        'creator',
        'image',
        'created_at',
        'updated_at'
    )

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ( #Comment에서 어떻게 보이는지 설정
        'message',
        'creator',
        'image',
        'created_at',
        'updated_at'
    )