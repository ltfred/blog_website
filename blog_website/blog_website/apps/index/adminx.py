import xadmin
from .models import *


class CarouselAdmin(object):
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    list_display = ['image_url', 'url']


xadmin.site.register(Carousel, CarouselAdmin)