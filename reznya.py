import time
import datetime
import random
import save_load
from token_and_bot import TOKEN,bot;
from my_funcs import GetUserfromMention,toInt,minmax
from discord.ext import commands;
from bank import Wallet,Num;

NUM = Num()

class UserCd:
    def __init__(self,_id:int):
        self._id = _id
        self.cd_time = float(save_load.read(self._id,"kdtime", 0))
        print("UserCd ",self._id,"kdtime ",self.cd_time)
    def get_cd(self)->float:
        return (self.cd_time-time.time());
    def set_cd(self,value:float):
        self.cd_time = time.time() + value;
        save_load.write(self._id,"kdtime",self.cd_time)
    def is_cd(self)->bool:
        return (self.cd_time >= time.time());



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{round(error.retry_after, 2)} секунд осталось")
    else:
        print("!!!Ошибка:",error)

async def mute_member(ctx,member,duration:int)->str:
        member = GetUserfromMention(member).id
        victim = Wallet(member)
        thief = Wallet(ctx.author.id)
        duration = minmax(1,duration*pow(1.1,thief.get(NUM.dmg))/pow(1.1,victim.df),3600)
        print(member);
        m_member = ctx.guild.get_member(member)
        time = (datetime.timedelta(seconds=duration))
        await m_member.timeout(time, reason="резня")
        return m_member.mention;

def steal(ctx,member,summa:int)->str:
    member = GetUserfromMention(member).id
    m_member = ctx.guild.get_member(member)
    thief = Wallet(ctx.author.id);
    victim = Wallet(member);
    if m_member.is_timed_out():
        mes = "Но благородно ничего не украл"
    else:
        summa = round(summa*pow(1.1,thief.get(NUM.dmg))/pow(1.1,victim.df))
        if victim != thief:
            final_summa = thief.transfer(victim,summa)
            if final_summa > 0:
                mes = "И украл " + str(final_summa) + " 🧱";
            else:
                mes = "Но ничего не украл"
        else:
            mes = "";
    return mes;

@bot.command(name = "динамит",aliases=["д"])
async def boom(ctx,friend,*,reason = ""):
    U = UserCd(ctx.author.id);
    if U.is_cd():
        await ctx.send("кд еще " + str(U.get_cd()) + " сек")
    else:
        member = GetUserfromMention(friend).id
        thief = Wallet(ctx.author.id);
        victim = Wallet(member);
        GOIDA = Wallet(800598406149701634);
        if thief.check_balance() < 50:
            await ctx.reply("стоимость динамита 50 🧱")
        else:
            GOIDA.transfer(thief,50);
            if (random.randint(0,1) == 0) and (victim.check_bank()>2):
                summa =random.randint(1,round(victim.check_bank()*0.4));
                summa = round(summa*pow(1.1,thief.get(NUM.dmg))/pow(1.1,victim.get(NUM.df)))
                victim.banking(-summa);
                thief.transfer(victim,summa);
                await ctx.reply("вы украли из банка " + str(summa) + " 🧱")
            else:
                await ctx.reply("вам не повезло и динамит оторвал вам жопу")
            U.set_cd(60);


@bot.command(name = "хил",aliases=["х"])
async def heal(ctx,friend,*,reason = ""):
    try:
        U = UserCd(ctx.author.id);
        if U.is_cd():
            await ctx.send("кд еще " + str(U.get_cd()) + " сек")
        else:
            target = await mute_member(ctx,friend,1)
            if (reason != ""):
                mes = ctx.author.mention + " **вылечил** " + target + " по причине " + reason; 
            else:
                mes = ctx.author.mention + " **вылечил** " + target; 
            U.set_cd(5)
            await ctx.send(mes)
    except Exception as err:
        print(err)
        await ctx.send("либо нет прав нормальных, либо ты хуйню вместо аргументов указал какую-то")

