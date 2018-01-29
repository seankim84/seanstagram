from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.Images.as_view(),  #image들은 그냥 클래스이기 때문에 view()를 해줘야한다.
        name='feed'),
    url(
        regex=r'^(?P<image_id>[0-9]+)/$',
        view=views.ImageDetail.as_view(),  #image들은 그냥 클래스이기 때문에 view()를 해줘야한다.
        name='feed'),
    url(
        regex=r'^(?P<image_id>[0-9]+)/likes/$',  #image_id를 요구하는 argument를 보냄
        view=views.LikeImage.as_view(),
        name='like_image'),
    url(
        regex=r'^(?P<image_id>[0-9]+)/unlikes/$',  #image_id를 요구하는 argument를 보냄
        view=views.UnLikeImage.as_view(),
        name='unlike_image'),
    url(
        regex=r'^(?P<image_id>[0-9]+)/comments/$',  #image_id를 요구하는 argument를 보냄
        view=views.CommentOnImage.as_view(),
        name='comment_image'),
    url(regex=r'^(?P<image_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$',
        view=views.ModerateComments.as_view(),
        name='comment_image'),
    url(
        regex=
        r'^comments/(?P<comment_id>[0-9]+)/$',  #image_id를 요구하는 argument를 보냄
        view=views.Comment.as_view(),
        name='comment'),
    url(
        regex=r'^search/$',  #image/search 이렇게 생겨야한다.
        view=views.Search.as_view(),
        name='search'),
]