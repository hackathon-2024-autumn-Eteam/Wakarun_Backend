from django.db import models


class Questions(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=64)
    content = models.CharField(max_length=255)
    type = models.IntegerField()
    create_at = models.DateTimeField()
    updated_at = models.DateTimeField()