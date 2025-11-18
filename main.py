from bot import start_bot
from config import disc_token


def main():
    bot = start_bot()
    bot.run(disc_token)

if __name__ == "__main__":
    main()