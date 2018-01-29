from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from sean.users import models as user_models
from sean.images import models as image_models

class Notification(image_models.TimeStampedModel):

    TYPE_CHOICES = (
        ('like','Like'),
        ('commnet','Comment'),
        ('follow','Follow')
    )

    creator = models.ForeignKey(user_models.User, related_name='creator') #둘다 User이기 때문에 에러 발생하므로,related_name을 설정하여 서로 구분짓는다. 생성자는 그 알림을 만들어 내는사람
    to = models.ForeignKey(user_models.User, related_name='to') #to는 받는 사람
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES) #위에 만들어 놓은 Type_Choices를 가져다 쓴다.
    image = models.ForeignKey(image_models.Image, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self): #__str__ object가 어떻게 보이는지를 보여줌
        return '{} {}'.format(self.creator, self.to)