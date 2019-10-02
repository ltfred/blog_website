import xadmin
from soup.models import Soup


class SoupAdmin(object):
    pass


xadmin.site.register(Soup, SoupAdmin)
