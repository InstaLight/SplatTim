import discord
from discord.ext import commands
from sys import argv

class Memes:
    """
    Meme commands
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        
    async def _meme(self, ctx, msg):
        author = ctx.message.author
        if ctx.message.channel.name[0:5] == "help-" or "assistance" in ctx.message.channel.name:
            await self.bot.delete_message(ctx.message)
            try:
                await self.bot.send_message(author, "Meme commands are disabled in this channel, or your privileges have been revoked.")
            except discord.errors.Forbidden:
                await self.bot.say(author.mention + " Meme commands are disabled in this channel, or your privileges have been revoked.")
        else:
            await self.bot.say(self.bot.escape_name(ctx.message.author.display_name) + ": " + msg)

    # list memes
    @commands.command(name="listmemes", pass_context=True)
    async def _listmemes(self, ctx):
        """List meme commands."""
        # this feels wrong...
        funcs = dir(self)
        msg = "```\n"
        msg += ", ".join(func for func in funcs if func != "bot" and func[0] != "_")
        msg += "```"
        await self._meme(ctx, msg)

    # Splat Tim memes
    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def splattim(self, ctx):
        """Memes."""
        await self._meme(ctx, "it splat tim\nhttp://i.imgur.com/qpOXdnd.jpg")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def woomy(self, ctx):
        """Memes."""
        await self._meme(ctx, "WOOMY!\nhttps://www.youtube.com/watch?v=SE9pySihYpA ")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def splattina(self, ctx):
        """Memes."""
        await self._meme(ctx, "she does it too!\nhttp://i.imgur.com/3I6muSu.jpg")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def comcast(self, ctx):
        """Memes."""
        await self._meme(ctx, "http://i.imgur.com/DWawpw6.gif")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def eatthatpussy445(self, ctx):
        """Memes."""
        await self._meme(ctx, "https://www.youtube.com/watch?v=1_X_64cfnE0")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def h(self, ctx):
        """Memes."""
        await self._meme(ctx, "```  _     \n | |__  \n | '_ \ \n | | | |\n |_| |_|\n        ```")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def nicememe(self, ctx):
        """Memes."""
        await self._meme(ctx, "http://niceme.me/")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def succ(self, ctx):
        """Memes."""
        await self._meme(ctx, "https://www.youtube.com/watch?v=fPNdWnwuBDI")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def autistic(self, ctx):
        """Memes."""
        await self._meme(ctx, "http://i.imgur.com/LWI4H5l.jpg")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def bamboozler(self, ctx):
        """Memes."""
        await self._meme(ctx, "http://i.imgur.com/7tjDeaZ.jpg")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def shitdick(self, ctx):
        """Memes."""
        await self._meme(ctx, "https://www.youtube.com/watch?v=ancB4B6_VKQ")

    @commands.command(pass_context=True, hidden=True)
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.channel)
    async def derekbrick(self, ctx):
        """Memes."""
        await self._meme(ctx, "http://i.imgur.com/f5Szs6J.png \n http://i.imgur.com/8njZTRL.png")


# Load the extension
def setup(bot):
    bot.add_cog(Memes(bot))
