from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):
    """返回首页"""
    def get(self, request):

        return render(request, 'index.html')
