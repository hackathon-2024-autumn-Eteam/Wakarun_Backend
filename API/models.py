from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=64, primary_key=True)
    user_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254, unique=True)
    user_icon = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.email

class Questions(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='questions', null=True)
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
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites', null=True)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='favorites', null=True)
    registered_at = models.DateTimeField(auto_now_add=True)