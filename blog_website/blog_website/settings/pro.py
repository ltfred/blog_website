import datetime
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 添加导包路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_app'))

SECRET_KEY = 'n7-t&@=+ovjlqc*3=zsrw+9-8+0^i+uauxwasgx$4_3m29v&^p'

DEBUG = False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'rest_framework',
    'ckeditor',
    'notice',
    'article',
    'user',
    'index',
    'links',
    'photo',
    'soup',
    'comment',
    'site_statistics',
    'xadmin',
    'crispy_forms',
    'reversion',
    'myadmin',
    'corsheaders',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_website.urls'

TEMPLATES = [

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'environment': 'blog_website.utils.jinja2_env.jinja2_environment',
        },
    },
]

WSGI_APPLICATION = 'blog_website.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_website',
        'USER': 'root',
        'PASSWORD': 'mysql123',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}


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


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

STATIC_URL = '/static/'
# 配置静态文件加载路径
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 配置redis
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# 配置日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/blog_website.log'),
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'blog': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'ERROR',
        },
    }
}

# 指定用户模型类
AUTH_USER_MODEL = 'user.User'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'article.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

# 富文本编辑器设置
CKEDITOR_CONFIGS = {
    # django-ckeditor默认使用default配置
    'default': {
        # 编辑器宽度自适应
        'width': 'auto',
        'height': '400px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            # 表情 代码块
            ['Smiley', 'CodeSnippet'],
            # 字体风格
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote', 'FontSize', 'Font'],
            # 图片
            ['Image', ],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 链接
            ['Link', 'Unlink'],
            # 列表, 表格
            ['NumberedList', 'BulletedList', 'Table'],
            # 格式
            ['JustifyCenter', 'JustifyLeft', 'JustifyRight', 'Outdent', 'Indent'],
            # 最大化
            ['Maximize']
        ],
        # 加入代码块插件
        'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils']),
    }
}


# CORS跨域请求设置
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
)
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'blog_website.utils.pagination.StandardResultPagination',
}

# JWT扩展配置
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
}

# OSS
OSS_CONF = {
    'key': '********',
    'access_key': '*********'
}