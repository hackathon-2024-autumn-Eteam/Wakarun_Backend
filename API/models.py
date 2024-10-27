from django.db import models

class Users(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=64)
    user_icon = models.CharField(max_length=64)
    create_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    def __str__(self):
        return self.user_name

class Questions(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='users', null=True)
    content = models.CharField(max_length=255)
    type = models.IntegerField()
    create_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    def __str__(self):
        return self.content