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

class BanList(BaseCog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 54564894107)
        self.config.register_guild(**{"ENABLED":True})
        self.users = {}
        self.messages = {}; print('NOTICE: LOADED BANCHECK')

    @checks.admin_or_permissions(manager_server=True)
    @commands.group(pass_context=True)
    async def bancheck(self, ctx):
        """Check if users are banned on bans.discordlist.com"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @checks.admin_or_permissions(manager_server=True)
    @bancheck.command(pass_context=True)
    async def channel(self, ctx, channel:discord.TextChannel=None):
        """Set the channel you want members to welcomed in"""
        if channel is None:
            channel = ctx.message.channel
        await self.config.guild(ctx.guild).channel.set(channel.id)
        try:
                infomessage = "Channel has been set to {}".format(channel.mention)
                e = discord.Embed(title="Channel Successfully Set!", colour=discord.Colour.green())
                e.description = "Successfully changed bancheck channel."
                e.add_field(name="Information:", value=infomessage, inline=False)
                e.set_footer(text="Channel ID: {}".format(channel.id))
                e.set_thumbnail(url="http://i.coltoutram.nl/green-tick.png")
                return await ctx.send(embed=e)
                                  
        except discord.errors.Forbidden:
            await ctx.send(channel, 
                ":no_entry: **I'm not allowed to send embed links here.**")

    @checks.admin_or_permissions(manager_server=True)
    @bancheck.command(pass_context=True)
    async def toggle(self, ctx):
        """Toggle banchecks on new users on/off."""
        guild = ctx.message.guild
        if self.config.guild(guild).GUILD is None:
            return
        else:
            if await self.config.guild(guild).ENABLED():
                await self.config.guild(guild).ENABLED.set(False)
                await ctx.send("Bancheck is now enabled.")
            else:
                await self.config.guild(guild).ENABLED.set(True)
                await ctx.send("Bancheck is now disabled.")

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
async def _channel(self, ctx):
   if msg.author.bot:
       return
   if msg.content.startswith("=banned ") or msg.content.startswith("=check "):
        await msg.delete()
        edi = await msg.channel.send(content = "Looking up <a:plswait:480058164453179428>")
        userid = ""
        if msg.content.startswith("=banned "):
            userid = str(int(msg.content.replace("=banned ", "")))
        elif msg.content.startswith("=check "):
            userid = str(int(msg.content.replace("=check ", "")))
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
        eme.set_footer(text = "Requested by " + msg.author.name + "#" + msg.author.discriminator)
        eme.timestamp = msg.created_at
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
        await edi.edit(embed = eme, content = "")
client.run("potato")
