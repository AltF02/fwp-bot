from src.bot import Bot
from src.config import Config
from src.reddit import Reddit


def main():
    location = "config.yml"
    config = Config(location)
    reddit = Reddit(config)

    bot = Bot(config, reddit, location)
    bot.run(config.data['discord']['token'])


if __name__ == '__main__':
    main()
