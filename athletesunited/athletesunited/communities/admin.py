from django.contrib import admin

from athletesunited.communities.models import Community, Country, City
from athletesunited.communities.models import CommunityPost

admin.site.register(Community)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(CommunityPost)





