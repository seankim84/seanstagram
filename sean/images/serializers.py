from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,TaggitSerializer)
from . import models
from sean.users import models as user_models


class SmallImageSerializer(serializers.ModelSerializer):

    """ Used for notifications """

    class Meta:
        model = models.Image
        fields = ('file', )


class CountImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count'
        )

class FeedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = ('username', 'profile_image')


class CommentSerializer(serializers.ModelSerializer):
    creator = FeedUserSerializer(read_only=True)

    #image = ImageSerializer()

    class Meta:
        model = models.Comment
        fields = ('id', 'message',
                  'creator')  #id는 read only field이기 때문에 바꿀 수 없다.


class LikeSerializer(serializers.ModelSerializer):

    #image = ImageSerializer()  #nested serializer 생성, 우선 네이밍을 먼저 해준다.

    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(TaggitSerializer, serializers.ModelSerializer):  #Serializer에서 확장됨

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = models.Image
        fields = ('id', 'file', 'location', 'caption', 'comments',
                  'like_count', 'creator', 'tags', 'created_at')
        #fields = '__all__'  # 전체 field

class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'file',
            'location',
            'caption',

        )