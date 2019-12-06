from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from article.models import Article, Label
from photo.models import Photo
from user.models import User


class AdminUserCount(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        count = User.objects.count()
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        response_data = {
            'date': now_date.date(),
            'count': count
        }

        return Response(response_data)


class AdminArticleCount(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        count = Article.objects.count()
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        response_data = {
            'date': now_date.date(),
            'count': count
        }

        return Response(response_data)


class AdminPhotoCount(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        count = Photo.objects.count()
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        response_data = {
            'date': now_date.date(),
            'count': count
        }

        return Response(response_data)


class AdminLabelCount(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        count = Label.objects.count()
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        response_data = {
            'date': now_date.date(),
            'count': count
        }

        return Response(response_data)


class AdminUserDayActiveCount(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gte=now_date).count()
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        response_data = {
            'date': now_date.date(),
            'count': count
        }
        return Response(response_data)


class AdminArticleMonthCountView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):

        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        begin_date = now_date - timedelta(days=29)
        count_list = []
        for i in range(30):
            cur_date = begin_date + timedelta(days=i)
            next_date = cur_date + timedelta(days=1)
            count = Article.objects.filter(create_time__gte=cur_date, create_time__lt=next_date).count()
            count_list.append({
                'date': cur_date.date(),
                'count': count
            })

        return Response(count_list)


class AdminLabelArticle(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        labels_queryset = Label.objects.all()
        labels = []
        for label in labels_queryset:
            labels.append({
                'category': label.name,
                'count': label.article_set.all().count()  # 每个标签下的文章的数量
            })
        return Response(labels)