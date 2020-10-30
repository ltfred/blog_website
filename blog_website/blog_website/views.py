# _*_coding:utf-8_*_
# author: ltfred
from django.shortcuts import render


def page_not_found(request):
    return render(
        request,
        'error.html',
        context={'code': 404, 'msg': u'对不起，你要找的这个页面突然不见了。不过，放心，一切都在我的掌控之中，不会跑多远！'}
    )


def server_error(request):
    return render(
        request,
        'error.html',
        context={'code': 500, 'msg': u'对不起，似乎出了点问题呢。不过，放心，一切都在我的掌控之中，不会跑多远！'}
    )
