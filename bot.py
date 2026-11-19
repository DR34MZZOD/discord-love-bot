
import os
import discord
from discord.ext import commands

TOKEN = os.environ["DISCORD_TOKEN"]


class LoveBot(commands.Bot):

    async def setup_hook(self):
        await self.load_extension("lovebot")
        await self.tree.sync()
        print("Slash commands synced!")


intents = discord.Intents.default()

bot = LoveBot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Lovebot is online!")


bot.run(TOKEN)
