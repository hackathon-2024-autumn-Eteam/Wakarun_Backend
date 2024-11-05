from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from API.models import Users, Questions, Answers, Favorites
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from API.serializers import QuestionsSerializer

#タイムライン記事リスト取得
class TimelineView(APIView):
    def get(self, request, *args, **kwargs):
        instance = Questions.objects.all()
        serializer = QuestionsSerializer(instance, many=True)
        resp = {"questions": serializer.data}
        return Response(resp, status.HTTP_200_OK)
    
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")