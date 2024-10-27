from API.models import Questions, Users
from rest_framework import serializers

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields =  ['user_name', 'user_icon']

class QuestionsSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    class Meta:
        model = Questions
        fields =  ['id', 'user','content','type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_name = representation['user']['user_name']
        user_icon = representation['user']['user_icon']
        representation.pop('user')
        representation['user_name'] = user_name
        representation['user_icon'] = user_icon

        return representation
