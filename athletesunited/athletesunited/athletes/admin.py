from django.contrib import admin

from athletesunited.athletes.models import Athlete, AthleteEmail, Follow, RegistrationProfile

admin.site.register(Athlete)
admin.site.register(AthleteEmail)
admin.site.register(Follow)
admin.site.register(RegistrationProfile)



