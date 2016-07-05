from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Team Member
@python_2_unicode_compatible
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    avatar = models.ImageField("Team Member Picture", upload_to="images/teammember/", blank=True, null=True, default='images/no-profile-photo.jpg')
    bio = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return str(self.name)

