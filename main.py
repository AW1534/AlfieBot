import asyncio
import random

import os
import time

from dotenv import load_dotenv
load_dotenv()

import requests

import discord
from discord.ext import commands

import config

bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.prefix), case_insensitive=True)

@bot.event
async def on_ready():
    print('Logged in.')
    print("\n")
    print("Setting status...")
    status = random.choice(config.status)
    await bot.change_presence(activity=discord.Game(f"{config.prefix} " + status))
    print(f"""Status set to "{status}".""")
    print('------')



@bot.command()
async def inspire(ctx):
    descriptions = [
        "Here, have some food for thought.", "Send help", "Be inspired", "Go commit :arrow_down:",
        "Inspiring people is my passion", "Am I doing it right?", "Here you go."
    ]
    try:
        url = 'http://inspirobot.me/api?generate=true'
        params = {'generate': 'true'}
        response =requests.get(url, params, timeout=10)

        image = response.text
        embed = discord.Embed(title=descriptions[random.randint(0, len(descriptions) - 1)], color=config.infoColor)
        embed.set_image(url=image)
        embed.set_footer(text="Generated using https://inspirobot.me")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="Inspirobot is broken, we have no reason to live.", color=config.errorColor)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@bot.command()
async def sudo(ctx, username, *, text):
    await ctx.message.delete()
    webhook = await ctx.message.channel.create_webhook(name=username)
    await webhook.send(text)
    await webhook.delete()

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member=None, *, reason="No reason provided"):
    if ctx.author.top_role < member.top_role:
        embed = discord.Embed(title="Error", color=config.errorColor)
        embed.add_field(name="NErd", value="You cannot kick someone with a higher role than you.")
        embed.set_footer(text="Use `{}help mod` for more info.".format(config.prefix))
        await ctx.send(embed=embed)
        return
    elif member.id == bot.user.id:
        embed = discord.Embed(title="Error", color=config.errorColor)
        embed.add_field(name="Error", value="I cannot kick myself.")
        embed.set_footer(text="Use `{}help mod` for more info.".format(config.prefix))
        await ctx.send(embed=embed)
        try:
            _ = await bot.wait_for('message', timeout=5)
        except asyncio.exceptions.TimeoutError:
            await ctx.send("I can't believe you would try that tbh.")
        return

    if discord.member == None:
        embed = discord.Embed(title="Error", color=config.errorColor)
        embed.add_field(name="Error", value="Sure. let me go and kick this ghost. genius right here.")
        embed.set_footer(text="Use `{}help mod` for more info.".format(config.prefix))
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(title=f"You have been kicked from {ctx.message.guild.name}", color=config.errorColor)
    embed.add_field(name="Reason", value=reason)
    embed.set_author(name=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
    await member.send(embed=embed)
    if ctx.channel.id != config.testChannel:
        await ctx.send(f"This is not in the test channel. in future, this will seriously be a kick.")
        # await member.kick(reason=reason)
    await ctx.send(f"banned {member.mention}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None, *, reason="No reason provided"):
    if ctx.author.top_role < member.top_role:
        embed = discord.Embed(title="Error", color=config.errorColor)
        embed.add_field(name="NErd", value="You cannot ban someone with a higher role than you.")
        embed.set_footer(text="Use `{}help mod` for more info.".format(config.prefix))
        await ctx.send(embed=embed)
        return
    elif member.id == bot.user.id:
        embed = discord.Embed(title="Error", color=config.errorColor)
        embed.add_field(name="Error", value="I cannot ban myself.")
        embed.set_footer(text="Use `{}help mod` for more info.".format(config.prefix))
        await ctx.send(embed=embed)
        try:
            _ = await bot.wait_for('message', timeout=5)
        except asyncio.exceptions.TimeoutError:
            await ctx.send("I can't believe you would try that tbh.")
        return

    if discord.member == None:
        embed = discord.Embed(title="Error", color=config.errorColor)
        embed.add_field(name="Error", value="Sure. let me go and ban this ghost. genius right here.")
        embed.set_footer(text="Use `{}help mod` for more info.".format(config.prefix))
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(title=f"You have been banned from {ctx.message.guild.name}", color=config.errorColor)
    embed.add_field(name="Reason", value=reason)
    embed.set_author(name=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
    await member.send(embed=embed)
    if ctx.channel.id != config.testChannel:
        await ctx.send(f"This is not in the test channel. in future, this will seriously be a ban.")
        # await member.ban(reason=reason)
    await ctx.send(f"banned {member.mention}")

@bot.command(aliases=["purge", "delete"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    if amount > 100:
        embed = discord.Embed(title="Error", color=config.errorColor)
        embed.add_field(name="Error", value="You can only clear up to 100 messages at a time.")
        embed.set_footer(text="Use `{}help mod` for more info.".format(config.prefix))
        await ctx.send(embed=embed)
    elif amount < 1:
        embed = discord.Embed(title="Error", color=config.errorColor)
        embed.add_field(name="Error", value="You cannot clear less than 1 message.")
        embed.set_footer(text="Use `{}help mod` for more info.".format(config.prefix))
        await ctx.send(embed=embed)
    else:
        await ctx.channel.purge(limit=amount)
        msg = await ctx.send("Cleared {} messages.".format(amount))
        await msg.delete(delay=5)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Info", color=config.infoColor)
    embed.add_field(name="Version", value=config.version)
    embed.add_field(name="Author", value="<@{}>".format(config.authorID))
    embed.add_field(name="GitHub", value="https://github.com/AW1534/AlfieBot")
    embed.add_field(name="Note", value=f"Discord bot made custom by <@{config.authorID}> for <@{config.ownerID}>. If you would like your own bot, have spotted a bug, or have any quetions please contact the author.")
    await ctx.send(embed=embed)

bot.remove_command("help")
@bot.command()
async def help(ctx, page="1", _page="1"):
    prefix = config.prefix
    if (page == "mod"):
        page = int(_page)
        def p1():
            embed = discord.Embed(title="__(1) Moderation Commands__", color=config.infoColor)
            embed.add_field(name="Kick", value="`{}kick @user [reason]`".format(config.prefix))
            embed.add_field(name="Ban", value="`{}ban @user [reason]`".format(config.prefix))
            embed.add_field(name="Clear", value="`{}clear [amount]`".format(config.prefix))
            embed.set_footer(text="Use `{}help mod` for more info.".format(config.prefix))
            return embed

        pages = [p1]

        try:
            embed = pages[page - 1]()
            embed.set_footer(text=f"use {prefix}help <1-{len(pages)}>")
            await ctx.send(embed=embed)
        except IndexError:
            embed = pages[0]()
            embed.set_footer(text=f"There was an error; Here is the first page.")
            await ctx.send(embed=embed)
    else:
        page = int(page)
        def p1():
            embed = discord.Embed(title="__(1) Essential commands__", color=config.infoColor)
            embed.add_field(name=f"{prefix}help", value=f"sends this!\n**usage**: `{prefix}help <1-{len(pages)}>`")
            return embed

        def p2():
            embed = discord.Embed(title="__(2) Fun commands__", color=config.infoColor)
            embed.add_field(name=f"{prefix}inspire", value='Generates an "inspirational" image.')
            embed.add_field(name=f"{prefix}sudo", value=f"Sends a message as another user.\n**usage**: `{prefix}sudo <username> <message>`")
            return embed


        pages = [p1, p2]

        try:
            embed = pages[page-1]()
            embed.set_footer(text=f"use {prefix}help <1-{len(pages)}>")
            await ctx.send(embed=embed)
        except IndexError:
            embed = pages[0]()
            embed.set_footer(text=f"There was an error; Here is the first page.")
            await ctx.send(embed=embed)

print("Logging in...")
bot.run(os.environ['DC_TOKEN'])