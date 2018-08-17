from poolbot.util import JsonConfig
from poolbot.bot import Bot

if __name__ == "__main__":
    try:
        config = JsonConfig.load("config.json")
        b = Bot(config)
    except KeyboardInterrupt:
        print("\nStopped")
