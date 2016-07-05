import stream_django
from stream_django import feed_manager
from stream_django.enrich import Enrich
from stream_django.activity import Activity

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

# Community
@python_2_unicode_compatible
class Community(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=100, blank=True, default="")
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'

    def __str__(self):
        return str(self.name)

# Country
@python_2_unicode_compatible
class Country(models.Model):
    name = models.CharField(max_length=100, default="")
    short = models.CharField(max_length=100, default="")
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
    
    def __str__(self):
        return str(self.name)

# City
@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(max_length=100, default="")
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
    
    def __str__(self):
        return str(self.name)

# Community Post
@python_2_unicode_compatible
class CommunityPost(Activity, models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name="%(class)s_posts")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    community = models.ForeignKey(Community, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    verified_users = models.ManyToManyField(User, blank=True)
    spam_count = models.IntegerField(default=0, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Community Post'
        verbose_name_plural = 'Community Posts'
    
    def __str__(self):
        return str(self.body)
    
    @property
    def print_self(self):
        print(self.body)
    
    @property
    def activity_object_attr(self):
        return self
    
    def save(self):
        super(CommunityPost, self).save()
    
    @property
    def activity_notify(self):
        targets = []
        '''
        if self.community is not None:
            targets.append(feed_manager.get_feed('communitypost', self.community.name.replace(" ", "_")))
        '''
        if self.city is not None:
            targets.append(feed_manager.get_feed('citypost', self.city.name.replace(" ", "_")))
        return targets

# Community Post Hashtag
class Hashtag(models.Model):
    name = models.CharField(max_length=160)
    occurrences = models.IntegerField(default=0)




