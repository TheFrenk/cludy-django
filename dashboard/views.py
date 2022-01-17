from calendar import c
from email import header
from aiohttp import request
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse, response
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
import requests
import json
from .models import Guilds
from pymongo import MongoClient

tokenURL = "https://discordapp.com/api/oauth2/token"
apiURLBase = "https://discordapp.com/api/users/@me"
apiURLGuilds = "https://discordapp.com/api/users/@me/guilds"
revokeURL = "https://discordapp.com/api/oauth2/token/revoke"
auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=930550246776385667&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify%20email%20guilds"
API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_ID = '930550246776385667'
CLIENT_SECRET = '-1BvektQZ9nTa1Al31C3Kv6DDDCscnIJ'
REDIRECT_URI = 'http://localhost:8000/oauth2/login/redirect'

client = MongoClient('mongodb+srv://cakenuss:A795239120905z@cluster0.xyux9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['myFirstDatabase']
collection = db['guilds']

def home(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"msg": "Hello"})

@login_required(login_url="/dashboard")
def get_authenticated_user(request: HttpRequest):
    user = request.user
    guilds = Guilds.objects.filter(owner="True")
    dbguilds = Guilds.objects.all()
    context = {'user': user, 'guilds': guilds, 'dbguilds': dbguilds}
    return render(request, 'dashboard/index.html', context)

def discord_login(request: HttpRequest):
    return redirect(auth_url_discord)

def discord_logout(request: HttpRequest):
    try:
        Session.objects.all().delete()
    except KeyError:
        pass
    return HttpResponse("You're logged out")

def discord_login_redirect(request: HttpRequest):
    code = request.GET.get('code')
    token = exchange_code(code)
    user = get_user_info(token['access_token'])
    guild = get_guild_info(token['access_token'])
    for item in guild:
        guilds = Guilds(
            id=item['id'],
            name=item['name'],
            icon=item['icon'],
            owner=item['owner'],
        )
        guilds.save()
    for bot in collection:
        botguilds = Guilds(
            guildID=bot['id'],
            prefix=bot['prefix'],
        )
        botguilds.save()
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    print(discord_user)
    login(request, discord_user)
    return redirect("/dashboard")

def exchange_code(code: str):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify guilds email"
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    r.raise_for_status()
    token = r.json()
    return token

def get_user_info(token: str):
    response = requests.get("https://discord.com/api/users/@me", headers={
        'Authorization': 'Bearer %s' % token
    })
    user = response.json()
    return user

def get_guild_info(token: str):
    response = requests.get("https://discord.com/api/users/@me/guilds", headers={
        'Authorization': 'Bearer %s' % token
    })
    guild = response.json()
    return guild