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
    
#問題文作成機能
class CreateQuestionSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField()  # クライアントからUUIDとしてユーザーIDを受け取る

    class Meta:
        model = Questions
        fields = ['user', 'title', 'content', 'type']

    def validate_user(self, value):
        """
        UUID形式のユーザーIDを検証し、対応するユーザーを取得する。
        """
        try:
            user = CustomUser.objects.get(id=value)  # UUIDからCustomUserを取得
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("指定されたユーザーは存在しません。")
        return user  # CustomUserインスタンスを返す
    
    def create(self, validated_data):
        question = Questions.objects.create(**validated_data)
        return question


#解答作成機能(many=Trueで呼び出した場合、CreateListAnswerSerializerがよばれる)
class CreateListAnswersSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        answers = [Answers(**item) for item in validated_data]
        return Answers.objects.bulk_create(answers)

    def validate(self, data):
        # 解答を３つ以上登録しようとしたらエラー
        if len(data) > 3 :
            raise serializers.ValidationError("Questionに対してAnswerを３つ以上登録することはできません。")

        # 正解を2つ以上登録しようとしたらエラー
        true_count = 0
        for item in data:
            if item['is_true'] == True :
                true_count += 1

        if true_count > 1:
            raise serializers.ValidationError("正解は１つまでしか設定することができません")

class CreateAnswersSerializer(serializers.ModelSerializer):
    # クライアントからUUIDとしてユーザーIDを受け取る
    question_id = serializers.UUIDField()  

    class Meta:
        model = Answers
        fields = ['question_id', 'content', 'is_true']
        list_serializer_class = CreateListAnswersSerializer

    def validate_question_id(self, value):
        """
        UUID形式のユーザーIDを検証し、対応するユーザーを取得する。
        """
        try:
            # UUIDからQuestionを取得
            question = Questions.objects.get(id=value)  
        except Questions.DoesNotExist:
            raise serializers.ValidationError("指定されたユーザーは存在しません。")
        # Questionインスタンスを返す
        return question  
    
    def create(self, validated_data):
        answer = Answers.objects.create(**validated_data)
        return answer

#問題に解答する（正答を表示する）機能
class AnswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = ['content']
        
