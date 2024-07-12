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
from reznya import MuteCD
from my_funcs import GetUserfromMention,toInt,Decorated
from info import change,gb_triger
import bank
import wordle
import my_funcs

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
        M = MuteCD(ctx.author.id,ctx.guild.id)
        if M.is_cd():
            await ctx.delete()
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


@bot.command(name="hello") 
@Decorated()
async def hello(ctx):
    await ctx.reply("hello ебать")

@bot.command(name = "пиво")
async def pivo(ctx):
    class Button(discord.ui.View):
        @discord.ui.button(label = "выпить пиво",style=discord.ButtonStyle.primary, emoji="😎")
        async def button_callback(self,inter,button):
            UM = inter.user.id
            if UM == ctx.author.id:
                print("кнопка нажата",inter.response)
                print("self",self)
                print(UM)
                
                button.disabled = True
                button.label = "пиво выпито("
                await inter.response.edit_message(content="вы успешно выпили пиво", view=self)
                #await inter.response.send_message("гооооол")
            else:
                pass
    await ctx.send('пиво ебать', view = Button())

@bot.command(name = "кд",aliases=["КД","кулдаун","cd","cooldown"])
async def check_cd(ctx):
    rezCD = reznya.UserCd(ctx.author.id).get_cd()
    NukeCD = reznya.UserCdNuke(ctx.author.id).get_cd()
    rewardCD = bank.UserCdDaily(ctx.author.id).get_cd()
    wordleCD = wordle.UserCdWordle(ctx.author.id,ctx.guild.id).get_cd()
    mes=f"Кд для {ctx.author.mention}:\n"
    mes += f"кд на резню: {max(0,round(rezCD))} сек\n"
    mes += f"кд на ядерку: {max(0,round(NukeCD))} сек\n"
    if rewardCD>0:
        mes += f"кд на награду: {my_funcs.BeaTime(rewardCD)} сек\n"
    else:
        mes += f"кд на награду: 0 сек\n"
    mes += f"кд на слова: {max(0,round(wordleCD))} сек\n"
    await ctx.send(mes)

@bot.command(name = "help",aliases=["помощь","хелп","помоги","??"])
async def help(ctx):
    embed_admin = discord.Embed(title="Гойда бот",description="🔧админские команды")
    embed_reznya = discord.Embed(title="Гойда бот",description="🔪РЕЗНЯ") #,color=Hex code
    embed_bank = discord.Embed(title="Гойда бот",description="💸экономические команды")
    embed_fun = discord.Embed(title="Гойда бот",description="🎲рофло команды")

    #embed.add_field(name="?gpt (запрос)", value="можно просто пингануть бота вместо написания команды" + '\n' + "GPT 3.5 TURBO пишет херню исходя из вашего запроса, на данный момент количество запросов ограниченно самим сайтом", inline=False);
    #embed.add_field(name="?reset", value="стирает прошлые запросы", inline=False);
    #embed.add_field(name="?Tgpt (запрос)", value="тоже самое что и ?gpt только без памяти и контекста, используйте если нужно чтобы бот ответил серьезно",inline=False);
    
    #фановое
    embed_fun.add_field(name="?Anekdot", value="рассказывает случайный анекдот, самая полезная функция бота",inline=False);
    embed_fun.add_field(name="?награда", value="получить награду, работает раз в 8 часов",inline=False);
    embed_fun.add_field(name="?wordle (слово)", value="просто вордли, за правильно введенное слово вы получите 300 кирпичей, слово уникально на каждом сервере и обновляется раз в день",inline=False);
    embed_fun.add_field(name="?очко (команда) [число]", value="русская карточная игра, напишите ?очко, чтобы узнать больше",inline=False);
    embed_fun.add_field(name="?клик", value="кликай на кирпич, буквально",inline=False);

    #админское
    embed_admin.add_field(name="?help", value="не поверишь",inline=False);
    embed_admin.add_field(name="?set_global_chat (канал)", value="включает глобальный чат в этом канале",inline=False);
    embed_admin.add_field(name="?добавить_роль (IDроли) (Цена) [имя_в_одно_слово] [описание]", value="добавить роль в магазин",inline=False);
    embed_admin.add_field(name="?удалить_роль (название)", value="удалить роль из магазина",inline=False);
    #резня
    embed_reznya.add_field(name="?резня (@кто-нибудь) []", value="выдает мут на 15 сек, кд 5 сек",inline=False);
    embed_reznya.add_field(name="?пистолет (@кто-нибудь) []", value="выдает мут на 30 сек с 50% шансом, кд 15 сек",inline=False);
    embed_reznya.add_field(name="?рр (@кто-нибудь) []", value="выдает мут на 60 сек с 50% шансом, может выдать мут вам",inline=False);
    embed_reznya.add_field(name="?динамит (@кто-нибудь)", value="позволяет взорвать банк  ||и (взять до 40% оттуда)|| или себе жопу",inline=False);
    embed_reznya.add_field(name="?атомная_бомба (@кто-нибудь) []", value="выдает мут на 5 минут",inline=False);
    embed_reznya.add_field(name="?хил (@кто-нибудь) []", value="снимает мут",inline=False);
    #банковское
    embed_bank.add_field(name="?баланс [@кто-нибудь]", value="выводит баланс",inline=False);
    embed_bank.add_field(name="?банк (сумма)", value="позволяет положить или снять деньги из банка",inline=False);
    embed_bank.add_field(name="?перевод (@кто-нибудь) [сумма] []", value="позволяет перевести деньги",inline=False);
    embed_bank.add_field(name="?купить [название] [кол-во]", value="позволяет купить что-нибудь или посмотреть список товаров",inline=False);
    
    embed = embed_fun
    class View(discord.ui.View):
        @discord.ui.button(label = "админ",style=discord.ButtonStyle.primary, emoji="🔧")
        async def button_admin(self,inter,button):
            UM = inter.user.id
            if UM == ctx.author.id:
                embed = embed_admin
                await inter.response.edit_message(embed=embed, view=self)
        @discord.ui.button(label = "резня",style=discord.ButtonStyle.primary, emoji="🔪")
        async def button_reznya(self,inter,button):
            UM = inter.user.id
            if UM == ctx.author.id:
                embed = embed_reznya
                await inter.response.edit_message(embed=embed, view=self)
        @discord.ui.button(label = "экономика",style=discord.ButtonStyle.primary, emoji="💸")
        async def button_bank(self,inter,button):
            UM = inter.user.id
            if UM == ctx.author.id:
                embed = embed_bank
                await inter.response.edit_message(embed=embed, view=self)
        @discord.ui.button(label = "fun",style=discord.ButtonStyle.primary, emoji="🎲")
        async def button_fun(self,inter,button):
            UM = inter.user.id
            if UM == ctx.author.id:
                embed = embed_fun
                await inter.response.edit_message(embed=embed, view=self)

    await ctx.reply(embed=embed,view = View())

bot.run(TOKEN)
