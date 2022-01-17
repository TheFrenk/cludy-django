import email
import imp
from operator import mod
from statistics import mode
from django.db import models
from .managers import DiscordUserOAuth2Manger

class DiscordUser(models.Model):
    objects = DiscordUserOAuth2Manger()

    id = models.BigIntegerField(primary_key=True)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    flags = models.IntegerField()
    locale = models.CharField(max_length=100)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)

    def is_authenticated(self, request):
        return True

class Guilds(models.Model):
    id = models.BigIntegerField(primary_key=True)
    guildID = models.CharField(max_length=100)
    prefix = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=255, null=True)
    owner = models.BooleanField()
