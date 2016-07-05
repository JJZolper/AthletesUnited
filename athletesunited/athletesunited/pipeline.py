import datetime
import urllib.request

from django.core.files.base import ContentFile
from django.contrib.auth.models import User, Group
from django.contrib.gis.geoip import GeoIP
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify

from athletesunited.athletes.models import Athlete, AthleteEmail
from athletesunited.communities.models import Community

def my_social_auth(backend, user, response, *args, **kwargs):
    g = GeoIP()
    if backend.name == 'twitter':
        isVerified = response.get('verified')
        # Pro / College Athlete
        if isVerified == True:
            if kwargs['is_new']:
                # Collect the athlete information
                imageurl = response.get('profile_image_url')
                twitter_screenname = response.get('screen_name')
                slug = slugify(twitterscreenname)
                birthday = '1111-11-11'
                language = 'en'
                # Set the collected information to the athlete
                # temp patch
                ip_address = '108.28.166.187'
                athleteCity = g.city(ip_address)['city']
                athleteCountry = g.country(ip_address)['country_name']
                CurrentCity = get_object_or_404(City, name = athleteCity)
                CurrentCountry = get_object_or_404(Country, name = athleteCountry)
                athlete = Athlete(user=user, slug = slug, birthday=birthday, language=language, twitter_screenname=twitter_screenname, is_verified=is_verified, ip_address = ip_address, current_city = CurrentCity, current_country = CurrentCountry)
                athlete.save()
                AthleteMainCommunity = Community.objects.get(name = "Athletes United")
                athlete.communities.add(AthleteMainCommunity)
                athlete.save()
                if imageurl:
                    avatar = urllib.request.urlopen(imageurl)
                    athlete.avatar.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar.read()))
                    athlete.save()
            else:
                pass
        # Athlete
        else:
            isVerified = False
            if kwargs['is_new']:
                # Collect the athlete information
                imageurl = response.get('profile_image_url')
                twitter_screenname = response.get('screen_name')
                slug = slugify(twitter_screenname)
                birthday = '1111-11-11'
                language = 'en'
                # Set the collected information to the athlete
                # temp patch
                ip_address = '108.28.166.187'
                athleteCity = g.city(ip_address)['city']
                athleteCountry = g.country(ip_address)['country_name']
                CurrentCity = get_object_or_404(City, name = athleteCity)
                CurrentCountry = get_object_or_404(Country, name = athleteCountry)
                athlete = Athlete(user=user, slug = slug, birthday=birthday, language=language, twitterscreenname=twitterscreenname, is_verified=is_verified, ip_address = ip_address, current_city = CurrentCity, current_country = CurrentCountry)
                athlete.save()
                AthleteMainCommunity = Community.objects.get(name = "Athletes United")
                athlete.communities.add(AthleteMainCommunity)
                athlete.save()
                if imageurl:
                    avatar = urllib.request.urlopen(imageurl)
                    athlete.avatar.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar.read()))
                    athlete.save()
            else:
                pass
    elif backend.name == 'facebook':
        isVerified = response.get('is_verified')
        # Pro / College Athlete
        if isVerified == True:
            if kwargs['is_new']:
                # Collect the athlete information
                imageurl = "http://graph.facebook.com/%s/picture?type=large" % response['id']
                birthday = '1111-11-11'
                first_name = response.get('first_name')
                last_name = response.get('last_name')
                email = response.get('email')
                slug = slugify(first_name + last_name)
                language = 'en'
                # Set the collected information to the athlete
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                # temp patch
                ip_address = '108.28.166.187'
                athleteCity = g.city(ip_address)['city']
                athleteCountry = g.country(ip_address)['country_name']
                current_city = get_object_or_404(City, name = athleteCity)
                current_country = get_object_or_404(Country, name = athleteCountry)
                athlete = Athlete(user=user, slug=slug, birthday=birthday, language=language, is_verified=is_verified, ip_address=ip_address, current_city=current_city, current_country=current_country)
                athlete.save()
                PrimaryAthleteEmail = AthleteEmail(athlete=user.athlete, email=user.email, is_verified=True)
                PrimaryAthleteEmail.save()
                AthleteMainCommunity = Community.objects.get(name = "Athletes United")
                athlete.communities.add(AthleteMainCommunity)
                athlete.save()
                if imageurl:
                    avatar = urllib.request.urlopen(imageurl)
                    athlete.avatar.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar.read()))
                    athlete.save()
            else:
                pass
        # Athlete
        else:
            isVerified = False
            if kwargs['is_new']:
                # Collect the athlete information
                imageurl = "http://graph.facebook.com/%s/picture?type=large" % response['id']
                # birthday = response.get('birthday')
                birthday = '1111-11-11'
                first_name = response.get('first_name')
                last_name = response.get('last_name')
                email = response.get('email')
                slug = slugify(first_name + last_name)
                language = 'en'
                # Set the collected information to the athlete
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                # temp patch
                ip_address = '108.28.166.187'
                athleteCity = g.city(ip_address)['city']
                athleteCountry = g.country(ip_address)['country_name']
                current_city = get_object_or_404(City, name = athleteCity)
                current_country = get_object_or_404(Country, name = athleteCountry)
                athlete = Athlete(user=user, slug=slug, birthday=birthday, language=language, is_verified=is_verified, ip_address=ip_address, current_city=current_city, current_country=current_country)
                athlete.save()
                PrimaryAthleteEmail = AthleteEmail(athlete=user.athlete, email=user.email, is_verified=True)
                PrimaryAthleteEmail.save()
                AthleteMainCommunity = Community.objects.get(name = "Athletes United")
                athlete.communities.add(AthleteMainCommunity)
                athlete.save()
                if imageurl:
                    avatar = urllib.request.urlopen(imageurl)
                    athlete.avatar.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar.read()))
                    athlete.save()
            else:
                pass



