#в этом файле все что берется из инета (кроме гпт) и глобал чат
import discord;
import requests
import random
import asyncio
import nest_asyncio
import re
import datetime

from discord.ext import commands;
from discord.utils import get
from discord.ext import tasks
from pprint import pprint
from asyncio import sleep
from bs4 import BeautifulSoup

import save_load #чтобы сохранять файлы
from token_and_bot import TOKEN,bot; #база дискорд пая
from gpt import on_mention; 
import reznya
from my_funcs import GetUserfromMention,toInt

#функция только для дсж
async def change():
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    dollar = (data['Valute']['USD']["Value"]) #спизженно в душе не ебу что за хуйня
    _name = "$" + str(dollar);  

    some_date = datetime.datetime(2022, 2, 24)
    now_date = datetime.datetime.now()
    svo = "гойда уже: " + str((now_date - some_date).days)


    guild = bot.get_guild(1055159007213539351)
    channel = bot.get_channel(1238235103214178367)
    channel_svo = bot.get_channel(1145799838596866120)
    

    await channel.edit(name = _name) 
    await channel_svo.edit(name = svo) 
    print("svo");
    await asyncio.sleep(3600)
    print ("working");
    await change();

#анекдоты
def Anekdoted(Number:int)->str:
    if (Number == 0):
        Link = "https://anekdot.me/wiki/" + str(random.randint(0, 6000))
    else:
         Link = "https://anekdot.me/wiki/" + str(Number)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
    #https://www.youtube.com/watch?v=4L57oY3J378&t=196s
    full_page = requests.get(Link, headers=headers)

    soup = BeautifulSoup(full_page.content, "html.parser")
    Result = soup.findAll("div",{"class": "anekdot-centred-text"})
    Result = str(Result[0].text)
    if Result == "":
        print("anekdot failet... retry")
        return Anekdoted(0);
    elif len(Result)>1900:
        print("anekdot too big... retry")
        return Anekdoted(0);
    elif Result == "доступен только зарегистрированным пользователям":
        print("anekdot too huinya")
        return Anekdoted(0);
    else:
        return Result;

@bot.command(name="anekdot", aliases=["Anekdot","анекдот","Анекдот"])
async def Anekdot(ctx):
    await ctx.reply("**Внимание, анекдот:**" + Anekdoted(0))

#глобальный чат
@commands.has_permissions(administrator = True)
@bot.command()
async def set_global_chat(ctx,arg):
    try:
        serv = ctx.message.guild.id;
    except:
        serv = -1;
    print("set_global_chat starting...")
    if (arg != -1):
        array = save_load.read("has_GB","GB",[])
        print(array)
        print(type(array))
        if not (array == None):
            if not (serv in array):
                array.append(serv)
                save_load.write("has_GB","GB",array) #записываю сервер в базу 1337 вместо конкретного сервера, ибо данные общие
        else:
            array = [];
            array.append(serv)
            save_load.write("has_GB","GB",array)
        
    channel = bot.get_channel(toInt(arg)).id
    print("serv:",serv)
    print("channel: ", channel)
    save_load.write("globalchat",serv,channel)
    a = save_load.read("globalchat",serv,-1)
    await ctx.reply(a)

async def Global_send(ctx,data):
    array = save_load.read("has_GB","GB",[])
    for i in array:
        if i!=ctx.guild.id:
            need_channel = save_load.read("globalchat",i,None) # достаем id канала из файла
            need_channel = bot.get_channel(need_channel)
            await need_channel.send(embed=data)
        else:
            await ctx.add_reaction("🚀")

async def gb_triger(ctx):
    if not (ctx.author.bot):
        print(ctx.content)
        picture = ""

        NEED_SEND = ctx.content
        embed = discord.Embed(description=NEED_SEND) #,color=Hex code
        embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar)
        for i in ctx.attachments:
            print(i);
            embed.set_image(url=i);
        embed.set_footer(text=ctx.guild.name)
        await Global_send(ctx,embed)

print("info.py work")