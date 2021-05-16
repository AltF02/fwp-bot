import discord

import yaml
from discord.ext import commands
from asyncpraw.models import Submission

from src.systems.fwp import Fwp


class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def config(self, ctx: commands.Context):
        await ctx.send("Please provide an subcommand")

    @config.command()
    async def channel(self, ctx: commands.Context, channel: discord.TextChannel):
        self.bot.config.data['discord']['channel'] = channel.id
        with open(self.bot.location, 'w') as file:
            yaml.dump(self.bot.config.data, file)

        await ctx.send("Updated the channel to {0}".format(channel.mention))

    @config.command()
    async def prefix(self, ctx: commands.Context, new: str = None):
        if new is None:
            await ctx.send("My current prefix is {0}".format(ctx.prefix))
        else:
            self.bot.config.data['discord']['prefix'] = new
            self.bot.command_prefix = new

            with open(self.bot.location, 'w') as file:
                yaml.dump(self.bot.config.data, file)

            await ctx.send("Updated the prefix to {0}".format(self.bot.config.data['discord']['prefix']))

    @commands.command()
    async def force(self, ctx: commands.Context, url: str):
        await ctx.send('Starting forced... Send `done` when finished')

        fwp = Fwp(url, self.bot)
        await fwp.start(ctx.message)

        await ctx.send("Generating list...")
        await ctx.send("```\n{0}\n```".format(fwp.generate()))


def setup(bot):
    bot.add_cog(Meta(bot))
