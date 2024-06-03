import random
import save_load
import datetime
import time
import discord;
from token_and_bot import TOKEN,bot; 
from bank import Wallet

class UserCdWordle:
    def __init__(self,_id:int,serv:int):
        self._id = _id
        self.serv = serv
        self.cd_time = float(save_load.read(self._id,f"{self.serv}wordle_kdtime", 0))
        print("UserCd ",self._id,f"{self.serv}wordle_kdtime",self.cd_time)
    def get_cd(self)->float:
        return (self.cd_time-time.time());
    def set_cd(self,value:float):
        self.cd_time = time.time() + value;
        save_load.write(self._id,f"{self.serv}wordle_kdtime",self.cd_time)
    def is_cd(self)->bool:
        return (self.cd_time >= time.time());


class wordle:
        def __init__(self, serv:int):
                self._id = serv
                self.today_word = str(save_load.read(serv,"wordle",None))
                self.today_word_guessed = save_load.read(serv,"wordle_guessed",0)
                self.last_date = datetime.datetime.fromtimestamp(int(save_load.read(serv,"wordle_date",0)))
                print(self.last_date)
                self.mes = str(save_load.read(serv,"wordle_str",""))
        def get_today_word(self): 
                dif = datetime.datetime.now() - self.last_date
                if dif > datetime.timedelta(days=1): 
                        self.last_date = datetime.datetime.now()
                        array = self.get_array() 
                        self.today_word =array[random.randint(0,len(array)-1)]
                        t = time.mktime(self.last_date.timetuple())
                        print(t)
                        save_load.write(self._id,"wordle_guessed", 0)
                        save_load.write(self._id,"wordle_date", t)
                        save_load.write(self._id,"wordle_str","")
                        save_load.write(self._id,"wordle",self.today_word)
                print(self.today_word)
                return self.today_word
        def get_array(self):
                file1 = open("wordly.txt", "r", encoding="utf-8")
                lines = file1.readlines()
                array = []
                # итерация по строкам
                for line in lines:
                        array.append(line);
                array = [line.rstrip() for line in array]
                return array
        def attemp(self,try_word):
                self.get_today_word()
                if self.today_word_guessed == 1:
                        return -1,"На этом сервере слово уже угадано"
                else:
                        full_guessed=[]
                        guessed=[]
                        try_word = try_word.upper()
                        print(try_word)
                        if len(try_word) == 5:
                                if try_word in self.get_array():
                                        if self.today_word != try_word:
                                                for i in range(0,5):
                                                        if self.today_word[i] == try_word[i]:
                                                                full_guessed.append(i);
                                                        if self.today_word.find(try_word[i])!=-1 and not(try_word[i] in guessed):
                                                                guessed.append(i);
                                                new = ""
                                                for i in range(0,5):
                                                        if i in full_guessed:
                                                                new+="**"+try_word[i]+"**";
                                                        elif i in guessed:
                                                                new+=try_word[i];
                                                        else:
                                                                new+="~~"+try_word[i]+"~~";
                                                self.mes +="\n" + new + "\n" + "угадано " + str(len(guessed)) + " из которых на своем месте " + str(len(full_guessed))
                                                save_load.write(self._id,"wordle_str",self.mes)
                                                print(self.mes)
                                                return 0,self.mes
                                        else:
                                                save_load.write(self._id,"wordle_guessed",1)
                                                return 1,self.mes
                                else:
                                        return -1,"не знаю такого слова, попробуй другое"
                        else:
                                return -1,"не знаю такого слова, попробуй другое"
                        

@bot.command(name = "wordle",aliases=["вордли","слово"])
async def try_wordle(ctx,word):
        game = wordle(0)
        U = UserCdWordle(ctx.author.id,ctx.guild.id)
        if U.is_cd():
               await ctx.reply("кд еще " + str(U.get_cd))
        else:
                check,mes = game.attemp(word)
                if check == -1:
                        await ctx.reply(mes)
                elif check == 0:
                        await ctx.reply(mes)
                        U.set_cd(3600)
                elif check == 1:
                        W = Wallet(ctx.author.id)
                        W.give(250)
                        await ctx.reply("Угадал, ты получил 250 🧱  и кружку пива")
               
print("wordle.py работает")

