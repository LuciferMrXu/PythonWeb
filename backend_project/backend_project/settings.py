"""
Django settings for backend_project project.

Generated by 'django-admin startproject' using Django 2.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
sys.path.insert(1,os.path.join(BASE_DIR,'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="http://ef99b8cbe6814d92bb53d40087b74a30@172.31.184.60:9000/2",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z0&pwaya(-00z%yy7!(899yfg_0gdeqa=hk(()3*w__#rsp_u$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'users.UserProfile'

AUTHENTICATION_BACKENDS = [
    'apps.users.views.CustomBackend'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "apps.pipeline_app",
    "apps.users",
    "django_filters",
    "corsheaders",
    "rest_framework",
    'rest_framework.authtoken',
]


MIDDLEWARE = [
    "apps.middleware.mymiddleware.PublicAccessControlMiddleware",
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'backend_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR+"/front_end_project/dist"],
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# 数据库备份和迁移
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'init_command':'SET default_storage_engine=INNODB;'},
        'NAME': 'ai_conf_platform',
        'USER': 'root',
        'PASSWORD': 'iflytek@ATP123',
        # 'HOST': '172.31.128.180',
        'HOST': '172.31.130.108',
        'PORT': '3306'
        # 'NAME': 'ai_conf_platform',
        # 'USER': 'root',
        # 'PASSWORD': '1qa2ws3ed',
        # 'HOST': '127.0.0.1',
        # 'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# STATICFILES_DIRS=(
#     os.path.join(BASE_DIR,'front_end_project/dist/static'),
# )

# 数据库缓存
# CACHE_BACKEND = "db://mysite_cache"
# # 配置redis缓存
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# 文件上传目录和外部访问的路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# 添加Cors配置
# 1、设置白名单
CORS_ORIGIN_WHITELIST = (
    'http://localhost:9528',
    'http://127.0.0.1:9528',
    'http://172.31.128.180:9528',
)
# 2、设置Cors Cookie
CORS_ALLOW_CREDENTIALS = True


# drf框架的配置信息
REST_FRAMEWORK = {
    # 'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 全局配置异常模块
    'EXCEPTION_HANDLER': 'apps.utils.exception.custom_exception_handler',
    # 修改默认返回JSON的renderer的类
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'apps.utils.rendererresponse.customrenderer',
    # ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
    # 设置所有接口都需要被验证
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    # 用户登陆认证方式
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 接口api测试用
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# REST_FRAMEWORK_EXTENSIONS = {
#     'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 15
# }

# jwt载荷中的有效期设置
JWT_AUTH = {
    #token 有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=8),
    'JWT_ALLOW_REFRESH': True,
    "JWT_AUTH_HEADER_PREFIX": "JWT",
     #续期有效期（该设置可在24小时内带未失效的token 进行续期） 
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=24),
    # 自定义返回格式，需要手工创建
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.utils.jwttoken.jwt_response_payload_handler',
}

# 发送邮件
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True   #是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
#EMAIL_USE_SSL = True    #是否使用SSL加密，qq企业邮箱要求使用
EMAIL_HOST = 'smtp.qq.com'   #发送邮件的邮箱 的 SMTP服务器，这里用了163邮箱
EMAIL_PORT = 25     #发件箱的SMTP服务器端口
EMAIL_HOST_USER = '938503262@qq.com'    #发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = 'vmcbpzhybitlbaid'         #发送邮件的邮箱密码(这里使用的是授权码)
EMAIL_FROM = 'RDG综合管理平台<938503262@qq.com>'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER