import json

import stream_django
from stream_django import feed_manager
from stream_django.enrich import Enrich

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.gis.geoip import GeoIP
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import translation
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from athletesunited.athletes import signals
from athletesunited.athletes.forms import *
from athletesunited.athletes.models import *
from athletesunited.communities.models import Community, Country, City

# AU Athletes
def Athletes(request):
    return render(request, 'athletes.html')

# AU Athlete
@login_required
def AthletePage(request, athleteslug):
    context_data = {}
    SelectedAthlete = get_object_or_404(Athlete, slug = athleteslug)
    # test
    feed_manager.follow_user(request.user.id, SelectedAthlete.user.id)
    # test
    enricher = Enrich()
    feed = feed_manager.get_user_feed(SelectedAthlete.user.id)
    activities = feed.get(limit=3600)['results']
    enricher.enrich_activities(activities)
    athlete_community_list = SelectedAthlete.communities.all()
    context_data = {
        'Athlete': SelectedAthlete,
        'AthleteCommunities': athlete_community_list,
        'activities': activities
    }
    return render(request, 'athlete/athlete.html', context_data)

def follow_user(request, user_profile_id):
    contextdata = {}
    SelectedAthlete = get_object_or_404(Athlete, pk=user_profile_id)
    feed_manager.follow_user(request.user.id, SelectedAthlete.id)
    data['message'] = "You are now following {}".format(profile_to_follow)
    return JsonResponse(data, safe=False)

# AU Athlete Follow
@login_required
def AthleteFollow(request):
    form = FollowForm(request.POST)
    if form.is_valid():
        follow = form.instance
        follow.user = request.user
        follow.save()
    return redirect('Athletes')

# AU Athlete Unfollow
@login_required
def AthleteUnfollow(request, target_id):
    follow = Follow.objects.filter(user=request.user, target_id=target_id).first()
    if follow is not None:
        follow.delete()
    return redirect('Athletes')

# AU Athlete Registration
def AthleteRegistration(request):
    contextdata = {}
    if request.user.is_authenticated():
        return redirect('ProfileEdit')
    g = GeoIP()
    ip_address = request.META.get("REMOTE_ADDR", None)
    # TODO: Remove at launch
    # Vienna
    ip_address = '108.28.166.187'
    athleteCountry = g.country(ip_address)['country_name']
    # Can Register
    if athleteCountry == 'United States':
        if request.method == 'POST':
            form = AthleteRegistrationForm(request.POST)
            if form.is_valid():
                # ******* Need to add the below email to the Athlete's AthleteEmail list!!! *******
                email = form.cleaned_data['email']
                # ******* Need to add the above email to the Athlete's AthleteEmail list!!! *******
                username = form.cleaned_data['username']
                slug = slugify(username)
                password = form.cleaned_data['password']
                if Site._meta.installed:
                    site = Site.objects.get_current()
                else:
                    site = RequestSite(request)
                user = RegistrationProfile.objects.create_inactive_user(username, email, password, site)
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                # Vienna, United States
                ip_address = '108.28.166.187'
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                athleteCity = g.city(ip_address)['city']
                CurrentCity = get_object_or_404(City, name = athleteCity)
                CurrentCountry = get_object_or_404(Country, name = athleteCountry)
                athlete = Athlete(user=user, slug = slug, language = 'en', ip_address = ip_address, current_city = CurrentCity, current_country = CurrentCountry)
                athlete.save()
                AthleteMainCommunity = Community.objects.get(name = "Athletes United")
                athlete.communities.add(AthleteMainCommunity)
                for community in communities:
                    athlete.communities.add(community)
                for country in countries:
                    athlete.countries.add(country)
                for city in cities:
                    athlete.cities.add(city)
                athlete.save()
                # signals.user_registered.send(sender=self.__class__, user=new_user, request=request)
                return render(request, 'registration/registration_complete.html', contextdata)
            else:
                print(form.errors) # To see the form errors in the console.
        else:
            form = AthleteRegistrationForm()
            contextdata = {
                'form': form,
                'CanRegister': True
            }
            return render(request, 'athlete/athleteregistration.html', contextdata)
    else:
        # Cannot Register
        contextdata = {
            'CanRegister': False
        }
        return render(request, 'athlete/athleteregistration.html', contextdata)