@bot.command(name = "резня",aliases=["р"])
async def reznya(ctx,friend,*,reason = ""):
    try:            
        U = UserCd(ctx.author.id);
        if U.is_cd():
            await ctx.send("кд еще " + str(U.get_cd()) + " сек")
        else:
            if Wallet(GetUserfromMention(friend).id).is_armor():
                mes = "вы чувствуете себя умиротворенным"
            else:
                stealed = steal(ctx,friend,random.randint(1,15))
                target = await mute_member(ctx,friend,15)
                if (reason != ""):
                    mes = ctx.author.mention + " **зарезал** " + target + " по причине " + reason + '\n' + stealed; 
                else:
                    mes = ctx.author.mention + " **зарезал** " + target + '\n' + stealed; 
            U.set_cd(10)
            await ctx.send(mes)
    except Exception as err:
        print(err)
        await ctx.send("либо нет прав нормальных, либо ты хуйню вместо аргументов указал какую-то")

@bot.command(name = "пиу",aliases=["пистолет","п"])
async def shoot(ctx,friend,*,reason = ""):
    try:
        U = UserCd(ctx.author.id);
        if U.is_cd():
            await ctx.send("кд еще " + str(U.get_cd()) + " сек")
        else:
            if Wallet(GetUserfromMention(friend).id).is_armor():
                mes = "вы чувствуете себя умиротворенным"
            else:
                if random.randint(0,1) == 0:
                    stealed = steal(ctx,friend,random.randint(1,30))
                    target = await mute_member(ctx,friend,30)
                    if (reason != ""):
                        mes = ctx.author.mention + " **застрелил** " + target + " по причине " + reason + '\n' + stealed; 
                    else:
                        mes = ctx.author.mention + " **застрелил** " + target + '\n' + stealed; 
                else:
                    mes = "промахнулся, лох, кд 15 секунд"
            U.set_cd(15)
            await ctx.send(mes)
    except Exception as err:
        print(err)
        await ctx.send("либо нет прав нормальных, либо ты хуйню вместо аргументов указал какую-то")

@bot.command(name = "руская_рулетка",aliases=["рр"])
async def rr(ctx,friend,*,reason = ""):
    try:
        if Wallet(GetUserfromMention(friend).id).is_armor():
                mes = "вы чувствуете себя умиротворенным"
        else:
            if random.randint(0,1) == 0:
                stealed = steal(ctx,friend,random.randint(1,60))
                target = await mute_member(ctx,friend,60)
            else:
                target = await mute_member(ctx,ctx.author.id,60)
                stealed = "";
            if (reason != ""):
                mes = ctx.author.mention + " **застрелил** " + target + " по причине " + reason + '\n' + stealed; 
            else:
                mes = ctx.author.mention + " **застрелил** " + target + '\n' + stealed; 
            await ctx.send(mes)
    except Exception as err:
        print(err)
        await ctx.send("либо нет прав нормальных, либо ты хуйню вместо аргументов указал какую-то")

@bot.command(name = "атомная_бомба",aliases=["а","ядерная_бомба","воронеж","сво","ядерная","атомная"])
async def nuke(ctx,friend,*,reason = ""):
    try:
        U = UserCd(ctx.author.id);
        if U.is_cd():
            await ctx.send("кд еще " + str(U.get_cd()) + " сек")
        else:
            if Wallet(GetUserfromMention(friend).id).is_armor():
                mes = "вы чувствуете себя умиротворенным"
            else:
                target = await mute_member(ctx,friend,60*5)
                await mute_member(ctx,ctx.author.id,60*5)
                if (reason != ""):
                    mes = ctx.author.mention + " и " + target + " ликвидированы по причине " + reason; 
                else:
                    mes = ctx.author.mention + " и " + target + " посещают Воронеж"; 
            U.set_cd(60)
            await ctx.send(mes)
    except Exception as err:
        print(err)
        await ctx.send("либо нет прав нормальных, либо ты хуйню вместо аргументов указал какую-то")

@bot.command(name = "кд",aliases=["КД","кулдаун","cd","cooldown"])
async def check_cd(ctx):
    U = UserCd(ctx.author.id)
    await ctx.reply(str(U.get_cd()))
print("reznya.py work")
