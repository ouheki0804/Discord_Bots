# Discord.py is smoooooooooooooosh!!!!!
import discord
from discord.ext import tasks, commands
import asyncio
import os # .env読み込みスターズ。
import json

def json_load(path):
    with open(path, "r") as f:
        return json.load(f)

class Server_Stats(commands.Cog):
    def __init__(self, airlinia):
        self.bot = airlinia #botを受け取る。
        self.datas = json_load("./data/pokemon.json")
        self.all_channel_id = 663297143909515274
        self.member_channel_id = 663297196531253249
        self.bot_channel_id = 663297233453842452
        self.online_channel_id = 663297268455309332
        self.idle_channel_id = 664160147886833678
        self.dnd_channel_id = 664160201125003295
        self.offline_channel_id = 663297305847398421
        self.message_channel_id = 663297421417119754
        self.time_channel_id = 663297453621116988

    @commands.Cog.listener()
    async def on_member_join(self, member):
        datas = self.datas
        server = member.guild
        datas["all"] = len(server.members)
        datas["member"] = len([member for member in server.members if not member.bot])
        datas["bot"] = len([member for member in server.members if member.bot])
        with open("./data/pokemon.json", "w") as file:
            json.dump(file, datas, indent=4)
        await channel_name_edit()

    @commands.Cog.listener()
    async def on_message(self, message):
        datas = self.datas
        server = message.guild
        if message.author.bot:  # ボットのメッセージをハネる
            return
        datas["message"] += 1
        with open("./data/pokemon.json", "w") as file:
            json.dump(file, datas, indent=4)
        await channel_name_edit()

    @commands.Cog.listener()
    async def on_member_updata(self, before, after):
        datas = self.datas
        server = after.guild
        datas["online"] = len([member for member in server.members if member.status.online])
        datas["idle"] = len([member for member in server.members if member.status.idle])
        datas["dnd"] = len([member for member in server.members if member.status.dnd])
        datas["offline"] = len([member for member in server.members if member.status.offline])
        with open("./data/pokemon.json", "w") as file:
            json.dump(file, datas, indent=4)
        await channel_name_edit()

    async def channel_name_edit():
        datas = self.datas
        all_channel : discord.VoiceChannel = self.bot.get_channel(self.all_channel_id)
        member_channel : discord.VoicetChannel = self.bot.get_channel(self.member_channel_id)
        bot_channel : discord.VoiceChannel = self.bot.get_channel(self.bot_channel_id)
        online_channel : discord.VoiceChannel = self.bot.get_channel(self.online_channel_id)
        idle_channel : discord.VoiceChannel = self.bot.get_channel(self.idle_channel_id)
        dnd_channel : discord.VoiceChannel = self.bot.get_channel(self.dnd_channel_id)
        offline_channel : discord.VoiceChannel = self.bot.get_channel(self.offline_channel_id)
        message_channel : discord.VoiceChannel = self.bot.get_channel(self.message_channel_id)
        time_channel : discord.VoiceChannel = self.bot.get_channel(self.time_channel_id)
        # await self.all_channel.edit(name=f"all : {datas["all"]}")
        # await self.member_channel.edit(name=f"member : {datas["member"]}")
        # await self.bot_channel.edit(name=f"bot : {datas["bot"]}")
        await online_channel.edit(name=f"online : {datas["online"]}")
        await idle_channel.edit(name=f"idle : {datas["idle"]}")
        await dnd_channel.edit(name=f"dnd : {datas["dnd"]}")
        await offline_channel.edit(name=f"offline : {datas["offline"]}")
        # await self.message_channel.edit(name=f"message : {datas["message"]}")
        # await self.time.all_channel.edit(name=f"time : {datas["time"]}")

def setup(airlinia):
    airlinia.add_cog(Server_Stats(airlinia))
