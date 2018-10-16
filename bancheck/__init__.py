from .bancheck import BanList


def setup(bot):
    n = BanList(bot)
    bot.add_cog(n)
