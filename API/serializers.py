from API.models import CustomUser, Questions, Answers
from rest_framework import serializers

#タイムライン記事リスト取得

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_name', 'user_icon']

class QuestionsSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    class Meta:
        model = Questions
        fields = ['id', 'user', 'title', 'content', 'type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_name = representation['user']['user_name']
        user_icon = representation['user']['user_icon']
        representation.pop('user')
        representation['user_name'] = user_name
        representation['user_icon'] = user_icon

        return representation 

#サインアップ機能
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

#問題作成機能
class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['id', 'content', 'is_true', 'answers']
        # extra_kwargs = {'question': {'read_only': True}}
    
    def validate(self, data):
        question = self.context['question']  # context から question を取得
        question_type = question.type

        if question_type == 1:
            data['is_true'] = None # 記述式の場合、is_true は null に設定
        
        # 選択式の場合、is_true は必須
        elif question_type == 2:
            if data.get('is_true') is None:
                raise serializers.ValidationError('選択肢には正誤判定が必要です')
        return data

class CreateQuestionSerializer(serializers.ModelSerializer):
    answers = CreateAnswerSerializer(many=True)

    class Meta:
        model =Questions
        fields = ['title', 'content', 'type', 'answers', 'question']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # 問題が選択式の場合、選択肢を含める
        if instance.type == 2: # 問題が選択式の場合
            for answer in representation['answers']:
                answer['content'] = answer.get('content') #選択式の内容を返す

        return representation
