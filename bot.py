import discord;
import requests
import asyncio
import nest_asyncio
import re
import datetime
import random

from discord.ext import commands;
from discord.utils import get
from discord.ext import tasks
from pprint import pprint
from asyncio import sleep
from bs4 import BeautifulSoup

#не библиотеки а мои файлы :) 
import save_load #чтобы сохранять файлы
from token_and_bot import TOKEN,bot; #база дискорд пая
from gpt import on_mention; 
import reznya
from my_funcs import GetUserfromMention,toInt
from info import change,gb_triger
import bank
import wordle

nest_asyncio.apply() # в душе не ебу что за хуйня можно попробовать снести

#база
#dkkd
print ("bot starting...")


@bot.event
async def on_message(ctx):
    if not ctx.author.bot:
        #тригер на упоминания
        if ((ctx.content).find("<@800598406149701634>")!= -1):
            await on_mention(ctx)

        #тригер глобального чата 
        try:
            serv = ctx.guild.id;
        except:
            serv = -1;
        need_channel = save_load.read("globalchat",serv,None)
        if (need_channel != None):
            need_channel = bot.get_channel(need_channel)
            if (ctx.channel.id == need_channel.id):
                await gb_triger(ctx);
        if random.randint(0,50) == 0:
            await bank.mes_reward(ctx);
    await bot.process_commands(ctx)

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle, activity = discord.Activity(name = "пригласи меня к себе пжлст <3", type = discord.ActivityType.playing)) 
    print("Bot Is Ready And Online!")
    await change()

@bot.command()
async def hello(ctx):
    await ctx.reply("hello ебать")
@bot.command(name = "пиво")
async def pivo(ctx):
    await ctx.reply("пиво ебать")


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Гойда бот") #,color=Hex code
    embed.add_field(name="?gpt (запрос)", value="можно просто пингануть бота вместо написания команды" + '\n' + "GPT 3.5 TURBO пишет херню исходя из вашего запроса, на данный момент количество запросов ограниченно самим сайтом", inline=False);
    embed.add_field(name="?reset", value="стирает прошлые запросы", inline=False);
    embed.add_field(name="?Tgpt (запрос)", value="тоже самое что и ?gpt только без памяти и контекста, используйте если нужно чтобы бот ответил серьезно",inline=False);
    embed.add_field(name="?Anekdot", value="рассказывает случайный анекдот, самая полезная функция бота",inline=False);
    embed.add_field(name="?help", value="не поверишь",inline=False);
    embed.add_field(name="?set_global_chat (канал)", value="Включает глобальный чат в этом канале",inline=False);
    embed.add_field(name="?резня (@кто-нибудь) []", value="выдает мут на 15 сек, кд 5 сек",inline=False);
    embed.add_field(name="?пистолет (@кто-нибудь) []", value="выдает мут на 30 сек с 50% шансом, кд 15 сек",inline=False);
    embed.add_field(name="?рр (@кто-нибудь) []", value="выдает мут на 60 сек с 50% шансом, может выдать мут вам",inline=False);
    embed.add_field(name="?динамит (@кто-нибудь)", value="позволяет взорвать банк  ||и (взять до 40% оттуда)|| или себе жопу",inline=False);
    embed.add_field(name="?атомная_бомба (@кто-нибудь) []", value="выдает мут на 5 минут",inline=False);
    embed.add_field(name="?хил (@кто-нибудь) []", value="снимает мут",inline=False);
    embed.add_field(name="?баланс [@кто-нибудь]", value="выводит баланс",inline=False);
    embed.add_field(name="?банк (сумма)", value="позволяет положить или снять деньги из банка",inline=False);
    embed.add_field(name="?перевод (@кто-нибудь) [сумма] []", value="позволяет перевести деньги",inline=False);
    embed.add_field(name="?купить [название] [кол-во]", value="позволяет купить что-нибудь или посмотреть список товаров",inline=False);
    embed.add_field(name="?награда", value="получить награду, работает раз в 8 часов",inline=False);
    embed.add_field(name="?wordle (слово)", value="просто вордли, за правильно введенное слово вы получите 300 кирпичей, слово уникально на каждом сервере и обновляется раз в день",inline=False);


    await ctx.reply(embed=embed)

bot.run(TOKEN)
