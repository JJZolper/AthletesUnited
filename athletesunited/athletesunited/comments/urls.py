from django.conf.urls import patterns, url

from django.contrib.contenttypes import views as django_views

from athletesunited.comments.views import comments as comments_views
from athletesunited.comments.views import moderation as moderation_views

urlpatterns = [
    url(r'^post/ajax/$', comments_views.post_comment_ajax, name='post_comment_ajax'),

    url(r'^flag/(\d+)/$', moderation_views.flag, name='flag'),
    url(r'^flagged/$', moderation_views.flag_done, name='flag_done'),
    url(r'^delete/(\d+)/$', moderation_views.delete, name='delete'),
    url(r'^deleted/$', moderation_views.delete_done, name='delete_done'),
    url(r'^approve/(\d+)/$', moderation_views.approve, name='approve'),
    url(r'^approved/$', moderation_views.approve_done, name='approve_done'),
               
    url(r'^cr/(\d+)/(.+)/$', django_views.shortcut, name='url_redirect'),
]





