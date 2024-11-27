from API.models import CustomUser, Questions, Answers, Favorites
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from API.serializers import(
    QuestionsSerializer, RegisterSerializer, 
    CreateQuestionSerializer,
    CreateAnswersSerializer, AnswersSerializer
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

class CreateAnswersView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = CreateAnswersSerializer(data=request.data, many=True)

        if serializer.is_valid():
            answer = serializer.save()
            return Response({
                'status': '200',
                'message': '解答が作成されました。',
                'answer': JSONRenderer().render(serializer.data)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#問題に解答する（正答を表示する）機能
class AnswersView(APIView):
    def get(self, request, *args, **kwargs):
        # クエリパラメータから 'question_id' を取得
        question_id = request.query_params.get('question_id')
        
        # question_idが空の場合、400_BAD_REQUESTを返す
        if not question_id:
            return Response({"content": "Question ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 問題に対応する解答を取得
            answer = Answers.objects.get(question_id=question_id)

        # データが見つからない場合、エラーメッセージを返す    
        except Answers.DoesNotExist:
            return Response(
                {"content": "解答が存在しません。"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # 解答が見つかれば、contentをシリアライズして返す
        serializer = AnswersSerializer(answer, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)