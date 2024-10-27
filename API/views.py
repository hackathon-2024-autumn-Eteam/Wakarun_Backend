from API.models import Questions, Answers, Favorites
from rest_framework import permissions, viewsets

from API.serializers import QuestionsSerializer, AnswersSerializer, FavoritesSerializer


class QuestionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer