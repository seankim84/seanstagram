from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    """ User Model """
    
    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female'),
        ('not-specified','Not-specified')
    )
    # First Name and Last Name do not cover name patterns
    # around the globe.
    profile_image = models.ImageField(null=True)
    name = models.CharField(_('Name of User'), blank=True, max_length=255) #name부분에 Name of User라 대신 쓴다.
    website = models.URLField(null=True)
    bio = models.TextField(null=True)
    phone = models.CharField(max_length = 140, null=True)
    gender = models.CharField(max_length = 80, choices=GENDER_CHOICES, null=True) 
    followers = models.ManyToManyField("self", blank=True) #팔로잉 팔로워 둘다 자기 자신을 지정한다.
    following = models.ManyToManyField("self", blank=True) #본인 유저 자신에게 연결해야 하기 때문이다.
    
    def __str__(self):
        return self.username

    @property
    def post_count(self):
        return self.images.all().count()
    @property
    def followers_count(self):
        return self.followers.all().count()
    @property
    def following_count(self):
        return self.following.all().count()
