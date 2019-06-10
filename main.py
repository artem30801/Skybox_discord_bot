import os
import re
import random
import pickle
import collections
import traceback

import discord
import statistics
from discord.ext import commands
from discord.ext.commands import BucketType
from discord.utils import get
import typing

import skybox_fetcher
import vc_mask

pages_dir = 'pages/'
frames_dir = 'frames/'
gif_dir = 'gif/'
database_file = 'database.txt'

user_votes_file = 'votes.txt'

#https://discordapp.com/api/oauth2/authorize?client_id=569075344938893322&permissions=268958784&scope=bot
with open(os.path.abspath("token.txt"), "r") as f:  # 261184
    TOKEN = f.read()

bot = commands.Bot(command_prefix=('$', '!'), case_insensitive=True)

#current_page = 1
#current_frame = -1
#current_gif = 2


def _default():
    return "", 0


current = collections.defaultdict(_default)

now_downloading = False

data = None
arcs_names = None


async def _download():
    global now_downloading, arcs_names, data

    downloaded = await skybox_fetcher.pull_comic()

    arcs_names, data = None, None
    return downloaded


def get_page_from_frame(dt, current_frame):
    for i, fr in enumerate([x[0] for x in list(dt.values())]):
        if current_frame+1 <= fr:
            return i


@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user))
    print(bot.guilds)


@bot.event
async def on_message(message):
    global now_downloading
    #print(message.guild.name, message.channel.name, str(message.author).split('#')[1])
    if message.guild is not None:
        if message.guild.name == "The Skybox" and message.channel.name == "newest-updates" and str(message.author).split('#')[1] == '8517':
            print("Message from Lynx! New updates!")
            if not now_downloading:
                now_downloading = True
                await message.add_reaction(emoji="👍")
                await _download()
                await message.add_reaction(emoji="✅")
                now_downloading = False
            else:
                await message.add_reaction(emoji="⌛")

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('Heyo! Not so fast! Try again in {0:.2f}s'.format(error.retry_after))
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Sorry, but your arguments are invalid!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Sorry, but you missed required argument!")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("You can use that only in guild!")
    else:
        print(error)
        traceback.print_exc()


@bot.command(aliases=["hi", "hoi", ])
async def hello(ctx):
    variants = \
        ["Hi, {}!",
         "Skybox waited for you, {}!",
         "Greetings, {} =)",
         "/-//- /--/ {}",
         "Oh! Hello there, you must be {}!",
         "G'day, {}!",
         "Howdy, {}",
         ]
    name = discord.ext.commands.HelpCommand().remove_mentions(ctx.author.display_name)
    await ctx.send(random.choice(variants).format(name))


@bot.command()
async def download(ctx):
    global now_downloading
    async with ctx.typing():
        print(now_downloading)
        if not now_downloading:
            now_downloading = True
            await ctx.send("Download process started!")
            downloaded = await _download()
            await ctx.send("Downloaded and split {} new frames and {} new gif animations!".format(*downloaded))
            now_downloading = False

        else:
            await ctx.send("Comic downloading process is already running, just hang out a bit!")


def _get_database(database=database_file):
    global data, arcs_names
    if (data is None) or (arcs_names is None):
        with open(os.path.abspath(database), 'rb') as f:
            file_arc_names, file_data = pickle.load(f)

        data = file_data
        arcs_names = file_arc_names

    return arcs_names, data


@discord.ext.commands.cooldown(1, 2.5, type=BucketType.channel)
@bot.command(name="next", aliases=["forward", "+"])
async def _next(ctx, arg1=""):
    _type = current[ctx.message.channel.id][0]
    if _type == "frame":
        await _frame(ctx, "next", arg1)
    if _type == "page":
        await _page(ctx, "next", arg1)
    if _type == "gif":
        await _gif(ctx, "next", arg1)


