from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from API.models import CustomUser, Questions, Answers, Favorites
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from API.serializers import QuestionsSerializer, RegisterSerializer

#タイムライン記事リスト取得
class TimelineView(APIView):
    def get(self, request, *args, **kwargs):
        instance = Questions.objects.select_related('user').all()
        serializer = QuestionsSerializer(instance, many=True)
        resp = {"questions": serializer.data}
        return Response(resp, status.HTTP_200_OK)

#サインアップ機能
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                'message': 'ユーザーが作成されました。', 
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

