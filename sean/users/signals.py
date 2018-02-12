from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from io import BytesIO
from urllib.request import urlopen
from django.core.files import File


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs): # 유저가 가입을 하면 유저정보(user)를 얻게된다.
    if len(user.socialaccount_set.all()) > 0: #이 social account의 아래와 같은 정보를 가지고 오고 싶다.(social account는 forign key이다.)
        social_account = user.socialaccount_set.all()[0]
        uid = social_account.uid
        gender = social_account.extra_data.get('gender', None) # 소셜계정의 정보 추출
        user.gender = gender
        avatar = social_account.get_avatar_url()  #아바타를 가지고 와서
        avatar_image = urlopen(avatar)  #이미지를 열고
        io = BytesIO(avatar_image.read())
        user.profile_image.save('{}.jpg'.format(uid), File(io)) #이미지를 저장한다.
        user.name = user.get_full_name()
    user.save() # 마지막엔 유저 저장