@discord.ext.commands.cooldown(1, 2.5, type=BucketType.channel)
@bot.command(name="back", aliases=["previous", "prev", "-"])
async def _back(ctx, arg1=""):
    _type = current[ctx.message.channel.id][0]
    if _type == "frame":
        await _frame(ctx, "back", arg1)
    if _type == "page":
        await _page(ctx, "back", arg1)
    if _type == "gif":
        await _gif(ctx, "back", arg1)


@discord.ext.commands.cooldown(1, 2.5, type=BucketType.channel)
@bot.command()
async def arc(ctx, *args):
    args = list(args)
    arcs, dt = _get_database()
    frame = None
    is_gif = False
    try:
        if args[0].isdigit():
            arc_name = arcs[int(args[0].lstrip("0") or 0)]
        else:
            if args[0].lower() == 'im':
                arc_name = arcs[0]
            else:
                arc_name = args[0].lower().capitalize()

        if len(args) >= 2:
            if not args[1].isdigit():
                args.pop(1)
            page = args[1].zfill(2)

            if len(args) >= 3:
                if not args[2] in ("gif", "-gif", "--gif"):
                    if not args[2].isdigit():
                        args.pop(2)
                    frame = int(args[2].lstrip("0"))-1
                else:
                    is_gif = True
            result = dt[(arc_name, page)]
        else:
            page = "Title"
            try:
                result = dt[(arc_name, page)]
            except KeyError:
                page = "Intro"
                result = dt[(arc_name, page)]

    except (KeyError, ValueError, IndexError):
        async with ctx.typing():
            await ctx.send("Seems there is some mistakes in command! Maybe such page is missing!")
    else:
        with ctx.typing():
            if frame is not None:
                if frame+1 > result[1]:
                    await ctx.send("Frame number is out of range")
                else:
                    ind = result[0]-result[1]+frame
                    current[ctx.message.channel.id] = ("frame", ind)
                    img = '{}.jpg'.format(ind)
                    try:
                        file = discord.File(os.path.abspath(frames_dir + img), filename=img)
                    except FileNotFoundError:
                        await ctx.send("Sorry, but i can't find such frame!")
                    else:
                        await ctx.send("Here you go, frame №{} of Arc {} - {}: Page {} - frame {}/{}".format(
                            ind,
                            arcs_names.index(arc_name),
                            arc_name,
                            page,
                            frame+1,
                            result[1],
                        ), file=file)
            else:
                ind = list(dt.keys()).index((arc_name, page))+2
                if is_gif:
                    current[ctx.message.channel.id] = ("gif", result[0]-result[1])

                    img = '{}.gif'.format(ind)
                    try:
                        file = discord.File(os.path.abspath(gif_dir + img), filename=img)
                    except FileNotFoundError:
                        await ctx.send("Sorry, but i can't find such gif!")
                    else:
                        await ctx.send("Here you go, gif №{} of Arc {} - {}: Page {} ({} frames)".format(
                            ind,
                            arcs_names.index(arc_name),
                            arc_name,
                            page,
                            result[1],
                        ), file=file)
                else:
                    current[ctx.message.channel.id] = ("page", result[0]-result[1])

                    img = '{}.jpg'.format(ind)
                    try:
                        file = discord.File(os.path.abspath(pages_dir + img), filename=img)
                    except FileNotFoundError:
                        await ctx.send("Sorry, but i can't find such page!")
                    else:
                        await ctx.send("Here you go, page №{} of Arc {} - {}: Page {} ({} frames)".format(
                            ind,
                            arcs_names.index(arc_name),
                            arc_name,
                            page,
                            result[1],
                        ), file=file)


@discord.ext.commands.cooldown(1, 2.5, type=BucketType.channel)
@bot.command()
async def page(ctx, arg1="", arg2=""):
    await _page(ctx, arg1, arg2)


