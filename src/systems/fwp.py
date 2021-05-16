import asyncio
from typing import Dict
import time

import discord
from discord.ext import commands
from asyncpraw.models import Submission
from asyncpraw.models.reddit.submission import SubmissionFlair

from src.embeds import Embeds
from src.utils import Utils


class Fwp:
    def __init__(self, yt_url: str, bot):
        self.bot = bot
        self.yt_url = yt_url
        self.posts: Dict[Submission, str] = {}
        self.format = "%M:%S"

    def _add(self, submission: Submission, timestamp: str):
        if not timestamp.startswith('0'):
            timestamp = '0' + timestamp

        self.posts[submission] = timestamp

    def _sort(self):
        _min = [time.strptime(t, self.format) for t in self.posts.values()]
        values = [time.strftime(self.format, h) for h in sorted(_min)]

        new_posts = {}
        for i in values:
            for k in self.posts.keys():
                if self.posts[k] == i:
                    new_posts[k] = self.posts[k]
                    break

        self.posts = new_posts

    async def _flair(self, submission: Submission):
        submission_flair: SubmissionFlair = submission.flair
        levels = self.bot.config.data['reddit']['flairs']['user']['levels']

        await submission_flair.select(self.bot.config.data['reddit']['flairs']['post'])

        user_flair = ''
        async for flair in submission.subreddit.flair(redditor=submission.author):
            user_flair = flair['flair_text'] or ''

        existing_flairs = [s for s in levels if s in user_flair]

        if existing_flairs:
            index = levels.index(existing_flairs[-1])
            if index < len(levels) - 1:
                user_flair += levels[index + 1]
        else:
            user_flair += levels[0]

        await submission.subreddit.flair.set(submission.author,
                                             flair_template_id=self.bot.config.data['reddit']['flairs']['user']['id'],
                                             text=user_flair)

    # noinspection PyDunderSlots,PyUnresolvedReferences
    async def _confirm(self, msg: discord.Message, submission: Submission, timestamp: str):
        embed = Embeds.post(submission)
        message = await msg.channel.send('Is this the correct post?', embed=embed)

        await Utils.multi_react(message, ['✅', '⛔'])

        try:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     timeout=60.0,
                                                     check=lambda react, react_user:
                                                     react.message.id == message.id and react_user == msg.author)
        except asyncio.TimeoutError:
            await msg.channel.send("Smh, at least give me an reaction. Try again >:(")
            return
        else:
            if reaction.emoji == '✅':
                self._add(submission, timestamp)
                await self._flair(submission)
                embed.color = discord.colour.Color.green()
            else:
                embed.color = discord.colour.Color.red()
                await msg.channel.send("Looks like something went wrong :(, please try again")

            await message.edit(embed=embed)

    async def _get_submission(self, url) -> Submission:
        submission = Submission(self.bot.reddit, url=url)
        await submission.load()
        await submission.author.load()
        await submission.subreddit.load()

        return submission

    async def start(self, msg: discord.Message):
        while True:
            msg = await self.bot.wait_for('message', check=lambda m: m.channel == msg.channel)
            if msg.content.lower() == "done":
                break

            args = msg.content.split()
            try:
                submission = await self._get_submission(args[0])
                await self._confirm(msg, submission, args[1])
            except Exception as e:
                await msg.channel.send("I'm having some trouble serializing that, please try again\n\n"
                                       "Example: "
                                       "`https://www.reddit.com/r/YouFellForItFool/comments/cjlngm"
                                       "/you_fell_for_it_fool/ "
                                       "1:30`\n\n"
                                       "```{0}```".format(e))

    def generate(self) -> str:
        self._sort()
        comment = ''
        for k in self.posts.keys():
            comment += "* [https://reddit.com{0}]({1}) {2}\n".format(k.permalink, k.title, self.posts[k])

        return comment
