from django.db import models

class Users(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=64)
    user_icon = models.CharField(max_length=255, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user_name

class Questions(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='users', null=True)
    title = models.CharField(max_length=255, default='未設定')
    content = models.TextField()
    type = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class Answers(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    is_true = models.BooleanField()
    def __str__(self):
        return self.content

class Favorites(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='favorites', null=True)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='favorites', null=True)
    registered_at = models.DateTimeField(auto_now_add=True)