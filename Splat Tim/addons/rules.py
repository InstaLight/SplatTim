import discord
from discord.ext import commands
# from discord.ext.commands import cooldown
from sys import argv

class Rules:
    """
    Read The rules.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def simple_embed(self, text, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = text
        await self.bot.say("", embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def r1(self):
        """Lists rule 1"""
        await self.bot.say("```Be nice to each other. It's fine to disagree, it's not fine to insult or attack other people.```")

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def r2(self):
        """Lists rule 2"""
        await self.bot.say("```This is an English-speaking server, so please speak English to keep communication simple.```")

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def r3(self):
        """Lists rule 3"""
        await self.bot.say("```One account per user. Bots/fully automated clients run by users are not allowed. Alternate accounts will have access removed. If you are switching accounts, please remove your original from the server.```")

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def r4(self):
        """Lists rule 4"""
        await self.bot.say("```User-side scripts are fine if they are only accessible by you and are not annoying. Community-accessible triggers on a user account are a violation of the Discord Terms of Service.```")

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def r5(self):
        """Lists rule 5"""
        await self.bot.say("```Not-safe-for-work content (including gore and other shock content) goes in #nsfw.```")

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def r6(self):
        """Lists rule 6"""
        await self.bot.say("```Don't post other people's personal information, including social media accounts with this. This may warrant an immediate ban.```")

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def r7(self):
        """Lists rule 7"""
        await self.bot.say("```Ask a staff member before posting invite links to things like servers on Discord, Skype groups, etc.```")

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def r8(self):
        """Lists rule 8"""
        await self.bot.say("```Voice and music command usage belong in #voice-and-music and will only work in voice and music.```")

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def r9(self):
        """Lists rule 9"""
        await self.bot.say("```Trying to evade, look for loopholes, or stay borderline within the rules will be treated as breaking them.```")

def setup(bot):
    bot.add_cog(Rules(bot))
