# models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4


from datetime import datetime, timedelta
from django.utils import timezone

class UserActivateTokensManager(models.Manager):
    def activate_user_by_token(self, token):
        user_activate_token = UserActivateTokens.objects.filter(
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        if user_activate_token:
            user = user_activate_token.user
            user.is_active = True
            user.save()

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

class UserActivateTokens(models.Model):
    token = models.UUIDField(db_index=True, default=uuid4, editable=False)
    expired_at = models.DateTimeField()
    user = models.OneToOneField(
        Users, on_delete=models.CASCADE,
        primary_key=True,
    )

    @classmethod
    def activate_user_by_token(cls, token):
        try:
            user_token = cls.objects.get(token=token, expired_at__gt=timezone.now())
            user_token.user.is_active = True
            user_token.user.save()
            user_token.delete()  # トークンは一度使われたら削除する場合
            return True  # 有効化成功
        except cls.DoesNotExist:
            return False  # トークンが見つからないか有効期限切れ

    objects = UserActivateTokensManager()

    class Meta:
        db_table = 'user_activate_tokens'

@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs):
    user_activate_token = UserActivateTokens.objects.create(
        user=instance, expired_at=datetime.now() + timedelta(days=1)
    )
