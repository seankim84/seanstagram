from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex = r'^$', #^$ 뜻은 index 이다.
        view = views.Notifications.as_view(),  #image들은 그냥 클래스이기 때문에 view()를 해줘야한다.
        name = 'notifications'
    ),
]