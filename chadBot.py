from discord.ext import commands
from discord.ext.commands import Bot
import discord
import random
import json
from roll import roll_

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


# This could be useful

"""

username = str(message.author).split('#')[0]
user_message = str(message.content)
channel = str(message.channel.name)

"""

intents = discord.Intents.all()

# Bot command prefix
bot = Bot(command_prefix="!", intents=intents)


# Confirm logon
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


# Grab random quote
@bot.command()
async def quote(ctx):
    try:
        with open("./quotes.json", "r") as r:
            j = json.load(r)
            all_quotes = j["quotes"]
    except:
        await ctx.send("No quotes stored! Add it using the !addquote command")
        return

    await ctx.send(random.choice(all_quotes))


# Add a quote (use format "!addquote "*insert quote here*"")
@bot.command()
async def addquote(ctx, quote_):
    def add_quote(quote, file="./quotes.json"):
        with open(file, "r+") as fw:
            j = json.load(fw)
            j["quotes"].append(quote)
            with open(file, "w+") as wp:
                wp.write(json.dumps(j))

    try:
        with open("./quotes.json", "r"):
            pass
    except:
        with open("./quotes.json", "w+") as wp:
            wp.write('{"quotes" : []}')
    finally:
        add_quote(quote_)
        await ctx.send("Quote added!")


# Say hello
@bot.command()
async def hello(ctx):
    username = str(ctx.author).split("#")[0]
    await ctx.send(f"Hello {username}!")


# Say bye
@bot.command()
async def bye(ctx):
    username = str(ctx.author).split("#")[0]
    await ctx.send(f"Goodbye {username}!")


# Next!!!
@bot.command()
async def next(ctx):
    await ctx.send(f"NEXT!!!")


# Link to the full Morbius movie
@bot.command()
async def morb(ctx):
    await ctx.send("https://www.youtube.com/watch?v=CBn7Ctjh9Mk")


# Roll dice in format "(number of dice)d(sides on dice)"  Example: 1d20
@bot.command()
async def roll(ctx, dice):
    # uses roll_() function from roll.py
    result = roll_(dice)
    if result > 0:
        embed = discord.Embed(
            title="Your Roll", description=str(result), color=0xDF0000
        )
    else:
        embed = discord.Embed(
            title="Error", description="You BETA! Try rolling dice REALISTICALLY this time!", color=0xDF0000
        )
    await ctx.send(embed=embed)


# Make a bubble popping game
@bot.command()
async def pop(ctx):
    # string for the game (a word with two pipes on both sides of it is marked with the spoiler tag that requires users to click it to see it)
    pop = """\n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||
    ||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||
    ||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||
    ||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||
    ||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||
    ||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||
    ||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||
    ||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||
    ||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||
    ||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n"""

    # embed the result
    embed = discord.Embed(
        title="Popping Game!", description=pop, color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


@bot.command()
async def inputs(ctx, input1, input2):
    await ctx.send(f"{input1}, {input2}")

# Run the bot
bot.run(TOKEN)
