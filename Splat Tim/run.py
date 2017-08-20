#!/usr/bin/env python3

# Kurisu by 916253 & ihaveamac
# license: Apache License 2.0
# https://github.com/916253/Kurisu
# Modified by Zewia and Sentry
# https://github.com/Zewia/Splat-Tim

description = """
Splat Tim, he does it all.
"""

# import dependencies
import os
from discord.ext import commands
import discord
import datetime
import json, asyncio
import copy
import configparser
import traceback
import sys
import os
import re

# sets working directory to bot's folder
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# read config for token
config = configparser.ConfigParser()
config.read("config.ini")

os.makedirs("data", exist_ok=True)
os.makedirs("data/ninupdates", exist_ok=True)
# create warns.json if it doesn't exist
if not os.path.isfile("data/warns.json"):
    with open("data/warns.json", "w") as f:
        f.write("{}")

# create restrictions.json if it doesn't exist
if not os.path.isfile("data/restrictions.json"):
    with open("data/restrictions.json", "w") as f:
        f.write("{}")

# create staff.json if it doesn't exist
if not os.path.isfile("data/staff.json"):
    with open("data/staff.json", "w") as f:
        f.write("{}")

# create helpers.json if it doesn't exist
if not os.path.isfile("data/helpers.json"):
    with open("data/helpers.json", "w") as f:
        f.write("{}")

# create timebans.json if it doesn't exist
if not os.path.isfile("data/timebans.json"):
    with open("data/timebans.json", "w") as f:
        f.write("{}")

# create softbans.json if it doesn't exist
if not os.path.isfile("data/softbans.json"):
    with open("data/softbans.json", "w") as f:
        f.write("{}")

# create watch.json if it doesn't exist
if not os.path.isfile("data/watch.json"):
    with open("data/watch.json", "w") as f:
        f.write("{}")

prefix = ['!', '.']
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None)

bot.actions = []  # changes messages in mod-/server-logs
with open("data/watch.json", "r") as f:
    bot.watching = json.load(f)  # post user messages to messaage-logs

# http://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
chars = "\\`*_<>#@:~"
def escape_name(name):
    name = str(name)
    for c in chars:
        if c in name:
            name = name.replace(c, "\\" + c)
    return name.replace("@", "@\u200b")  # prevent mentions
bot.escape_name = escape_name

bot.pruning = False  # used to disable leave logs if pruning, maybe.

# mostly taken from https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/bot.py
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.CommandNotFound):
        pass  # ...don't need to know if commands don't exist
    if isinstance(error, commands.errors.CheckFailure):
        await bot.send_message(ctx.message.channel, "{} You don't have permission to use this command.".format(ctx.message.author.mention))
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        formatter = commands.formatter.HelpFormatter()
        await bot.send_message(ctx.message.channel, "{} You are missing required arguments.\n{}".format(ctx.message.author.mention, formatter.format_help_for(ctx, ctx.command)[0]))
    elif isinstance(error, commands.errors.CommandOnCooldown):
        try:
            await bot.delete_message(ctx.message)
        except discord.errors.NotFound:
            pass
        message = await bot.send_message(ctx.message.channel, "{} This command was used {:.2f}s ago and is on cooldown. Try again in {:.2f}s.".format(ctx.message.author.mention, error.cooldown.per - error.retry_after, error.retry_after))
        await asyncio.sleep(10)
        await bot.delete_message(message)
    else:
        await bot.send_message(ctx.message.channel, "An error occured while processing the `{}` command.".format(ctx.command.name))
        print('Ignoring exception in command {0.command} in {0.message.channel}'.format(ctx))
        mods_msg = "Exception occured in `{0.command}` in {0.message.channel.mention}".format(ctx)
        # traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        print(''.join(tb))
        await bot.send_message(bot.boterr_channel, mods_msg + '\n```' + ''.join(tb) + '\n```')

# mostly taken from https://github.com/Rapptz/discord.py/blob/async/discord/client.py
@bot.event
async def on_error(event_method, *args, **kwargs):
    if isinstance(args[0], commands.errors.CommandNotFound):
        # for some reason runs despite the above
        return
    print('Ignoring exception in {}'.format(event_method))
    mods_msg = "Exception occured in {}".format(event_method)
    tb = traceback.format_exc()
    print(''.join(tb))
    mods_msg += '\n```' + ''.join(tb) + '\n```'
    mods_msg += '\nargs: `{}`\n\nkwargs: `{}`'.format(args, kwargs)
    await bot.send_message(bot.boterr_channel, mods_msg)
    print(args)
    print(kwargs)

