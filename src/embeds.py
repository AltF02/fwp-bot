import discord
from asyncpraw.models import Submission


class Embeds:
    @staticmethod
    def post(submission: Submission) -> discord.Embed:
        embed = discord.Embed()
        embed.title = submission.title
        embed.set_author(name=submission.author.name, icon_url=submission.author.icon_img)
        embed.set_image(url=submission.url)
        embed.set_footer(text="👍 {0} | 💬 {1}".format(submission.score, submission.num_comments))

        return embed
