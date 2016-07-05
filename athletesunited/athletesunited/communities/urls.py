from django.conf.urls import include, url
from athletesunited.communities import views as communities_views

urlpatterns = [
    url(r'^communities/$', communities_views.Communities, name='Communities'),
    url(r'^communities/myconversations/$', communities_views.CommunityMyConversations, name='communities-views-CommunityMyConversations'),
    url(r'^communities/topic/(?P<communityslug>[a-zA-Z]+)/posts/cities/(?P<cityslug>[a-zA-Z]+)/$', communities_views.CommunityCityPostPage, name='communities-views-CommunityCityPostPage'),
    url(r'^communities/location/cities/$', communities_views.CityCommunities, name='communities-views-CityCommunities'),
    url(r'^communities/location/cities/(?P<cityslug>[a-zA-Z]+)/posts/$', communities_views.CityCommunityPostPage, name='communities-views-CityCommunityPostPage'),
    url(r'^search/$', communities_views.Search_Communities_AJAX, name='communities-views-Search_Communities_AJAX'),
    url(r'^search-results/$', communities_views.Search_Community_Results, name='communities-views-Search_Community_Results'),
    # API
    url(r'^api/', include('athletesunited.communities.api.urls')),
]




