import discord
from discord.ext import commands, tasks

from config import disc_token, interval, sound, email
from gmail_watcher import gmail_watcher, gmail_checker

service = gmail_watcher()
voice_client = None
watching = False
author = None


def start_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @tasks.loop(seconds=interval)
    async def gmail_loop():
        global voice_client
        global watching
        global author
        global service

        if not watching or author is None:
            return

        try:
            if gmail_checker(service):
                await author.send(f"It's time. {author.author.mention}")

            if voice_client and voice_client.is_connected():
                print('asdfsdf')
                audio = discord.FFmpegPCMAudio(source=sound)

                voice_client.play(audio)

            watching = False
            gmail_loop.stop()

        except Exception as e:
            service = gmail_watcher()

    @bot.command()
    async def run(ctx):
        global voice_client
        global watching
        global author

        if not ctx.author.voice:
            await ctx.send("Join VC")
            return

        author = ctx
        channel = ctx.author.voice.channel

        voice_client = await channel.connect()
        await ctx.send(f'joined {channel}')

        watching = True
        gmail_loop.start()
        await ctx.send(f"Scouting for {email.split('@')[0]}")

    @bot.command()
    async def stop(ctx):
        global voice_client
        global watching

        global watching, voice_client

        watching = False
        gmail_loop.stop()

        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()

        await ctx.send("Stopped")

    return bot