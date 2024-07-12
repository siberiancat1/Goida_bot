import time
import datetime
import random
import save_load
from token_and_bot import TOKEN,bot;
from my_funcs import GetUserfromMention,toInt,minmax,UserCdParent
from discord.ext import commands;
from bank import Wallet,Num,VALUTE;

NUM = Num()

class UserCd(UserCdParent):
    name_for_file = "reznya_cd"
class UserCdNuke(UserCdParent):
    name_for_file = "nuke_cd"

class MuteCD(UserCdParent):
	name_for_file = f"muted_on_serv"





@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{round(error.retry_after, 2)} секунд осталось")
    else:
        print("!!!Ошибка:",error)

async def mute_member(ctx,member,duration:int)->str:
        member = GetUserfromMention(member).id
        if member != 800598406149701634:
            victim = Wallet(member)
            thief = Wallet(ctx.author.id)
            duration = minmax(1,duration*pow(1.1,thief.get(NUM.dmg))/pow(1.1,victim.df),3600)
            print(member);
            m_member = ctx.guild.get_member(member)
            time = (datetime.timedelta(seconds=duration))
            try:
                await m_member.timeout(time, reason="резня")
            except:
                M = MuteCD(member,ctx.guild.id)
                M.set_cd(round(duration))
            return m_member.mention;
        else:
            await mute_member(ctx,ctx.author.mention,duration)
            return "соси жопу"

def steal(ctx,member,summa:int)->str:
    member = GetUserfromMention(member).id
    m_member = ctx.guild.get_member(member)
    thief = Wallet(ctx.author.id);
    victim = Wallet(member);
    if m_member.is_timed_out():
        mes = "Но благородно ничего не украл"
    else:
        summa = round(summa*pow(1.1,thief.get(NUM.dmg))/pow(1.1,victim.get(NUM.df)))
        summa = minmax(0,summa,1000)
        if ctx.author.id != member:
            final_summa = thief.transfer(victim,summa)
            if final_summa > 0:
                mes = f"И украл {final_summa} 🧱"
            else:
                mes = "Но ничего не украл"
        else:
            mes = "шизофрения"
    return mes

@bot.command(name = "динамит",aliases=["д"])
async def boom(ctx,friend,*,reason = ""):
    U = UserCd(ctx.author.id)
    if U.is_cd():
        await ctx.send(f"кд еще {U.get_cd()} сек")
    else:
        member = GetUserfromMention(friend).id
        try:
            mention_for_friend = ctx.guild.get_member(member).mention
        except:
            await ctx.reply("походу его нет на этом сервере, так что соси жопу")
            return 0
        thief = Wallet(ctx.author.id);
        victim = Wallet(member);
        GOIDA = Wallet(800598406149701634);
        if thief.check_balance() < 50:
            await ctx.reply(f"стоимость динамита 50 {VALUTE}")
        else:
            GOIDA.transfer(thief,50);
            if (random.randint(0,1) == 0) and (victim.check_bank()>2):
                summa = random.randint(1,round(victim.check_bank()*0.4));
                summa = minmax(1,round(summa*pow(1.1,thief.get(NUM.dmg))/pow(1.1,victim.get(NUM.df))),victim.check_bank()*0.8)
                victim.banking(-summa)
                thief.transfer(victim,summa)
                await ctx.reply(f"вы украли из банка {mention_for_friend} {summa} {VALUTE}")
            else:
                await ctx.reply(f"вы хотели украсть у {mention_for_friend},но вам не повезло и динамит оторвал вам жопу")
            U.set_cd(60);


@bot.command(name = "хил",aliases=["х"])
async def heal(ctx,friend,*,reason = ""):
    try:
        U = UserCd(ctx.author.id);
        if U.is_cd():
            await ctx.send(f"кд еще {U.get_cd()} сек")
        else:
            target = await mute_member(ctx,friend,0)
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
            await ctx.send(f"кд еще {U.get_cd()} сек")
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
            await ctx.send(f"кд еще {U.get_cd()} сек")
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
        N = UserCdNuke(ctx.author.id)
        if U.is_cd() or N.is_cd():
            await ctx.send(f"кд еще {U.get_cd()} сек")
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
            N.set_cd(3600)
            await ctx.send(mes)
    except Exception as err:
        print(err)
        await ctx.send("либо нет прав нормальных, либо ты хуйню вместо аргументов указал какую-то")


print("reznya.py work")
