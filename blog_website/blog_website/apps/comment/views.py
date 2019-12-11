from django import http
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from comment.models import Message
import logging

logger = logging.getLogger('blog')


class CommentView(TemplateView):
    template_name = 'message.html'

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if not all([name, email, message]):
            return http.HttpResponse('请输入完整的内容')
        try:
            Message.objects.create(name=name, email=email, content=message)
        except Exception as e:
            logger.error('CommentView:post:' + str(e))
            raise
        return redirect(reverse('index:index_list'))
