import random
from django.views.generic import TemplateView

from article.models import ArticleCategory
from blog_website.utils.common import get_photo_category
from links.models import Link
import logging
from soup.models import Soup

logger = logging.getLogger('blog')


class LinkView(TemplateView):
    template_name = 'link.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommend_links'] = Link.objects.filter(is_recommend=True)
        context['links'] = Link.objects.filter(is_recommend=False)
        context['cat_list'] = ArticleCategory.get_cat_lst()
        context['photo_category'] = get_photo_category()
        soups = Soup.objects.all()
        context['soup'] = random.choice(soups).content if soups else ''
        return context
