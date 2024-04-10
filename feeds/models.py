from django.db import models
from django.contrib.auth.models import User

class ChannelGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_group = models.ForeignKey(ChannelGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'channel_group')