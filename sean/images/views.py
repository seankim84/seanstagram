from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  #HTTP Status를 불러온다.
from sean.users import models as user_models
from sean.users import serializers as user_serializers
from . import models, serializers  #같은 dir에서 models 전체를 불러온다.
from sean.notifications import views as notification_views


class Images(APIView):
    def get(self, request, format=None):

        user = request.user

        following_users = user.following.all()  #following은 manyTomany Field 이다. #내 유저가 following하는 유저의 list를 얻기위함.

        image_list = []

        for following_user in following_users:  #앞의 following_users는 그저 variable 이기 때문에 potato라 써도 무관.

            user_images = following_user.images.all(
            )[:2]  #[:2] 모델 케이스 제한, 이제 이 list들을 더 큰 리스트 안에 넣어야한다.

            for image in user_images:

                image_list.append(image)

        my_images = user.images.all()[:2]

        for image in my_images:

            image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)

        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)  #status보내는 대신에 serializer 데이터를 보냄

    def post(self, request, format=None):

        user = request.user #생성자가 유저와 동일함을 알려준다.

        serializer = serializers.InputImageSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user) #model 참조

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeImage(APIView):

    def get(self, request, image_id, format=None): # 1. likes를 긁어온다. 2. likes 안에서 생성자를 긁어온다. 3.유저모델 데이터베이스 안에서 해당 좋아요를 생성한 유저를 찾는다.

        likes = models.Like.objects.filter(image_id=image_id) # url이 id 숫자를 주면 해당 숫자를 갖고 있는 좋아요를 찾는다.

        like_creators_ids = likes.values('creator_id')

        users = user_models.User.objects.filter(id__in=like_creators_ids) # in = array 안에 있는 user id를 검색

        serializer = user_serializers.ListUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, image_id, format=None):  #urls.py 에 image_id 가 있다면, 여기에도 image_id가 있어야 한다.

        user = request.user

        #create notifications

        try:  #try로 해당코드를 하려고 시도한다.
            found_image = models.Image.objects.get(
                id=image_id
            )  #get 대신에 all() 혹은 filter()가 될 수 있다. 1개만 보고싶기 떄문에 get을 사용한다.

        except models.Image.DoesNotExist:  #위의 try 를 할 수 없는 경우,excpt 실행
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )  #function이 무언가를 return하면, 그 순간 function 작업은 끝이 난다.

        try:  #이미 존재하는 image가 있으면 삭제하라고 함
            preexisiting_like = models.Like.objects.get(  #get이 오는것 중요!!
                creator=user, image=found_image)

            return Response(
                status=status.HTTP_304_NOT_MODIFIED)  #204= 내용이 없음을 보여줌

        except models.Like.DoesNotExist:  # 좋아요가 없으면 좋아요 생성
            new_like = models.Like.objects.create(
                creator=user, image=found_image)

            new_like.save()

            notification_views.create_notification(user, found_image.creator,
                                                   'like', found_image)

            return Response(status=status.HTTP_201_CREATED)


class UnLikeImage(APIView):
    def delete(self, request, image_id, format=None):

        user = request.user

        try:
            preexisiting_like = models.Like.objects.get(
                creator=user, image__id=image_id)
            preexisiting_like.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Like.DoesNotExist:

            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):  #자기가 만든 댓글만 삭제가 가능해야함
    def post(self, request, image_id, format=None):

        user = request.user

        #create notifications

        try:
            found_image = models.Image.objects.get(id=image_id)

        except models.Image.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user, image=found_image)

            notification_views.create_notification(user, found_image.creator, 'comment', found_image, serializer.data['message'])

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:

            return Response(data=serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class Comment(APIView):

    def delete(self, request, comment_id, format=None):

        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

class Search(APIView):

    def get(self, request, format=None):

        hashtags = request.query_params.get('hashtags', None) #parmas가 여러개라도 get으로 가져올 수 있다.

        if hashtags is not None: #query prameter에 'hash'태그가 없다면 오류가 뜬다.=None split

            hashtags = hashtags.split(",") #params array 생성

            images = models.Image.objects.filter(tags__name__in=hashtags).distinct() #deep relationship을 검색하는 방법, distinct() => 검색결과가 겹치지 않게 해준다.

            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)

class ModerateComments(APIView):

    def delete(self, request, image_id, comment_id, format=None):

        user = request.user

        try :
            comment_to_delete = models.Comment.objects.get(
                id=comment_id, image__id=image_id, image__creator=user)
            comment_to_delete.delete()

        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

class ImageDetail(APIView):

    def find_own_image(self, image_id, user):

        try:
            image = models.Image.objects.get(id=image_id, creator=user) # creator=user 가 없으면 누구이미지든 관계없이 삭제할 수 있다.
            return image
        except models.Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):

        user = request.user

        try:
            image = models.Image.objects.get(id=image_id) #남이 만든 image도 볼 수 있어야 되기에, creator를 없앤다.

        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ImageSerializer(image)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, image_id, format=None): #put은 업데이트 전용. 이미지 편집!(내가 생성한 것만)

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None :
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            image = models.Image.objects.get(id = image_id, creator = user)

        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.InputImageSerializer(image, data = request.data, partial=True) #serializer의 3가지 필드를 모두 충족시키지 않아도 괜찮다. 즉 부분적으로 수정이 가능하다.

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response(
                data=serializer.data, status=status.HTTP_204_NO_CONTENT)

        else:

            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, image_id, format=None):

        user = request.user    

        image = self.find_own_image(image_id, user)

        if image is None :
            return Response(status=status.HTTP_400_BAD_REQUEST)

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)