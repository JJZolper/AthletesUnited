from django.conf.urls import url
from athletesunited.communities.api.views import CommunityPostList

urlpatterns = [
    # Communities API
    url(r'^communityposts/$', CommunityPostList.as_view(), name='communitypost-list'),
]




