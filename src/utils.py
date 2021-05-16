import typing

import discord


class Utils:
    @staticmethod
    async def multi_react(msg: discord.Message, emotes: typing.List[str]):
        for e in emotes:
            await msg.add_reaction(e)

    @staticmethod
    def format_link(video_id: str):
        return "https://www.youtube.com/watch?v={}".format(video_id)
