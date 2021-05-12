import discord


class Bot(discord.Client):
    async def on_ready(self):
        print('Bot ready as {0}'.format(self.user))

