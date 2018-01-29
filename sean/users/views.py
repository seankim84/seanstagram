from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  #HTTP Status를 불러온다.
from . import models, serializers  #같은 dir에서 models 전체를 불러온다.
from sean.notifications import views as notification_views
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class Users(APIView):
    pass


class ExploreUsers(APIView):
    def get(self, request, format=None):

        last_five = models.User.objects.all().order_by('-date_joined')[:5]

        serializer = serializers.ListUserSerializer(last_five, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowUser(APIView):
    def post(self, request, user_id, format=None):

        user = request.user

        #create notification

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)

        user.save()

        notification_views.create_notification(user, user_to_follow, 'follow')

        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):
    def post(self, request, user_id, format=None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)

        user.save()

        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):

    def get_user(self,username): #해당 유저와 사용자가 일치하는지를 본다. 일치하면 found_user을 Return

        try:
            found_user = models.User.objects.get(username=username)
            return found_user
        except models.User.DoesNotExist:
            return None

    def get(self, request, username, format=None):

        found_user = self.get_user(username) #위의 def 사용(found_user가 username과 같은지 확인)

        if found_user is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(found_user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, format=None): #userprofile을 수정 가능하도록 한다.

        user = request.user

        found_user = self.get_user(username) #위의 def 사용

        if found_user is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        elif found_user.username != user.username: #찾은 유저가 해당 페이지를 요청한 유저와 다르다면

            return Response(status=status.HTTP_401_UNAUTHORIZED) #해당 사용자가 아닌경우 권한을 주지 않는다.

        else: #위의 모든 사항에 해당이 안된다면 serializer 작업을 한다.

            serializer = serializers.UserProfileSerializer(found_user,data=request.data, partial = True) #partial을 사용하여, 부분적으로 수정이 가능하도록 한다.

            if serializer.is_valid(): #is_valid=내장되어있는 메서드

                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_200_OK)

            else:

                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFollowers(APIView):
    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followers = found_user.followers.all()

        serializer = serializers.ListUserSerializer(user_followers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowing(APIView):
    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_following = found_user.following.all()

        serializer = serializers.ListUserSerializer(user_following, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class Search(APIView):
    def get(self, request, format=None):

        username = request.query_params.get('username',None)

        if username is not None:

            users = models.User.objects.filter(username__istartswith=username)

            serializer = serializers.ListUserSerializer(users, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):

    def put(self, request, username, format=None):

        user = request.user

        if user.username == username: # 요청하는 유저가 url 유저와 동일한지 확인

            current_password = request.data.get('current_password', None)  #현재 비밀번호가 request.data를 통해 오는지 체크

            if current_password is not None:

                passwords_match = user.check_password(current_password)  #현재 비번과 해당 비번이 일치하는지 체크(check_password를 통해->function인데, 유저모델의 기능이다.)

                if passwords_match:

                    new_password = request.data.get('new_password', None)  #매칭이되면, 새로운비번을 request.data에서 얻는다.

                    if new_password is not None:

                        user.set_password(new_password)  #해당 비번이 존재하면, 이를 새로운 비번으로 설정

                        user.save()  # 저장

                        return Response(status=status.HTTP_200_OK)

                    else:

                        return Response(status=status.HTTP_400_BAD_REQUEST)

                else:

                    return Response(status=status.HTTP_400_BAD_REQUEST)

            else:

                return Response(status=status.HTTP_400_BAD_REQUEST)

        else:

            return Response(status=status.HTTP_401_UNAUTHORIZED)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