async def _page(ctx, arg1="", arg2=""):
    arcs, dt = _get_database()
    _current = get_page_from_frame(dt, current[ctx.message.channel.id][1]) + 2
    if arg1:
        if arg1 in ("random", "rnd"):
            paths = os.listdir(os.path.abspath(pages_dir))
            img = random.choice(paths)
            _current = int(img.split('.')[0])

        else:
            try:
                if arg1 in ("next", "forward", "+"):
                    if arg2:
                        _current += int(arg2)
                    else:
                        _current += 1
                elif arg1 in ("previous", "back", "prev", "-"):
                    if arg2:
                        _current -= int(arg2)
                    else:
                        _current -= 1
                else:
                    _current = int(arg1)
            except ValueError:
                await ctx.send("Hey, that should be a *number*! Integer, ya know")
                return
    img = '{}.jpg'.format(_current)

    item = list(dt.items())[_current-2]

    async with ctx.typing():
        try:
            file = discord.File(os.path.abspath(pages_dir + img), filename=img)
        except FileNotFoundError:
            await ctx.send("Sorry, but i can't find such page!")
        else:
            current[ctx.message.channel.id] = ("page", item[1][0]-item[1][1])
            await ctx.send("Here you go, page №{} of Arc {} - {}: Page {} ({} frames)".format(
                _current,
                arcs_names.index(item[0][0]),
                item[0][0],
                item[0][1],
                item[1][1],
            ), file=file)


@bot.command()
@discord.ext.commands.cooldown(1, 2.5, type=BucketType.channel)
async def frame(ctx, arg1="", arg2=""):
    await _frame(ctx, arg1, arg2)

    if arg1.isdigit() and arg1.isdigit():
        await _vote(ctx, int(arg2))


async def _frame(ctx, arg1="", arg2=""):
    arcs, dt = _get_database()
    _current = current[ctx.message.channel.id][1] or 0

    if arg1:
        if arg1 in ("random", "rnd"):
            paths = os.listdir(os.path.abspath(frames_dir))
            img = random.choice(paths)
            _current = int(img.split('.')[0])
        else:
            try:
                if arg1 in ("next", "forward", "+"):
                    if arg2:
                        _current += int(arg2)
                    else:
                        _current += 1
                elif arg1 in ("previous", "back", "prev", "-"):
                    if arg2:
                        _current -= int(arg2)
                    else:
                        _current -= 1
                else:
                    _current = int(arg1)
            except ValueError:
                await ctx.send("Hey, that should be a *number*! Integer, ya know")
                return
    img = '{}.jpg'.format(_current)

    page = get_page_from_frame(dt, _current)

    item = list(dt.items())[page]

    async with ctx.typing():
        try:
            file = discord.File(os.path.abspath(frames_dir + img), filename=img)
        except FileNotFoundError:
            await ctx.send("Sorry, but i can't find such frame!")
        else:
            current[ctx.message.channel.id] = ("frame", _current)
            await ctx.send("Here you go, frame №{} of Arc {} - {}: Page {} - frame {}/{}".format(
                _current,
                arcs_names.index(item[0][0]),
                item[0][0],
                item[0][1],
                item[1][1] - (item[1][0] - _current) + 1,
                item[1][1],
            ), file=file)


@discord.ext.commands.cooldown(1, 2.5, type=BucketType.channel)
@bot.command()
async def gif(ctx, arg1="", arg2=""):
    await _gif(ctx, arg1, arg2)


async def _gif(ctx, arg1="", arg2="", change_current=True):
    arcs, dt = _get_database()
    _current = get_page_from_frame(dt, current[ctx.message.channel.id][1]) + 2

    if arg1:
        if arg1 in ("random", "rnd"):
            paths = os.listdir(os.path.abspath(gif_dir))
            img = random.choice(paths)
            _current = int(img.split('.')[0])

        else:
            try:
                if arg1 in ("next", "forward", "+"):
                    if arg2:
                        _current += int(arg2)
                    else:
                        _current += 1
                elif arg1 in ("previous", "back", "prev", "-"):
                    if arg2:
                        _current -= int(arg2)
                    else:
                        _current -= 1
                else:
                    _current = int(arg1)
            except ValueError:
                await ctx.send("Hey, that should be a *number*! Integer, ya know")
                return
    img = '{}.gif'.format(_current)

    async with ctx.typing():
        try:
            file = discord.File(os.path.abspath(gif_dir + img), filename=img)
        except FileNotFoundError:
            await ctx.send("Sorry, but i can't find such gif!")
        else:
            if _current > 2:
                item = list(dt.items())[_current - 2]
                if change_current:
                    current[ctx.message.channel.id] = ("gif", item[1][0] - item[1][1])

                await ctx.send("Here you go, gif №{} of Arc {} - {}: Page {} ({} frames)".format(
                    _current,
                    arcs_names.index(item[0][0]),
                    item[0][0],
                    item[0][1],
                    item[1][1],
                ), file=file)
            else:
                await ctx.send("Here you go, bonus gif №{}".format(_current), file=file)


