import discord

from discord.ext import commands
@commands.command()
async def avatar(ctx,Member:discord.Member=None):
     if Member == None:
         Member = ctx.author
     embed = discord.Embed(
         title="Ok!"
     )
     embed.set_author(name=f"Avatar de {Member.display_name}!")
     embed.set_image(url=Member.avatar_url)
     await ctx.send(embed=embed)
def  setup(bot):
    bot.add_command(avatar)