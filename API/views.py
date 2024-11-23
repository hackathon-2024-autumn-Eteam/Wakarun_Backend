from API.models import CustomUser, Questions, Answers, Favorites
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from API.serializers import(
    QuestionsSerializer, RegisterSerializer, 
    CreateQuestionSerializer, CreateAnswerSerializer
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
    # permission_classes = [IsAuthenticated]  #認証されたユーザーのみがアクセス可能

    def post(self, request, *args, **kwargs):
        question_serializer = CreateQuestionSerializer(data=request.data, context={'request': request})

        if question_serializer.is_valid():
            # 問題を保存
            question = question_serializer.save()

            # 問題が記述式か選択式かに応じて解答を処理
            for answer_data in request.data.get('submit_answers', []):
                # 記述式の場合、is_trueはNone
                if question.type == 1: # 記述式
                    answer_data['is_true'] = None # is_trueはnullに設定
                
                #解答をシリアライズ
                answer_serializer = CreateAnswerSerializer(data=answer_data)
                if answer_serializer.is_valid():
                    answer_serializer.save(question_id=question.id) #解答を問題に関連づけて保存
                else:
                    return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(question_serializer.data, status=status.HTTP_201_CREATED)
        return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)