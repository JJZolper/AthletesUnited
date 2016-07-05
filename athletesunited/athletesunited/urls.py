from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from athletesunited.dev_settings import DEBUG

urlpatterns = [
    # Django
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
               
    # AU
    url('', include('athletesunited.main.urls')),
     
    # AU Athletes
    url('', include('athletesunited.athletes.urls')),

    # AU Communities
    url('', include('athletesunited.communities.urls')),
    
    # AU Mobile Landing Page
    url(r'^mobile/$', TemplateView.as_view(template_name="mobile.html")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




