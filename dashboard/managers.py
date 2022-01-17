from django.contrib.auth import models

class DiscordUserOAuth2Manger(models.UserManager):
    def create_new_discord_user(self, user):
        print('Inside Discord User Manager')
        discord_tag = user['username']
        new_user = self.create(
            id=user['id'],
            avatar=user['avatar'],
            flags=user['flags'],
            locale=user['locale'],
            mfa_enabled=user['mfa_enabled'],
            discord_tag=discord_tag,
        )
        return new_user