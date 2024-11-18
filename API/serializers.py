from API.models import CustomUser, Questions
from rest_framework import serializers
import uuid

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