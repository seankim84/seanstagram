from django.db import models
from django.utils.encoding import python_2_unicode_compatible #python2 의 유니코드 불러옴
from taggit.managers import TaggableManager
from sean.users import models as user_models #as 라는 닉네임을 만들어서 같은 models와의 충돌을 방지한다.

# Create your models here.
@python_2_unicode_compatible #compatible = "호환이 되는"
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True) #우리가 원할때마다 추가, 모델이 처음 생성되었을때
    updated_at = models.DateTimeField(auto_now=True) # 새로고침

    class Meta: #위의 클래스(TimeStampedModel)가 abstract 임을 알려줌
        abstract = True #Meta class는 반드시 abstract = True 가 되어야 한다.

@python_2_unicode_compatible
class Image(TimeStampedModel): #TimeStampedModel 의 확장, 딱히 default를 지정해줄 필요 없다
    
    """ Image Model """

    file = models.ImageField() #Image file
    location =  models.CharField(max_length=140) #지역정보
    caption = models.TextField() #캡션
    creator = models.ForeignKey(user_models.User , null=True, related_name='images')
    tags = TaggableManager()

    @property
    def like_count(self):#본인의 이미지에 접근하고 싶으므로 self사용
        return self.likes.all().count() 
        
    @property
    def comment_count(self):
        return self.comments.all().count()

    def __str__(self): #String Representation(Object가 어떻게 보이는지 결정)
        return '{} - {}'.format(self.location, self.caption)  # admin에서 location 과 caption을 보여준다

    class Meta:
        ordering = ['-created_at'] #생성된 날짜 순으로 정렬(가장최근순으로), 메타클래스는 이처럼 모델의 설정을 위해 사용한다.

@python_2_unicode_compatible
class Comment(TimeStampedModel): #TimeStampedModel 의 확장, 딱히 default를 지정해줄 필요 없다

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(user_models.User , null=True)
    image = models.ForeignKey(Image , null=True, related_name='comments') #Comment 가 달린 Image의 ForeignKey
    #related_name=None -> 디폴트로 연결된 이름은 위에서 사용한 set 이다.

    def __str__(self): #String Representation(Object가 어떻게 보이는지 결정)
        return self.message #admin에서 message를 보여준다.

@python_2_unicode_compatible
class Like(TimeStampedModel):

    """ Like Model """

    creator = models.ForeignKey(user_models.User , null=True) #좋아요 누른사람의 Foreign Key를 지정
    image = models.ForeignKey(Image , null=True, related_name='likes') #좋아요 받은 이미지의 Foreign Key

    def __str__(self): #Foreign Key에 접근하는 방법은 python object notation 이다.
        return 'User: {} - Image Caption: {}'.format(self.creator.username, self.image.caption) #username은 여기에 정의되있지 않고, AbstractUser에 정의되어있다.