bot.all_ready = False
bot._is_all_ready = asyncio.Event(loop=bot.loop)
async def wait_until_all_ready():
    """Wait until the entire bot is ready."""
    await bot._is_all_ready.wait()
bot.wait_until_all_ready = wait_until_all_ready

@bot.event
async def on_ready():
    # this bot should only ever be in one server anyway
    for server in bot.servers:
        bot.server = server
        if bot.all_ready:
            break

        print("{} has started! {} has {:,} members!".format(bot.user.name, server.name, server.member_count))

        # channels
        bot.welcome_channel = discord.utils.get(server.channels, name="welcome")
        bot.announcements_channel = discord.utils.get(server.channels, name="announcements")
        bot.voiceandmusic_channel = discord.utils.get(server.channels, name="voice-and-music")
        bot.elsewhere_channel = discord.utils.get(server.channels, name="nsfw")
        bot.mods_channel = discord.utils.get(server.channels, name="staff-chat")
        bot.modlogs_channel = discord.utils.get(server.channels, name="mod-logs")
        bot.serverlogs_channel = discord.utils.get(server.channels, name="server-logs")
        bot.messagelogs_channel = discord.utils.get(server.channels, name="message-logs")
        bot.watchlogs_channel = discord.utils.get(server.channels, name="watch-logs")
        bot.boterr_channel = discord.utils.get(server.channels, name="bot-err")
        bot.eventchat_channel = discord.utils.get(server.channels, name="cancer")

        # roles
        bot.op_role = discord.utils.get(server.roles, name="Fresh!")
        bot.superop_role = discord.utils.get(server.roles, name="SquidKid")
        bot.owner_role = discord.utils.get(server.roles, name="Woomy")
        bot.trusted_role = discord.utils.get(server.roles, name="Trusted")
        bot.muted_role = discord.utils.get(server.roles, name="Muted")
        bot.elsewhere_role = discord.utils.get(server.roles, name="nsfw")
        bot.eventchat_role = discord.utils.get(server.roles, name="cancer")
        bot.helpers_role = discord.utils.get(server.roles, name="Woomy")
        bot.everyone_role = server.default_role

        bot.staff_ranks = {
            "Fresh!": bot.op_role,
            "SquidKid": bot.superop_role,
            "Woomy": bot.owner_role,
        }

        # load timebans
        with open("data/timebans.json", "r") as f:
            timebans = json.load(f)
        bot.timebans = {}
        timebans_i = copy.copy(timebans)
        for user_id, timestamp in timebans_i.items():
            found = False
            for user in await bot.get_bans(server):
                if user.id == user_id:
                    bot.timebans[user_id] = [user, datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"), False]  # last variable is "notified", for <=30 minute notifications
                    found = True
                    break
            if not found:
                timebans.pop(user_id)  # somehow not in the banned list anymore so let's just remove it
        with open("data/timebans.json", "w") as f:
            json.dump(timebans, f)

        bot.all_ready = True
        bot._is_all_ready.set()

        # softban check
        with open("data/softbans.json", "r") as f:
            softbans = json.load(f)
        for member in server.members:
            if member.id in softbans:
                await bot.send_message(member, "This account has not been permitted to participate in {}. The reason is: {}".format(bot.server.name, softbans[member.id]["reason"]))
                bot.actions.append("sbk:" + member.id)
                await bot.kick(member)
                msg = "🚨 **Attempted join**: {} is soft-banned by <@{}> | {}#{}".format(member.mention, softbans[member.id]["issuer_id"], bot.escape_name(member.name), member.discriminator)
                embed = discord.Embed(color=discord.Color.red())
                embed.description = softbans[member.id]["reason"]
                await bot.send_message(bot.serverlogs_channel, msg, embed=embed)
                return

        break

# loads extensions
addons = [
    'addons.auto_probation',
    'addons.extras',
    'addons.kickban',
    'addons.load',
    'addons.lockdown',
    'addons.logs',
    'addons.memes',
    'addons.mod',
    'addons.mod_warn',
    'addons.mod_watch',
    'addons.nxerr',
    'addons.rules',
    'addons.splatoon',
    'addons.friendcode',
]

failed_addons = []

for extension in addons:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
        failed_addons.append([extension, type(e).__name__, e])

# Execute
print('Bot directory: ', dir_path)
bot.run(config['Main']['token'])
