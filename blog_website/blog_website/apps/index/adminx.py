import xadmin
from .models import *


class CarouselAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['title', 'url', 'is_active']


xadmin.site.register(Carousel, CarouselAdmin)