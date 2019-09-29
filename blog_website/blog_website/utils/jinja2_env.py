import time
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    # 将过滤器添加到jinja2中
    env.filters['time_filter'] = time_filter
    env.filters['date_time'] = date_time
    return env


# 定义了一个时间过滤器
def time_filter(datetime):
    ans_time = time.mktime(datetime.timetuple())
    timestamp = time.time() - ans_time
    if timestamp < 60:
        return '刚刚'
    elif 60 <= timestamp <= 60 * 60:
        minutes = timestamp / 60
        return '%s分钟前' % int(minutes)
    elif 60 * 60 <= timestamp <= 60 * 60 * 24:
        hours = timestamp / (60 * 60)
        return "%s小时前" % int(hours)
    elif 60 * 60 * 24 <= timestamp <= 60 * 60 * 24 * 3:
        days = timestamp / (60 * 60 * 24)
        return "%s天前" % int(days)
    else:
        return datetime.strftime("%Y-%m-%d %H:%M")


def date_time(datetime):
    return datetime.strftime("%Y-%m-%d")
