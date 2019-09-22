from django.shortcuts import render

# Create your views here.
from django.views import View


class CommentView(View):
    """留言"""

    def get(self, request):

        return render(request, 'comment.html')