def add_to_voted(index, value, user):
    if os.path.exists(os.path.abspath(user_votes_file)):
        with open(os.path.abspath(user_votes_file), 'rb') as f:
            votes = pickle.load(f)
    else:
        votes = collections.defaultdict(dict)

    votes[index].update({user: value})

    with open(os.path.abspath(user_votes_file), 'wb') as f:
        pickle.dump(votes, f)

    print(votes)
    return votes[index]


@bot.command(aliases=["v", "delay"])
async def vote(ctx, timing: int):
    await _vote(ctx, timing)


async def _vote(ctx, timing):
    if current[ctx.message.channel.id][0] == "frame":
        if timing in range(50, 5000+1):
            _current = current[ctx.message.channel.id][1]
            voted = add_to_voted(_current, timing, ctx.author.id)

            current_votes = ""
            for key, val in voted.items():
                name = get(bot.get_all_members(), id=key)
                current_votes += "\n {}: {} ms ".format(name.display_name or name, val)
            avg_votes = "\n *Average vote*: {} ms".format(round(statistics.mean(voted.values())))

            await ctx.send("Thanks! You are successfully voted for frame {}".format(_current))
            await ctx.send("Current votes are:"+current_votes+avg_votes)
        else:
            await ctx.send("That timing doesn't seem right... Try using range of 50 - 5000 milliseconds (1/1000 of second)")
    else:
        await ctx.send("Hey! You must vote for in-animation duration of certain *frame*!")


@discord.ext.commands.cooldown(1, 6, type=BucketType.default)
@bot.command(aliases=["regen", "r"])
async def regen_gif(ctx, arg1=""):
    arcs, dt = _get_database()
    if arg1:
        try:
            _current = int(arg1)
        except ValueError:
            await ctx.send("Hey, that should be a gif *number*!")
            return
    else:
        _current = get_page_from_frame(dt, current[ctx.message.channel.id][1]) + 2

    item = list(dt.items())[_current - 2]
    frame_num = item[1][0] - item[1][1]

    img = '{}.gif'.format(_current)
    try:
        os.remove(os.path.abspath(gif_dir+img))
    except FileNotFoundError:
        pass

    await skybox_fetcher.split_page('{}.jpg'.format(_current), frame_num, pages_dir, frames_dir, gif_dir, True)
    print("Gif {} regenerated".format(_current))
    await ctx.send("Gif {} successfully regenerated!".format(_current))
    await _gif(ctx, str(_current), change_current=False)


@bot.command(aliases=["st", ])
async def spacetalk(ctx, *, message: str):
    message = message.lower()
    out_msg = re.sub('[aeiou]', '-', message)
    out_msg = re.sub('[аеёиоуыэюяй]', '-', out_msg)
    out_msg = re.sub('--', '—', out_msg)
    out_msg = re.sub('[b-df-hyj-np-tv-xz]', '/', out_msg)
    out_msg = re.sub('[кнгшщзхфвпрлдчсмтжбцьъ]', '/', out_msg)

    await ctx.send("`{}`".format(out_msg))  # Some spaceside once told me:


@bot.command(aliases=["translate_word", "unspasetalk_word", "ustw"])
async def decipher_word(ctx, word: str, max_words: int = 100):
    result = list(vc_mask.mask_match(word))
    res_len = len(result)
    s = " | ".join(result[:max_words])
    await ctx.send("Found {} word matches (showing first {}): \n {}".format(res_len, min(res_len, max_words), s))


