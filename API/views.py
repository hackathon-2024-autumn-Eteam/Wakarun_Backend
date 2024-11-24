from API.models import CustomUser, Questions, Answers, Favorites
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from API.serializers import(
    QuestionsSerializer, RegisterSerializer, 
    CreateQuestionSerializer,
)

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
    

#問題作成機能
class CreateQuestionView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = CreateQuestionSerializer(data=request.data)

        if serializer.is_valid():
            question = serializer.save()
            return Response({
                'status': '200',
                'message': '問題文が作成されました。',
                'id': question.id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)