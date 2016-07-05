from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from athletesunited.athletes.views import ActivationView
from athletesunited.athletes import views as athletes_views

urlpatterns = [
    url(r'^athletes/$', athletes_views.Athletes, name='Athletes'),
    url(r'^athletes/(?P<athleteslug>[-a-zA-Z0-9_]+)/$', athletes_views.AthletePage, name='athletes-views-AthletePage'),
    url(r'^follow/$', athletes_views.AthleteFollow, name='AthleteFollow'),
    url(r'^unfollow/(?P<target_id>[-a-zA-Z0-9_]+)/$', athletes_views.AthleteUnfollow, name='AthleteUnfollow'),
    url(r'^register/$', athletes_views.AthleteRegistration, name='AthleteRegistration'),
    url(r'^register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'), name='registration_complete'),
    url(r'^activate/complete/$', TemplateView.as_view(template_name='registration/activation_complete.html'), name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^login/$', athletes_views.AthleteLogin, name='AthleteLogin'),
    url(r'^logout/$', athletes_views.AthleteLogout, name='AthleteLogout'),
    url(r'^password/change/$', auth_views.password_change, name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[a-zA-Z0-9]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^profile/$', athletes_views.Profile, name='Profile'),
    url(r'^profile/edit/$', athletes_views.ProfileEdit, name='ProfileEdit'),
    url(r'^profile/edit/emails/$', athletes_views.ProfileEditEmails, name='ProfileEditEmails'),
    url(r'^profile/edit/setlanguage/success/$', athletes_views.ProfileEditSetLanguageSuccess, name='ProfileEditSetLanguageSuccess'),
    url(r'^profile/edit/setlocation/success/$', athletes_views.ProfileEditSetLocationSuccess, name='ProfileEditSetLocationSuccess'),
    url('', include('social.apps.django_app.urls', namespace='social')),
]




