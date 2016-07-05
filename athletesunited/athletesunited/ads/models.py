from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.utils.translation import ugettext_lazy as _

# Ad
@python_2_unicode_compatible
class Ad(models.Model):
    image = models.ImageField("Ad", upload_to="images/partners/", blank=True, null=True, default='')
    title = models.CharField(max_length=30, blank=True) # title
    web_url = models.URLField(max_length=100, blank=True)
    community = models.ForeignKey('communities.Community', blank=True, null=True)
    country = models.ForeignKey('communities.Country', blank=True, null=True)
    city = models.ForeignKey('communities.City', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'
    
    def __str__(self):
        return str(self.title)




