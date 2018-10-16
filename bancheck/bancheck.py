import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
from dbans import DBans
import aiohttp
import discord
import asyncio
import json

dBans = DBans(token="TKDcIwZaeb")
DEFAULT = {
"ENABLED" : True,
"guild" : None}

BaseCog = getattr(commands, "Cog", object)
client = discord.Client()

class BanList():

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 54564894107)
        self.config.register_guild(**{"ENABLED":True})
        self.users = {}
        self.messages = {}
    
    @checks.admin_or_permissions(manager_server=True)
    @commands.group(pass_context=True)
    async def bancheck(self, ctx):
        """Check if users are banned on bans.discordlist.com"""


    async def check(userid):
        headers = {'Authorization': 'TKDcIwZaeb'}
        url = "https://bans.discord.id/api/check.php?user_id=" + userid
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url, headers = headers)
            final = await resp.text()
            resp.close()
        data = json.loads(final)
        result = []
        for s in data:
            if s["banned"] == "0":
                result.append(["0"])
            elif s["banned"] == "1":
                result.append(["1", s["case_id"], s["reason"], s["proof"]])
        return result
            
            
    @bancheck.command(name='search', pass_context=True, no_pm=True)
    async def _channel(self, ctx, user:discord.Member=None):
       if ctx.message.author.bot:
           return
       if ctx.message.content.startswith("=banned ") or ctx.message.content.startswith("=check "):
        await ctx.message.delete()
        edi = await ctx.message.channel.send(content = "Looking up <a:plswait:480058164453179428>")
        usar = await client.get_user_info(int(userid))
        res = await check(userid)
        clr = 0x42f49b # green
        mkay = "https://i.imgur.com/dgMFwTq.png"
        beaned = 0
        blacklisted = "No, this user is safe"
        if "1" in [s[0] for s in res]:
            clr = 0xfc6262
            beaned = 1
            blacklisted = "Yes, this user is global banned"
            mkay = "https://i.imgur.com/ExscAMH.png"
        eme = discord.Embed(color = clr, title = "Discord Bans Lookup")
        eme.set_author(name = usar.name + "#" + usar.discriminator, icon_url = mkay, url = "https://bans.discord.id")
        eme.set_footer(text = "Requested by " + ctx.message.author.name + "#" + ctx.message.author.discriminator)
        eme.timestamp = ctx.message.created_at
        eme.set_thumbnail(url = usar.avatar_url)
        eme.add_field(name = "User ID", value = userid, inline = True)
        eme.add_field(name = "User", value = usar.name + "#" + usar.discriminator, inline = True)
        if ".gif" in usar.avatar_url: # is_animated is not working well
            eme.add_field(name = "Avatar", value = "[Click](" + usar.avatar_url + ")", inline = True)
        else:
            eme.add_field(name = "Avatar", value = "[Click](" + usar.avatar_url_as(format = "png", size = 1024) + ")", inline = True)
        eme.add_field(name = "Blacklisted", value = blacklisted, inline = True)
        if beaned == 1:
            eme.add_field(name = "Cases", value = "\n".join(["ID: " + str(s[1]) + "\nReason: " + s[2] + "\nProof: [Click](" + s[3] + ")\n" for s in res] ) , inline = False)
        await ctx.send(embed = eme, content = "")

