from rest_framework import serializers
from . import models
from sean.images import serializers as images_serializers


class UserProfileSerializer(serializers.ModelSerializer):

    images = images_serializers.CountImageSerializer(many=True, read_only=True)
    post_count = serializers.ReadOnlyField() #ReadOnlyField = 해당 필드들을 수정하지 않는다(user가 수정 불가).그냥 model의 property 이기 떄문에.
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    class Meta:
        model = models.User
        fields = ('profile_image', 'username', 'name', 'bio', 'website',
                  'post_count', 'following_count', 'followers_count', 'images')


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name'
        )