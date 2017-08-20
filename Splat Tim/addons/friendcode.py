import discord
import hashlib
import sqlite3
import struct
from re import sub
from discord.ext import commands
from random import randint
from json import decoder, dump, load
from os import replace
from os.path import splitext

class DataIO():

    def save_json(self, filename, data):
        """Atomically save a JSON file given a filename and a dictionary."""
        path, ext = splitext(filename)
        tmp_file = "{}.{}.tmp".format(path, randint(1000, 9999))
        with open(tmp_file, 'w', encoding='utf-8') as f:
            dump(data, f, indent=4,sort_keys=True,separators=(',',' : '))
        try:
            with open(tmp_file, 'r', encoding='utf-8') as f:
                data = load(f)
        except decoder.JSONDecodeError:
            print("Attempted to write file {} but JSON "
                                  "integrity check on tmp file has failed. "
                                  "The original file is unaltered."
                                  "".format(filename))
            return False
        except Exception as e:
            print('A issue has occured saving ' + filename + '.\n'
                  'Traceback:\n'
                  '{0} {1}'.format(str(e), e.args))
            return False

        replace(tmp_file, filename)
        return True

    def load_json(self, filename):
        """Load a JSON file and return a dictionary."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = load(f)
            return data
        except Exception as e:
            print('A issue has occured loading ' + filename + '.\n'
                  'Traceback:\n'
                  '{0} {1}'.format(str(e), e.args))
            return {}

    def is_valid_json(self, filename):
        """Verify that a JSON file exists and is readable. Take in a filename and return a boolean."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = load(f)
            return True
        except (FileNotFoundError, decoder.JSONDecodeError):
            return False
        except Exception as e:
            print('A issue has occured validating ' + filename + '.\n'
                  'Traceback:\n'
                  '{0} {1}'.format(str(e), e.args))
            return False

dataIO = DataIO()


