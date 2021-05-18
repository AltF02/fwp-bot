from discord.ext import commands, tasks
import feedparser
import discord

from src.embeds import Embeds
from src.systems.fwp import Fwp
from src.utils import Utils


class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_video = ''
        self.check_youtube.start()

    @tasks.loop(minutes=1.0)
    async def check_youtube(self):
        feed = feedparser.parse(
            "https://www.youtube.com/feeds/videos.xml?channel_id={}".format(
                self.bot.config.data['youtube']['channel_id']
            ))

        entry = feed.entries[0]
        if entry['yt_videoid'] == self.last_video:
            return

        self.last_video = entry['yt_videoid']
        msg = await self._dispatch(entry)
        await Utils.multi_react(msg, ['👍', '👎'])

        await self._listen(msg)

    @check_youtube.before_loop
    async def wait_for_bot(self):
        await self.bot.wait_until_ready()

    async def _dispatch(self, entry) -> discord.Message:
        channel = await self.bot.fetch_channel(self.bot.config.data['discord']['channel'])
        return await channel.send(
            "**{0}** uploaded a new video, is this FWP? <@&{1}>\n{2}".format(entry['author_detail']['name'],
                                                                             self.bot.config.data['discord']['role'],
                                                                             entry['link'],
                                                                             ))

    async def _listen(self, msg: discord.Message):
        reaction, user = await self.bot.wait_for('reaction_add',
                                                 check=lambda r, a: r.message.channel == msg.channel and not a.bot)
        vid_url = Utils.format_link(self.last_video)

        if reaction.emoji == '👍':
            await msg.channel.send('Starting... Send `done` when finished')
            fwp = Fwp(vid_url, self.bot)
            await fwp.start(msg)

            await msg.channel.send("Generating list...")
            await msg.channel.send(file=discord.File(fwp.generate(), "list.txt"))
        else:
            await msg.channel.send('😦 Sadge, better luck next time!\n\n'
                                   '*If this is a mistake you can force the video with, '
                                   '`{0}force {1}`*'.format(self.bot.command_prefix,
                                                            vid_url))


def setup(bot):
    bot.add_cog(Youtube(bot))