@bot.command(aliases=["translate", "unspasetalk", "ust"])
async def decipher(ctx, mutate_num: typing.Optional[int] = 20, words_num: typing.Optional[int] = 5, *words):
    result = list(vc_mask.sentence_match(*words, wordnum=words_num))
    res_len = len(result)
    s = "\n".join([" ".join(x) for x in result[:mutate_num]])
    await ctx.send("Possible {} translation variants (of {} possible permutations) are: \n".format(
        min(res_len, mutate_num), res_len)+s)


@bot.command(hidden=True)
async def database(ctx):
    async with ctx.typing():
        try:
            file1 = discord.File(os.path.abspath(database_file), filename=database_file)
            file2 = discord.File(os.path.abspath(user_votes_file), filename=user_votes_file)

        except FileNotFoundError:
            await ctx.send("Sorry, but i can't find mah database!")
        else:
            await ctx.send("Here you go, my full database!", file=file1)
            await ctx.send("Here you go, my full votes database!", file=file2)


@bot.command(aliases=["stream", "crew", "stream_crew"])
@discord.ext.commands.guild_only()
async def streamcrew(ctx, arg=""):
    role = discord.utils.get(ctx.guild.roles, name="livestream crew")
    if role is None:
        await ctx.send("Sorry, but no such role here available!")
        return
    user = ctx.message.author
    if arg in ("no", "off", "exit", "leave", "-"):
        await user.remove_roles(role)
        await ctx.send("Goodbye!")
    else:
        await user.add_roles(role)
        await ctx.send("Welcome to stream crew!")


skybox_roles = {
    #"livestream crew": discord.Colour(0xA652BB),
    "Shanti": discord.Colour(0x0000FF),
    "Rachel": discord.Colour(0xFF0000),
    "Pegaside": discord.Colour(0x9f72f3),
    "Gryphside": discord.Colour(0x72a3f2),
    "Zalside": discord.Colour(0x70f290),
    "Nixside": discord.Colour(0xeb1f20),
    "Drakeside": discord.Colour(0xf3ef72),
    "Spaceside": discord.Colour(0x010101),

}


@bot.command(aliases=["chose_side", "pick_side", "side_pick", "sider"])
@discord.ext.commands.guild_only()
async def side(ctx, arg: str):
    if arg in ("setup", "refresh", "reload"):
        for role_name, col in skybox_roles.items():
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role is not None:
                await role.edit(colour=col)
            else:
                await ctx.guild.create_role(name=role_name, colour=col)
        await ctx.send("(re)created skybox roles!")
        return

    user = ctx.message.author

    if arg in ("none", "noside", "no", "off", "exit", "leave", "-"):
        for role_name in skybox_roles.keys():
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            await user.remove_roles(role)
        await ctx.send("You're now a *noside*! Is that what you wanted?")
        return

    if arg in ("all", "list", "view", "help", "halp"):
        sides = ""
        for key in skybox_roles.keys():
            sides += "\n {}".format(key)
        await ctx.send("Current available siders roles: {}".format(sides))
        return

    if arg.title() in skybox_roles.keys():
        s = arg.title()
    elif "sider"in arg.lower():
        s = arg.title()[:-1]
    elif "side" in arg.lower():
        s = arg.title()
    else:
        s = arg.title()+"side"

    if s in skybox_roles.keys():
        for role_name in skybox_roles.keys():
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role is not None and role in user.roles:
                await user.remove_roles(role)

        role = discord.utils.get(ctx.guild.roles, name=s)
        if role is not None:
            await user.add_roles(role)
            await ctx.send("You're now a {}!".format(s))
        else:
            await ctx.send("There is no such side role! Try to '!side setup'")
    else:
        await ctx.send("Sorry, but there is no such side!")


@bot.command(hidden=True)
@discord.ext.commands.guild_only()
async def side_delete(ctx):
    for role_name in skybox_roles.keys():
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is not None:
            await role.delete()
    await ctx.send("Deleted all 'side' roles.")


bot.run(TOKEN.strip())
