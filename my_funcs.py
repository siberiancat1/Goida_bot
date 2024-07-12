from token_and_bot import TOKEN,bot;
import re
import datetime
import discord
import save_load
import time
from discord.utils import get

class UserCdParent:
    name_for_file = "ENTER A NAME"
    def __init__(self,_id,_dopinfo = ""):
        self._id = _id
        self._dopinfo = _dopinfo
        self.cd_time = float(save_load.read(self._id,f"{self.__class__.name_for_file}{self._dopinfo}", 0))
        print("UserCd ",self._id,f"{self.__class__.name_for_file}{self._dopinfo}",self.cd_time)
    def get_cd(self)->float:
        return round(self.cd_time-time.time())
    def set_cd(self,value:float):
        self.cd_time = time.time() + value
        save_load.write(self._id,f"{self.__class__.name_for_file}{self._dopinfo}",self.cd_time)
    def is_cd(self)->bool:
        return (self.cd_time >= time.time())

def minmax(minimal,value,maximum):
    return min(maximum,max(minimal,value))

def log(new_line):
    with open("log.txt", 'a') as file:
        file.write(new_line + '\n')


def Decorated(Reznya = False,Bank = False):
    def decorator(func):
        async def wrapper(ctx, *args, **kwargs):
            st = time.time()
            await func(ctx, *args, **kwargs)
            et = time.time()
            all_time = et - st
            str ="["+str({datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")})+f"] {func.__name__}{args} for {all_time} sec, author {ctx.author.name}"
            log(str)
            wrapper.__name__ = func.__name__
        return wrapper
    return decorator
        


def GetUserfromMention(friend):
    try:
        a = int(friend)
        print("1",a)
    except:
        try:
            a = friend[2::]
            a = a[::1]
            a = Int(a)
            print("2",a)
        except:
            a = toInt(friend);
            print("3",a)
    a = bot.get_user(a);
    print("final",a)
    return a;
    
def toInt(arg)->int:
    try:
        arg1 = "a" + str(arg) 
        number = int(re.search(r'\d+', arg1).group())
        return number;
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!"+'\n' + "ERROR IN toInt")
        print("returned None")
        return 0;


async def Remove_Role(ctx,role_id):
    user = ctx.guild.get_member(ctx.author.id)
    try:
        role = get(user.guild.roles, id = role_id) 
    except Exception as err:
        raise err
        print("role issue")
        return 0;
    try:
        await user.remove_roles(role)
        return 1;
    except Exception as err:
        raise err
        print("per. issue",err)
    return 0;

async def Give_Role(ctx,role_id):
    user = ctx.guild.get_member(ctx.author.id)
    try:
        role = get(user.guild.roles, id = role_id) 
        print(role)
    except Exception as err:
        raise err
        print("role issue")
        return 0;
    try:
        await user.add_roles(role)
        return 1;
    except Exception as err:
        raise err
        print("per. issue",err)
    return 0
def BeaTime(sec):
    dif = datetime.timedelta(seconds=sec)

    # Преобразование timedelta в часы, минуты и секунды
    hours = dif.seconds // 3600
    minutes = (dif.seconds % 3600) // 60
    seconds = dif.seconds % 60

    # Форматирование времени в нужном формате
    formatted_time = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    return formatted_time
print("my_funcs work")