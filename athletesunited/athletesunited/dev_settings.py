from athletesunited.base_settings import *

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

# Athletes United Development
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'
DEFAULT_FROM_EMAIL = 'AU-NoReply <noreply@theathletesunited.com>'
SERVER_EMAIL = 'root@localhost'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition
INSTALLED_APPS = INSTALLED_APPS + (
    # AU
    'athletesunited.athletes.apps.AthletesConfig',
    'athletesunited.ads.apps.AdsConfig',
    'athletesunited.communities.apps.CommunitiesConfig',
    'athletesunited.comments.apps.CommentsConfig',
    'athletesunited.main.apps.MainConfig',
    # Third Party
    'social.apps.django_app.default',
    'stream_django',
    'rest_framework',
    # Development
    'debug_toolbar.apps.DebugToolbarConfig'
)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    # Not sure if I need the below
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'auusers',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'JJZ',
        'PASSWORD': 'MarlinMan33!',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_PATH + '/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # AU specific
                "athletesunited.templatecontextprocessor.AUPhaseManagement",
                "athletesunited.athletes.templatecontextprocessor.RenderAthleteAvatar",
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

LOCALE_PATHS = (
    'athletesunited/locale',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # athletesunited Static Home
    'athletesunited/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

GEOIP_PATH = PROJECT_PATH + '/geoipdata/'

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Español')),
)

# Third Party Apps Settings

# Amount of days before registration expires
ACCOUNT_ACTIVATION_DAYS = 7

# Third Party Apps Settings
LOGIN_URL = '/login/'
SOCIAL_AUTH_LOGIN_URL = '/login/'
SOCIAL_AUTH_LOGOUT_URL = '/logout/'
SOCIAL_AUTH_TWITTER_LOGIN_URL = '/login/twitter/'
SOCIAL_AUTH_FACEBOOK_LOGIN_URL = '/login/facebook/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login/error/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/profile/'

SOCIAL_AUTH_TWITTER_KEY = 'v5WFVxlOvGO2yppyj2PGbTn63'
SOCIAL_AUTH_TWITTER_SECRET = 'ZMO8Tor09i1NfpxXBLh5fnej9obubZ4h8GDr66SSlPNd2UmgPI'

SOCIAL_AUTH_FACEBOOK_KEY = '816424608392824'
SOCIAL_AUTH_FACEBOOK_SECRET = '28d832c1558e87d74a39fd309fd2df99'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.Facebook2OAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'last_name', 'email']

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'athletesunited.pipeline.my_social_auth',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

STREAM_API_KEY = 'y8uvcwtgmbk4'
STREAM_API_SECRET = '6rnt7twzpp7hygt7dkynt3us6vmzepwpraj8zcyutbq93a7w5erzubagc89wekb8'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2
}






