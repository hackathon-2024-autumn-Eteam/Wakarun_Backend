from django.db import models


class Questions(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=64)
    content = models.CharField(max_length=255)
    type = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    def __str__(self):
        return self.content
    
class Answers(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    question_id = models.CharField()
    content = models.CharField()
    is_true = models.BooleanField()

class Favorites(models.Model):
    user_id = models.CharField()
    question_id = models.CharField()
    registered_at = models.DateTimeField()