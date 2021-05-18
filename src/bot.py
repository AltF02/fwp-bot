import discord.ext.commands
from discord.ext import commands

from src.config import Config
from src.reddit import Reddit


class Bot(commands.Bot):
    def __init__(self, config: Config, reddit: Reddit, location: str):
        super().__init__(
            command_prefix=config.data['discord']['prefix'],
            case_insensitive=True,
        )

        self.load_extensions()
        self.config = config
        self.reddit = reddit
        self.location = location

    def load_extensions(self):
        self.load_extension('src.cogs.meta')
        self.load_extension('src.systems.youtube')

    async def on_ready(self):
        print('Logged into Discord as {0}'.format(self.user))
        print('Logged into Reddit as {0}'.format(await self.reddit.user.me()))

    async def on_command_error(self, ctx, e):
        if isinstance(e, discord.ext.commands.CommandNotFound):
            return

        await ctx.send("Something went wrong :/, please call my dad if this is unexpected\n\n```{0}```".format(e))

