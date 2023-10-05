from discord.ext import commands
from discord.ext.commands import Bot
import discord
import random
import json
from roll import roll_
from minesweeper import Minesweeper
from chadcounter import WordCounter

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
chadCounter = WordCounter("chadcount.json", 'chad')


# Confirm logon
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

# Message event handler
# Someday this should be it's own class in it's own file
@bot.event
async def on_message(message): #Note this overrides the previous event on_message
    #this is the only thing we're doing with message so far
    result = chadCounter.parseMessage(message)

    await bot.process_commands(message)

@bot.command()
async def chadcount(ctx):
    count = chadCounter.getCount()
    if not count:
        await ctx.send("Something went wrong with the chad counter, someone here should figure that out")
    else:
        await ctx.send("Total times the word \"" + chadCounter.word + "\" has been said: " + str(count)) 

# Grab random quote
@bot.command()
async def quote(ctx):
    try:
        with open("./quotes.json", "r") as r:
            j = json.load(r)
            all_quotes = j["quotes"]
            r.close()
    except:
        await ctx.send("No quotes stored! Add it using the !addquote command")
        return

    await ctx.send(random.choice(all_quotes))


# Add a quote (use format "!addquote "*insert quote here*"")
@bot.command()
async def addquote(ctx, quote_):

    filename = "./quotes.json" #For clarity - Mtlfs
    
    def add_quote(quote, file=filename):
        with open(file, "r+") as fw:
            j = json.load(fw)
            j["quotes"].append(quote)
            with open(file, "w+") as wp:
                wp.write(json.dumps(j))
                wp.close()
            fw.close()

    try:
        with open(filename, "r") as f:
            pass
            f.close()
    except:
        with open(filename, "w+") as wp:
            wp.write('{"quotes" : []}')
            wp.close()
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

# Minesweeper
@bot.command()
async def minesweeper(ctx, size=9, num_mines=5):
    if size < 2 or size > 9 or num_mines > size*size or num_mines == size*size:
        embed = discord.Embed(
            title="Error", description="Error creating board. Size must be less than 9 and the number of mines cannot be larger than the amount of cells", color=0xDF0000
        )
    else:
        m = Minesweeper(size, num_mines)
        m.initialize_board()
        embed = discord.Embed(
            title=f"Minesweeper: {size}x{size} - {num_mines} mines", description=m.get_board(), color=discord.Color.blue()
        )
    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)
