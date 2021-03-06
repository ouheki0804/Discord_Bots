import discord
from discord.ext import commands
import asyncio
import os
import re
import traceback
import json

class RolePanel(commands.Cog):  # 役職パネルの機能
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel: discord.TextChannel = self.bot.get_channel(616530487229546518)
        async for message in self.bot.get_channel(616530487229546518).history().filter(lambda m: m.author == self.bot.user):
            for reaction in message.reactions:
                async for user in reaction.users().filter(lambda u: u != self.bot.user):
                    self.bot.loop.create_task(message.remove_reaction(reaction, user))
            self.bot._connection._messages.append(message)

    @commands.group(aliases=["rp"])
    async def rolepanel(self, ctx):
        return

    @rolepanel.command(aliases=["rpaa", "alphaadd", "aa"])
    @commands.has_guild_permissions(administrator=True)
    async def _rolepanel_alpha_add(self, ctx, emoji, role: discord.Role, tag='通常'):
        await self._rolepanel_add(emoji, role, version='α', tag=tag)

    @rolepanel.command(aliases=["rpba", "betaadd", "ba"])
    @commands.has_guild_permissions(administrator=True)
    async def _rolepanel_beta_add(self, ctx, emoji, role: discord.Role, tag='通常'):
        await self._rolepanel_add(emoji, role, version='β', tag=tag)

    async def _rolepanel_add(self, emoji, role, version='α', tag='通常'):
        def check(m):
            return (
                m.author == self.bot.user and m.embeds
                and tag in m.embeds[0].title
            )
        break1 = False
        history = await self.bot.get_channel(616530487229546518).history(oldest_first=True, limit=None)\
            .filter(check).flatten()
        for m in history:
            embed = m.embeds[0]
            description = embed.description
            lines = description.splitlines()
            for i in range(20):
                if emoji not in description:
                    new_lines = '\n'.join(
                        lines[0:i]
                        + ['{0}:{1}'.format(emoji, role.mention)]
                        + lines[i:len(lines) + 1]
                    )
                    embed.description = new_lines
                    embed.color = 0xfefefe
                    await m.edit(embed=embed)
                    await m.add_reaction(emoji)
                    break1 = True
                    break
            if break1:
                break
        else:
            embed = discord.Embed(
                title='役職パネル{0}({1})({2}ページ目)'.format(version, tag, len(history) + 1),
                description='{1}:{0}'.format(role.mention, emoji),
                color=0xfefefe
            )
            embed.set_footer(text='役職パネル', icon_url='https://cdn.discordapp.com/attachments/658699920039215114/670817582034714635/b16b12b993469c42.gif')
            m = await self.bot.get_channel(616530487229546518).send(embed=embed)
            await m.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        if user == self.bot.user: #自分のをハネる
            return
        if message.channel.id == 616530487229546518 and message.author == self.bot.user: #役職申請チャンネル且つメッセージがBot
            if '役職パネルα' in message.embeds[0].title:
                await message.remove_reaction(reaction, user) #取り消す
                try:
                    match2 = re.search(reaction.emoji + r':<@&(\d*)>', message.embeds[0].description) #取り出す
                except TypeError:
                    emoji_text = f"<:{reaction.emoji.name}:{reaction.emoji.id}>"
                    match2 = re.search(emoji_text + r':<@&(\d*)>', message.embeds[0].description)
                if match2:
                    role = message.guild.get_role(int(match2.group(1)))
                    if role not in user.roles:
                        await user.add_roles(role)
                        description = '{0}の役職を付与しました。'.format(role.mention)
                        embed = discord.Embed(description=description, color=0x0080ff)
                        embed.set_footer(text='役職パネル', icon_url='https://cdn.discordapp.com/attachments/658699920039215114/670817582034714635/b16b12b993469c42.gif')
                        await message.channel.send(
                            user.mention,
                            embed=embed,
                            delete_after=10
                        )
                    else:
                        await user.remove_roles(role)
                        description = '{0}の役職を解除しました。'.format(role.mention)
                        embed = discord.Embed(description=description, color=0xffff00)
                        embed.set_footer(text='役職パネル', icon_url='https://cdn.discordapp.com/attachments/658699920039215114/670817582034714635/b16b12b993469c42.gif')
                        await message.channel.send(
                            user.mention,
                            embed=embed,
                            delete_after=10
                        )
# --------------------------------------------------------------------------------------------------------
            elif '役職パネルβ' in message.embeds[0].title:
                try:
                    match2 = re.search(reaction.emoji + r':<@&(\d*)>', message.embeds[0].description) #取り出す
                except TypeError:
                    emoji_text = f"<:{reaction.emoji.name}:{reaction.emoji.id}>"
                    match2 = re.search(emoji_text + r':<@&(\d*)>', message.embeds[0].description)
                if match2:
                    role = message.guild.get_role(int(match2.group(1))) # Roleを取得
                    if role not in user.roles:
                        await user.add_roles(role)
                        description = '{0}の役職を付与しました。'.format(role.mention)
                        embed = discord.Embed(description=description, color=0x0080ff)
                        embed.set_footer(text='役職パネル', icon_url='https://cdn.discordapp.com/attachments/658699920039215114/670817582034714635/b16b12b993469c42.gif')
                        await message.channel.send(
                            user.mention,
                            embed=embed,
                            delete_after=10
                        )

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user == self.bot.user: #自分のをハネる
            return
        message = reaction.message
        if message.channel.id == 616530487229546518 and message.author == self.bot.user: #役職申請チャンネル且つメッセージがBot
            await message.remove_reaction(reaction, user) #取り消す
            if '役職パネルβ' in message.embeds[0].title:
                try:
                    match2 = re.search(reaction.emoji + r':<@&(\d*)>', message.embeds[0].description) #取り出す
                except TypeError:
                    emoji_text = f"<:{reaction.emoji.name}:{reaction.emoji.id}>"
                    match2 = re.search(emoji_text + r':<@&(\d*)>', message.embeds[0].description)
                if match2:
                    role = message.guild.get_role(int(match2.group(1))) # Roleを取得
                    if role in user.roles:
                        await user.remove_roles(role)
                        description = '{0}の役職を解除しました。'.format(role.mention)
                        embed = discord.Embed(description=description, color=0xffff00)
                        embed.set_footer(text='役職パネル', icon_url='https://cdn.discordapp.com/attachments/658699920039215114/670817582034714635/b16b12b993469c42.gif')
                        await message.channel.send(
                            user.mention,
                            embed=embed,
                            delete_after=10
                        )

    @commands.command()
    async def rolepanel_remove(self, ctx, role: discord.Role, tag=None):
        break1 = False
        async for m in self.bot.get_channel(616530487229546518).history(oldest_first=True, limit=None)\
                .filter(lambda m: m.author == self.bot.user and m.embeds):
            embed = m.embeds[0]
            description = embed.description
            if tag is not None and tag not in embed.title:
                continue
            lines = description.splitlines(keepends=True)
            for line in lines[:]:
                if role.mention in line:
                    embed.description = description.replace(line, '')
                    await m.edit(embed=embed)
                    await m.remove_reaction(line[0], self.bot.user)
                    break1 = True
                    break
            m = await self.bot.get_channel(616530487229546518).fetch_message(m.id)
            if not m.reactions:
                await m.delete()
            if break1:
                break

def setup(airlinia):
    airlinia.add_cog(RolePanel(airlinia))
