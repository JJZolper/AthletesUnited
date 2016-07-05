from django.conf.urls import include, url

from athletesunited.main import views as main_views

urlpatterns = [
    url(r'^$', main_views.Home, name='Home'),
    url(r'^design/$', main_views.Design, name='Design'),
    url(r'^about/$', main_views.About, name='About'),
    url(r'^about/(?P<teammemberreq>[a-zA-Z0-9]+)/$', main_views.TeamMemberPage, name='TeamMemberPage'),
    url(r'^feedback/$', main_views.GiveFeedback, name='GiveFeedback'),
    url(r'^spam/$', main_views.ReportSpam, name='ReportSpam'),
    url(r'^privacyandterms/$', main_views.PrivacyAndTerms, name='PrivacyAndTerms'),
    url(r'^contactus/$', main_views.ContactUs, name='ContactUs'),
    url(r'^comments/', include('athletesunited.comments.urls')),
    url(r'^store/$', main_views.Store, name='Store'),
    url(r'^spam/communityposts/(?P<communitypostid>[a-zA-Z0-9]+)/$', main_views.ReportCommunityPostSpam, name='ReportCommunityPostSpam'),
]




