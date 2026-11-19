
import discord
import requests

from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def create_love_image(user1, user2, percentage):

    img = Image.new(
        "RGB",
        (1000, 500),
        (35, 12, 45)
    )

    draw = ImageDraw.Draw(img)

    def get_avatar(url):

        response = requests.get(url, timeout=15)
        response.raise_for_status()

        avatar = Image.open(
            BytesIO(response.content)
        ).convert("RGBA")

        avatar = avatar.resize((190, 190))

        mask = Image.new("L", (190, 190), 0)

        ImageDraw.Draw(mask).ellipse(
            (0, 0, 190, 190),
            fill=255
        )

        avatar.putalpha(mask)

        return avatar

    avatar1 = get_avatar(user1.display_avatar.url)
    avatar2 = get_avatar(user2.display_avatar.url)

    img.paste(avatar1, (140, 120), avatar1)
    img.paste(avatar2, (670, 120), avatar2)

    try:
        heart_font = ImageFont.truetype(
            "DejaVuSans.ttf", 110
        )

        percent_font = ImageFont.truetype(
            "DejaVuSans.ttf", 65
        )

    except OSError:
        heart_font = ImageFont.load_default()
        percent_font = heart_font

    draw.text(
        (425, 145),
        "♥",
        fill=(255, 55, 125),
        font=heart_font
    )

    draw.text(
        (440, 340),
        f"{percentage}%",
        fill="white",
        font=percent_font
    )

    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)

    return output


class LoveCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="love",
        description="Create a love compatibility picture!"
    )
    @app_commands.describe(
        user1="Choose the first person",
        user2="Choose the second person",
        percentage="Choose a percentage from 1 to 100"
    )
    @app_commands.choices(
        percentage=[
            app_commands.Choice(
                name=f"{i}%",
                value=i
            )
            for i in range(1, 101)
        ]
    )
    async def love(
        self,
        interaction: discord.Interaction,
        user1: discord.Member,
        user2: discord.Member,
        percentage: app_commands.Choice[int]
    ):

        await interaction.response.defer()

        try:
            image = create_love_image(
                user1,
                user2,
                percentage.value
            )

            file = discord.File(
                image,
                filename="love.png"
            )

            await interaction.followup.send(
                content=(
                    f"❤️ {user1.display_name} "
                    f"+ {user2.display_name} ❤️\n"
                    f"Compatibility: {percentage.value}%"
                ),
                file=file
            )

        except Exception as error:
            print(f"Love image error: {error}")

            await interaction.followup.send(
                "Something went wrong creating the picture."
            )


async def setup(bot):
    await bot.add_cog(LoveCommands(bot))
