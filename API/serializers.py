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
        # バリデーション済みのCustomUserインスタンスを取得
        user = validated_data.pop('user')
        question = Questions.objects.create(user=user, **validated_data)
        return question
