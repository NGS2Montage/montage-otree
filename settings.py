import os
import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = environ.Path(__file__) - 1

env = environ.Env()
env.read_env(ROOT_DIR('.env'))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if env.str('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

INTERNAL_IPS = ['127.0.0.1'] if DEBUG else []

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = env.str('OTREE_ADMIN_PASSWORD', None)

# don't share this with anybody.
SECRET_KEY = env.str('DJANGO_SECRET_KEY')

# To use a database other than sqlite,
# set the DATABASE_URL environment variable.
# Examples:
# postgres://USER:PASSWORD@HOST:PORT/NAME
# mysql://USER:PASSWORD@HOST:PORT/NAME

possible_hosts = env.str('DJANGO_ALLOWED_HOST', None)
ALLOWED_HOSTS = possible_hosts.split(',') if possible_hosts is not None else []


# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree',
                  'django.contrib.sites',  # required for allauth
                  'django_extensions',
                  'reversion',  # for tracking changes to models

                  'crispy_forms',  # Form layouts

                  'allauth',  # registration
                  'allauth.account',  # registration
                  'allauth.socialaccount',  # registration (must be here even if you don't use)

                  'channels',  # websockets
                  'channels_api',
                  'otreechat',

                  # our stuff
                  'core',
                  'clicktracking'
                  ]


DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = env.str('OTREE_AUTH_LEVEL', None)

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY', None)


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'


# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
oTree games
"""

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study', 'groups'],
    'title': 'Jointly - Group Exercise Games',
    'description': 'Play games with other AMT workers.',
    'frame_height': 500, #Needs adjustment
    'preview_template': 'core/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 1,  # 7 days
    # 'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1,
    'participation_fee': 0.05,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}


SESSION_CONFIGS = [
#    {
#        'name': 'production_pgg_IRBv1',
#        'display_name': 'Public Goods Game - IRB.v1',
#        'num_demo_participants': 2,
#        'app_sequence': [
#            'welcome', 
#            'demographic', 
#            'instructions_anagrams',
#            'anagrams',
#            'ruse',
#            'instructions_pgg', 
#            'public_goods',
#            'conclusion',
#            ],
#        
#        # Welcome - Variables
#        'n_games': 2,
#        
#        # Anagrams - Phase 1 Options
#        'bestScore': 400,
#        'threshold_num_words': 100,
#        'threshold_num_points': 100,
#        'marginal_points': 1,
#        'timeout_anagrams_min': 5, # do not change until otree upgrade
#        'n_neighbors': 2,
#        'n_letters': 3,
#        'use_chat': False,
#        
#        # Public Goods Game - Phase 2 Options
#        'pgg_bonus': 100,
#        'pgg_multiplier': 2, #do not change!
#        'pgg_timeout_min': 3, #do not change! dev coming
#    },
    {
        'name': 'production_pgg_IRBv2',
        'display_name': 'Public Goods Game - IRB.v2',
        'num_demo_participants': 3,
        'app_sequence': [
            'welcome', 
            'demographic', 
            'instructions_anagrams',
            'anagrams',
            'ruse',
            'instructions_pgg', 
            'public_goods', 
            'demographic_detailed',
            'conclusion',
            ],
        
        # Welcome - Variables
        'n_games': 2,
        
        # Anagrams - Phase 1 Options
        'bestScore': 400,
        'threshold_num_words': 2,
        'threshold_num_points': 100,
        'marginal_points': 1,
        'timeout_anagrams_min': 5, # do not change until otree upgrade
        'n_neighbors': 2,
        'n_letters': 3,
        'use_chat': False,
        
        # Public Goods Game - Phase 2 Options
        'pgg_bonus': 100,
        'pgg_multiplier': 2, #do not change!
        'pgg_timeout_min': 3, #do not change! dev coming
        
        # Demographic Detaile - "Optional Survey"
        'optional_survey_payout': 5,
    },
]

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = [ROOT_DIR.path('core')('templates')]

STATICFILES_DIRS = [
    ROOT_DIR.path('core')('static'),
    ROOT_DIR.path('anagrams')('static'),
]


# CHANNELS
# ------------------------------------------------------------------------------
CHANNEL_ROUTING = 'core.routing.channel_routing'
# This overrides the default ROUTING "otree.channels.routing.channel_routing". Might pose a challenge


SENTRY_DSN = 'http://0acbffd8caea463fb47dc7ab8449e49f:ce3a9cd912f240c79a85d96e6fe51066@sentry.otree.org/153'


# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())


MIDDLEWARE_CLASSES = [
    'otree.middleware.CheckDBMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # this middlewware is for generate human redeable errors

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

'''
if DEBUG:
    # INSTALLED_APPS.append('debug_toolbar')
    # INSTALLED_APPS.append('channels_panel')
    MIDDLEWARE_CLASSES.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'channels_panel.panel.ChannelsDebugPanel',
    ]
'''

TEMPLATES[0]['OPTIONS']['context_processors'].append('django.template.context_processors.request')

WSGI_APPLICATION = 'ngs2.wsgi.application'


# Hope this doesn't conflict with otree Admin account
ADMINS = (
    ("""Nathan Self""", 'nwself@vt.edu'),
    ("""Parang Saraf""", 'parang@cs.vt.edu'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

USE_I18N = True

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Get this id from the admin page site table
SITE_ID = 1


# ALLAUTH CONFIGURATION
# ------------------------------------------------------------------------------
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'core.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'core.users.adapters.SocialAccountAdapter'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[NGS2 Montage] '

# These can be useful
LOGIN_REDIRECT_URL = 'redirect'
LOGIN_URL = '/accounts/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'


ACCOUNT_FORMS = {'login': 'core.forms.LoginForm',
                 'change_password': 'core.forms.ChangePasswordForm',
                 'reset_password': 'core.forms.ResetPasswordForm',
                 'reset_password_from_key': 'core.forms.ResetPasswordKeyForm'}


CRISPY_FAIL_SILENTLY = True
CRISPY_TEMPLATE_PACK = 'bootstrap3'


# EMAIL SETTINGS
# ------------------------------------------------------------------------------
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ngs2.montage@gmail.com'
EMAIL_HOST_PASSWORD = env.str('PASSWORD')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'NGS2 Montage <ngs2.montage@gmail.com>'

del TEMPLATE_DIRS
