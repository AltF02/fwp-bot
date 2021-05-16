import asyncpraw


class Reddit(asyncpraw.Reddit):
    def __init__(self, config):
        super().__init__(
            client_id=config.data['reddit']['client_id'],
            client_secret=config.data['reddit']['client_secret'],
            user_agent=config.data['reddit']['user_agent'],
            refresh_token=config.data['reddit']['refresh_token'],
        )

    async def test(self):
        print(await self.user.me())