class FriendCode:
    """
    Stores and obtains friend codes using an SQLite 3 database.
    """
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/friendcodes.json')
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    # based on https://github.com/megumisonoda/SaberBot/blob/master/lib/saberbot/valid_fc.rb
    def verify_fc(self, fc, console:str='3ds'):
        if console.lower() == 'switch':
            fc = int(fc.lower().replace('sw-', '').replace('-', ''))
            return fc
        elif console.lower() == '3ds':
            fc = int(fc.replace('-', ''))
            if fc > 0x7FFFFFFFFF or fc < 0x0100000000:
                return None
            principal_id = fc & 0xFFFFFFFF
            checksum = (fc & 0xFF00000000) >> 32
            return (fc if hashlib.sha1(struct.pack('<L', principal_id)).digest()[0] >> 1 == checksum else None)
        else:
            return False

    def fc_to_string(self, fc):
        fc = str(fc).rjust(12, '0')
        return "{} - {} - {}".format(fc[0:4], fc[4:8], fc[8:12])

    @commands.group(pass_context=True)
    async def fcregister(self, ctx):
        if ctx.invoked_subcommand is None:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)

    @fcregister.command(name='3ds', pass_context=True)
    async def threedsregister(self, ctx, *, fc:str):
        """Add your friend code."""
        fc = self.verify_fc(fc)
        if not fc:
            await self.bot.say("This friend code is invalid.")
            return
        if not ctx.message.author.id in self.settings:
            self.settings.update({ctx.message.author.id:{'3ds':'','switch':''}})
            dataIO.save_json('data/friendcodes.json', self.settings)
        if self.settings[ctx.message.author.id]['3ds'] == fc:
            await self.bot.say('That is your current Friend Code')
            return
        elif self.settings[ctx.message.author.id]['3ds']:
            await self.bot.say("Please delete your current friend code with `.fcdelete 3ds` before adding another.")
            return
        self.settings[ctx.message.author.id]['3ds'] = fc
        dataIO.save_json('data/friendcodes.json', self.settings)
        await self.bot.say("{} Friend code inserted: {}".format(ctx.message.author.mention, self.fc_to_string(fc)))

    @fcregister.command(name='switch', pass_context=True)
    async def switchregister(self, ctx, fc):
        """Add your friend code."""
        fc = self.verify_fc(fc, 'switch')
        if not fc:
            await self.bot.say("This friend code is invalid.")
            return
        if not ctx.message.author.id in self.settings:
            self.settings.update({ctx.message.author.id:{'3ds':'','switch':''}})
            dataIO.save_json('data/friendcodes.json', self.settings)
        if self.settings[ctx.message.author.id]['switch'] == fc:
            await self.bot.say('That is your current Friend Code')
            return
        elif self.settings[ctx.message.author.id]['switch']:
            await self.bot.say("Please delete your current friend code with `.fcdelete 3ds` before adding another.")
            return
        self.settings[ctx.message.author.id]['switch'] = fc
        dataIO.save_json('data/friendcodes.json', self.settings)
        await self.bot.say("{} Friend code inserted: {}".format(ctx.message.author.mention, self.fc_to_string(fc)))

    @commands.group(pass_context=True)
    async def fcquery(self, ctx):
        if ctx.invoked_subcommand is None:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)

    @fcquery.command(name='3ds', pass_context=True)
    async def threedsquery(self, ctx, user:discord.Member):
        """Get other user's friend code. You must have one yourself in the database."""
        if not ctx.message.author.id in self.settings:
            await self.bot.say("You need to register your own friend code with `.fcregister switch <friendcode>` before getting others.")
            return
        elif not user.id in self.settings:
            await self.bot.say("This user does not have a registered friend code.")
            return
        else:
            await self.bot.say("{} friend code is {}".format(user.name, self.fc_to_string(self.settings[user.id]['3ds'])))
            try:
                await self.bot.send_message(user, "{} has asked for your friend code! Their code is {}.".format(ctx.message.author.display_name, self.fc_to_string(self.settings[user.id]['3ds'])))
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            return
        await self.bot.say("You need to register your own friend code with `.fcregister 3ds <friendcode>` before getting others.")

    @fcquery.command(name='switch', pass_context=True)
    async def switchquery(self, ctx, user:discord.Member):
        """Get other user's friend code. You must have one yourself in the database."""
        if not ctx.message.author.id in self.settings:
            await self.bot.say("You need to register your own friend code with `.fcregister switch <friendcode>` before getting others.")
            return
        elif not user.id in self.settings:
            await self.bot.say("This user does not have a registered friend code.")
            return
        else:
            await self.bot.say("sw-{} friend code is {}".format(user.name, self.fc_to_string(self.settings[user.id]['switch'])))
            try:
                await self.bot.send_message(user, "{} has asked for your friend code! Their code is {}.".format(ctx.message.author.display_name, self.fc_to_string(self.settings[user.id]['switch'])))
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            return

    @commands.group(pass_context=True)
    async def fcdelete(self, ctx):
        if ctx.invoked_subcommand is None:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)

    @fcdelete.command(name='3ds', pass_context=True)
    async def threedsdelete(self, ctx):
        """Delete your friend code."""
        self.settings[ctx.message.author.id]['3ds'] = ''
        dataIO.save_json('data/friendcodes.json', self.settings)
        await self.bot.say("Friend code removed from database.")

    @fcdelete.command(name='switch', pass_context=True)
    async def switchdelete(self, ctx):
        """Delete your friend code."""
        self.settings[ctx.message.author.id]['switch'] = ''
        dataIO.save_json('data/friendcodes.json', self.settings)
        await self.bot.say("Friend code removed from database.")

    @commands.group(pass_context=True)
    async def fctest(self, ctx):
        if ctx.invoked_subcommand is None:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)

    @fctest.command(name='3ds')
    async def threedstest(self, fc):
        fc = self.verify_fc(fc)
        if fc:
            await self.bot.say(self.fc_to_string(fc))
        else:
            await self.bot.say("invalid")

    @fctest.command(name='switch')
    async def switchtest(self, fc):
        fc = self.verify_fc(fc, 'switch')
        if fc:
            await self.bot.say(self.fc_to_string(fc))
        else:
            await self.bot.say("invalid")

def check_file():

    if not dataIO.is_valid_json("data/friendcodes.json"):
        print("[FriendCode]Creating friendcodes.json...")
        dataIO.save_json("data/friendcodes.json", {})

def setup(bot):
    check_file()
    bot.add_cog(FriendCode(bot))
