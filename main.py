import os
import re
import random
import discord
from discord.ext import commands

import skybox_fetcher

pages_dir = 'pages/'
frames_dir = 'frames/'
gif_dir = 'gif/'

with open(os.path.abspath("token.txt"), "r") as f:  # 261184
    TOKEN = f.read()

bot = commands.Bot(command_prefix='$')

current_page = 1
current_frame = -1
current_gif = 2


@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user))


@bot.command()
async def hello(ctx):
    variants = ["Hi, {}!", "Skybox waited for you, {}!", "Greetings, {} =)", "/.//. /../ {}"]
    await ctx.send(random.choice(variants).format(ctx.author.display_name))


@bot.command()
async def download(ctx, arg1):
    async with ctx.typing():
        downloaded = await skybox_fetcher.pull_comic(int(arg1))
        await ctx.send("Downloaded and splitted {} new frames and {} new gif animations!".format(*downloaded))


@bot.command()
async def page(ctx, arg1):
    global current_page

    if arg1 in ("random", "rnd"):
        paths = os.listdir(os.path.abspath(pages_dir))
        img = random.choice(paths)
    else:
        if arg1 in ("next", "forward", "+1"):
            current_page += 1
        elif arg1 in ("previous", "back", "-1"):
            current_page -= 1
        else:
            current_page = int(arg1)
        img = '{}.jpg'.format(current_page)

    async with ctx.typing():
        file = discord.File(os.path.abspath(pages_dir + img), filename=img)
        await ctx.send("Here you go, page {}!".format(img.split('.')[0]), file=file)


@bot.command()
async def frame(ctx, arg1):
    global current_frame

    if arg1 in ("random", "rnd"):
        paths = os.listdir(os.path.abspath(frames_dir))
        img = random.choice(paths)
    else:
        if arg1 in ("next", "forward", "+1"):
            current_frame += 1
        elif arg1 in ("previous", "back", "-1"):
            current_frame -= 1
        else:
            current_frame = int(arg1)
        img = '{}.jpg'.format(current_frame)

    async with ctx.typing():
        file = discord.File(os.path.abspath(frames_dir + img), filename=img)
        await ctx.send("Here you go, frame {}!".format(img.split('.')[0]), file=file)


@bot.command()
async def gif(ctx, arg1):
    global current_gif

    if arg1 in ("random", "rnd"):
        paths = os.listdir(os.path.abspath(gif_dir))
        img = random.choice(paths)
    else:
        if arg1 in ("next", "forward", "+1"):
            current_gif += 1
        elif arg1 in ("previous", "back", "-1"):
            current_gif -= 1
        else:
            current_gif = int(arg1)
        img = '{}.gif'.format(current_gif)

    async with ctx.typing():
        file = discord.File(os.path.abspath(gif_dir + img), filename=img)
        await ctx.send("Here you go, gif {}!".format(img.split('.')[0]), file=file)


@bot.command()
async def spacetalk(ctx, *args):
    vowel_list = {'a', 'e', 'i', 'o', 'u'}
    latin_check = re.compile(r'[a-z]')

    input_msg = " ".join(args).lower()
    out_msg = ""
    for ch in input_msg:
        if latin_check.match(ch):
            if ch == ' ':
                out_msg += ' '
            elif ch in vowel_list:
                out_msg += '-'
            else:
                out_msg += '/'
        else:
            out_msg += ch

    await ctx.send("`{}`".format(out_msg), )  # Some spaceside once told me:
    await ctx.send("{}".format(input_msg), tts=True, delete_after=1)

bot.run(TOKEN.strip())
