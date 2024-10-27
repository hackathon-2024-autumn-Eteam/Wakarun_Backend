from API.models import Questions,Answers,Favorites
from rest_framework import serializers


class QuestionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Questions
        fields = ['id', 'user_id', 'content', 'type', 'create_at', 'updated_at']

class AnswersSerializer(serializers.HyperlinkedModelSerializer):
    class meta:
        model = Answers
        fields = ['id', 'question_id', 'content', 'is_true']

class FavoritesSerializer(serializers.HyperlinkedModelSerializer):
    class meta:
        model = Favorites
        fields = ['user_id', 'question_id', 'registered_at']