# AU Athlete Registration Activation
class ActivationView(TemplateView):
    http_method_names = ['get']
    template_name = 'registration/activate.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(request, *args, **kwargs)
        if activated_user:
            signals.user_activated.send(sender=self.__class__, user=activated_user, request=request)
            success_url = self.get_success_url(request, activated_user)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        return super(ActivationView, self).get(request, *args, **kwargs)

    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.
        
        """
        activated_user = RegistrationProfile.objects.activate_user(activation_key)
        if activated_user:
            signals.user_activated.send(sender=self.__class__, user=activated_user, request=request)
        return activated_user

    def get_success_url(self, request, user):
        PrimaryAthleteEmail = AthleteEmail(athlete=user.athlete, email=user.email, is_verified=True)
        PrimaryAthleteEmail.save()
        return ('registration_activation_complete', (), {})

# AU Athlete Login
def AthleteLogin(request):
    contextdata = {}
    if request.user.is_authenticated():
        return redirect('Profile')
    form = AthleteLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.authenticate_user()
        if user.is_active == False:
            contextdata = {
                'form': form,
                'LoginError': "You cannot login. Your account has been locked."
            }
            return render(request, 'athlete/athletelogin.html', contextdata)
        else:
            login(request, user)
            return redirect('Home')
    else:
        contextdata = {
            'form': form
        }
        return render(request, 'athlete/athletelogin.html', contextdata)

# AU Athlete Logout
def AthleteLogout(request):
    logout(request)
    return redirect('AthleteLogin')

# AU Athlete Profile
@login_required
def Profile(request):
    contextdata = {}
    return render(request, 'athlete/profile.html', contextdata)

# AU Athlete Profile Edit
@login_required
def ProfileEdit(request):
    contextdata = {}
    SelectedAthlete = get_object_or_404(Athlete, id=request.user.athlete.id)
    if request.method == 'POST':
        userprofileupdateform = UserProfileUpdateForm(request.POST, instance=request.user)
        athleteprofileupdateform = AthleteProfileUpdateForm(request.POST, request.FILES, instance=SelectedAthlete)
        if userprofileupdateform.is_valid() and athleteprofileupdateform.is_valid():
            username = userprofileupdateform.cleaned_data['username']
            SelectedAthlete.slug = slugify(username)
            userprofileupdateform.save()
            athleteprofileupdateform.save()
            SelectedAthlete.save()
            return redirect('Profile')
        else:
            return redirect('Profile')
    else:
        SelectedLanguageCode = SelectedAthlete.language          # i.e. en for English
        LANGUAGESLIST = settings.LANGUAGES
        SelectedAthleteLocation = SelectedAthlete.current_city.name + ", " + SelectedAthlete.current_country.short
        user = request.user
        profile = user.profile
        userprofile = UserProfileUpdateForm(instance = user)
        athleteprofile = AthleteProfileUpdateForm(instance = profile)
        AthleteEmails = AthleteEmail.objects.filter(athlete = SelectedAthlete)
        contextdata = {
            'AthleteEmails': AthleteEmails,
            'SelectedLanguageCode': SelectedLanguageCode,
            'LANGUAGES': LANGUAGESLIST,
            'SelectedAthleteLocation': SelectedAthleteLocation,
            'AthleteProfileUpdateForm': athleteprofile,
            'UserProfileUpdateForm': userprofile
        }
        return render(request, 'athlete/profileedit.html', contextdata)

# AU Athlete Profile Edit Emails
@login_required
def ProfileEditEmails(request):
    contextdata = {}
    SelectedAthlete = get_object_or_404(Athlete, id=request.user.athlete.id)
    if request.method == 'POST':
        # Updating the existing email account information
        if 'update_emails' in request.POST:
            form = AthleteProfileEditUpdateEmailForm(request.POST, instance=SelectedAthlete)
            if form.is_valid():
                primaryathleteemail = form.cleaned_data['emails']
                user = request.user
                user.email = primaryathleteemail.email
                user.save()
                return redirect('ProfileEdit')
        # Adding new email account information
        if 'add_email' in request.POST:
            form = AthleteProfileEditAddEmailForm(request.POST, instance=SelectedAthlete)
            if form.is_valid():
                email = form.cleaned_data['email']
                NewAthleteEmail = AthleteEmail(athlete=SelectedAthlete, email=email, is_verified=False)
                NewAthleteEmail.save()
                return redirect('ProfileEdit')
    else:
        athleteprofileeditupdateemailform = AthleteProfileEditUpdateEmailForm(instance=SelectedAthlete)
        athleteprofileeditupdateemailform.fields['emails'].queryset = AthleteEmail.objects.filter(athlete=SelectedAthlete)
        athleteprofileeditupdateemailform.fields['emails'].initial = get_object_or_404(AthleteEmail, email=request.user.email)
        athleteprofileeditaddemailform = AthleteProfileEditAddEmailForm()
        contextdata = {
            'AthleteProfileEditUpdateEmailForm': athleteprofileeditupdateemailform,
            'AthleteProfileEditAddEmailForm': athleteprofileeditaddemailform
        }
        return render(request, 'athlete/profileeditemails.html', contextdata)

# AU Athlete Profile Edit Set Language Success
@login_required
def ProfileEditSetLanguageSuccess(request):
    contextdata = {}
    SelectedAthlete = get_object_or_404(Athlete, id=request.user.athlete.id)
    SelectedAthlete.language = request.session[translation.LANGUAGE_SESSION_KEY]
    SelectedLanguageCode = SelectedAthlete.language          # i.e. en for English
    translation.activate(SelectedLanguageCode)
    request.session[translation.LANGUAGE_SESSION_KEY] = SelectedLanguageCode
    SelectedAthlete.save()
    LANGUAGESLIST = settings.LANGUAGES
    contextdata = {
        'SelectedLanguageCode': SelectedLanguageCode,
        'LANGUAGES': LANGUAGESLIST
    }
    return render(request, 'athlete/profileeditsetlanguagesuccess.html', contextdata)

# AU Athlete Profile Edit Set Location Success
@login_required
def ProfileEditSetLocationSuccess(request):
    g = GeoIP()
    contextdata = {}
    ip_address = request.META.get("REMOTE_ADDR", None)
    # TODO: Remove at launch
    # Vienna
    ip_address = '108.28.166.187'
    # Mountain View
    # ip_address = '72.14.207.99'
    athleteCity = g.city(ip_address)['city']
    athleteCountry = g.country(ip_address)['country_name']
    CurrentCity = get_object_or_404(City, name = athleteCity)
    CurrentCountry = get_object_or_404(Country, name = athleteCountry)
    SelectedAthlete = get_object_or_404(Athlete, id=request.user.athlete.id)
    SelectedAthlete.current_city = CurrentCity
    SelectedAthlete.current_country = CurrentCountry
    SelectedAthlete.save()
    SelectedAthleteLocation = SelectedAthlete.current_city.name + ", " + SelectedAthlete.current_country.short
    contextdata = {
        'SelectedAthleteLocation': SelectedAthleteLocation
    }
    return render(request, 'athlete/profileeditsetlocationsuccess.html', contextdata)






