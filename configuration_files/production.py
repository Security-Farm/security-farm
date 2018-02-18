# This is the production settings !
# All settings that do not change across environments should be in 'fir.settings.base'
from fir.config.base import *

################################################################
##### Change these values
################################################################

ALLOWED_HOSTS = ['FIR.SOC.LAN']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fir',
        'USER': 'fir',
        'PASSWORD': 'firpassword',
        'HOST': 'localhost',
        'PORT': '3006',
    }
}

# SMTP SETTINGS
EMAIL_HOST = 'SMTP.SOC.LAN'
EMAIL_PORT = 25

# Uncomment this line to set a different reply-to address when sending alerts
# REPLY_TO = other@address.com
EMAIL_FROM = '"Administrator" <administrator@soc.lan>'

# Uncomment these lines if you want additional CC or BCC for all sent emails
# EMAIL_CC = ['address@email']
# EMAIL_BCC = ['address@email']

# SECRET KEY
SECRET_KEY = 'dwoqDL32ghd39lds112K'

################################################################

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# List of callables that know how to import templates from various sources.
# In production, we want to cache templates in memory
TEMPLATES[0]['OPTIONS']['loaders'] = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s: %(module)s %(filename)s:%(lineno)d(%(funcName)s)\n%(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'errors.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# External URL of your FIR application (used in fir_notification to render full URIs in templates)
EXTERNAL_URL = 'https://fir.soc.lan'
