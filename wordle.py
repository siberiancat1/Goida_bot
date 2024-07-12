import random
import save_load
import datetime
import time
from token_and_bot import TOKEN,bot; 
from my_funcs import BeaTime,UserCdParent
from bank import Wallet,NUM,VALUTE
import discord

class UserCdWordle(UserCdParent):
	name_for_file = f"wordle_kdtime"




class wordle:
		def __init__(self, serv:int):
				self._id = serv
				self.today_word = str(save_load.read(serv,"wordle",None))
				self.today_word_guessed = save_load.read(serv,"wordle_guessed",0)
				self.last_date = datetime.datetime.fromtimestamp(int(save_load.read(serv,"wordle_date",0)))
				self.last_user  = (int(save_load.read(serv,"wordle_last_user",0)))
				self.mes = str(save_load.read(serv,"wordle_str","**WORDLE**" + '\n'))
				self.today_word = self.get_today_word()
		def get_mes(self):
				dif = datetime.timedelta(days=1) - (datetime.datetime.now() - self.last_date)
				hours = dif.seconds // 3600
				minutes = (dif.seconds % 3600) // 60
				seconds = dif.seconds % 60
				# Форматирование времени в нужном формате
				formatted_time = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
				mes = f"*{self.mes} \ncледующее слово уже через {formatted_time}*"
				return mes
		def set_last_user(self,user:int):
				self.last_user = user
				save_load.write(self._id,"wordle_last_user",self.last_user)
		def get_last_user(self):
				self.last_user  = (int(save_load.read(self._id,"wordle_last_user",0)))
				return self.last_user
		def get_today_word(self): 
				dif = datetime.datetime.now() - self.last_date
				if dif >= datetime.timedelta(days=1):
						
						self.last_date = datetime.datetime.now()
						array = self.get_array() 
						self.today_word =array[random.randint(0,len(array)-1)]
						t = time.mktime(self.last_date.timetuple())
						save_load.write(self._id,"wordle_guessed", 0)
						save_load.write(self._id,"wordle_date", t)
						save_load.write(self._id,"wordle_str","")
						self.mes = ""
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
				self.today_word_guessed = save_load.read(self._id,"wordle_guessed",0)
				if self.today_word_guessed == 1:
						dif = datetime.timedelta(days=1) - (datetime.datetime.now() - self.last_date)
						return -1, f"На этом сервере слово уже угадано,следующее через {dif}"
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
																new+=try_word[i];
														elif i in guessed:
																new+=try_word[i].lower();
														else:
																new+="~~"+try_word[i].lower()+"~~";
												self.mes +="\n" + new + "\n" + "угадано " + str(len(guessed)) + " из которых на своем месте " + str(len(full_guessed))
												save_load.write(self._id,"wordle_str",self.mes)
												print(self.mes)
												return 0,self.mes
										else:
												self.mes+="\n" + f"слово угадано - {self.today_word}"
												save_load.write(self._id,"wordle_str",self.mes)
												save_load.write(self._id,"wordle_guessed",1)
												return 1,self.mes
								else:

										return -1,"не знаю такого слова, попробуй другое"
						else:
								return -1,"длина слова 5 букв"
						

@bot.command(name = "wordle",aliases=["вордли","слово"])
async def try_wordle(ctx,word = None):
		try:
			game = wordle(ctx.guild.id)
			if not (word is None):
					U = UserCdWordle(ctx.author.id,ctx.guild.id)
					if U.is_cd() and (game.get_last_user() == ctx.author.id):
						await ctx.reply(f"кд еще {BeaTime(U.get_cd())} или дай другим поиграть")
					else:
						check,mes = game.attemp(word)
						if check == -1:
							await ctx.reply(mes)
						elif check == 0:
							await ctx.reply(mes)
							U.set_cd(3600)
							game.set_last_user(ctx.author.id)
						elif check == 1:
							W = Wallet(ctx.author.id)
							summa = round(300 * (1 + W.get(NUM.luck)/20))
							W.give(summa)
							await ctx.reply(f"Угадал, ты получил {summa} {VALUTE}  и кружку пива")
			else:
				await ctx.reply(f".{game.get_mes()}")
		except Exception as error:
				print(error)
				await ctx.reply("неправильные аргументы, попробуйте: ?wordle гойда")
				

@bot.command(name = "ставка",aliases=["казино","казик","рулетка"])
async def casino(ctx,summa = None,stavka = "черное"):
		if summa is None:
				await ctx.reply(f"команда ?ставка (сумма) (куда) \nможно ставить на черное или красное, а также на конкрентое число\nНапример\n?ставка 50 0\n?казино 100 черное")
		else:
				W = Wallet(ctx.author.id)
				if summa == "все":
						summa = W.check_balance()
				try:
						summa = int(summa)
				except:
						await ctx.reply("сумма должна быть целом числом")
						return 0
				K = 1
				mes = ""
				if (W.check_balance() >= summa and summa > 0):
						W.give(-summa)
						if stavka in ["черное","ч","black","b","чёрное","чёрный"]:
								stavka = 2
								K = 2    
						elif stavka in ["красное","к","red","r","красный","красного"]:
								stavka = 1
								K = 2
						elif stavka in ["зеленое","green","g"]:
								stavka = 0
								K = 36
						else:
								try:
										stavka = int(stavka)
										K = 36
								except:
										await ctx.send("не понял, попробуй ?ставка 50 черное")
										return 0
						#ставка принята
						number = random.randint(0,36)
						color = ""
						if number == 0:
								color = "зеленое"
						elif number%2 == 0:
								color = "черное"
						else:
								color = "красное"
						mes += f"На рулетке **{number} {color}**\n"
						if K == 2:
								if (stavka%2 == number%2) and (number != 0):
										mes +=f"✔️ ты выиграл **{summa}** {VALUTE}"
										W.give(summa*K)
								else:
										mes += f"❌ ты проебал **{summa}** {VALUTE}"
						else:
								if stavka == number:
										mes +=f"✔️✔️✔️ ГООООООЛ ты выиграл **{summa * K}** {VALUTE}"
										W.give(summa*K)
								else:
										mes +=f"❌ ты проебал **{summa}** {VALUTE}"
						await ctx.reply(mes)
								

				else:
						await ctx.reply("возвращайся когда станешь мммм... побогаче")

class deck:
		def __init__(self,list = None) -> None:
				if list == None:
						self.deck = []
						for i in range(0,36):
								self.deck.append(i)
						random.shuffle(self.deck)
				else:
						self.deck = list
		
		def value(self,card:int):
				val = card//4
				mast = card%4
				ret_val = 0
				if val <= 4:
						ret_val = val+6
				elif val == 5:
						ret_val = 2 #valet
				elif val == 6:
						ret_val = 3 #dama
				elif val == 7:
						ret_val = 4 #king
				elif val == 8:
						ret_val = 11 #ace
				else:
						print("ERROR")
				if mast == 0:
						return ret_val,"C"
				elif mast == 1:
						return ret_val,"D"
				elif mast == 2:
						return ret_val,"S"
				else:
						return ret_val,"H"
		def score(self):
				summa = 0
				for i in self.deck:
						a,b = self.value(i)
						summa+=a
				return summa
		def list(self):
				return self.deck
		def append(self,card:int):
				self.deck.append(card)
				return self.deck
		def remove(self,card:int):
				self.deck.remove(card)
				return self.deck
		def take(self)->int:
				card = random.choice(self.deck)
				self.remove(card)
				return card
		def emoji(self,sumbol):
				d = {'4C': '<:cardClubs_K:1258439004949577809>', '6C': '<:cardClubs_6:1258439007168106546>', '7C': '<:cardClubs_7:1258439008569135105>', '8C': '<:cardClubs_8:1258439010469285968>', '9C': '<:cardClubs_9:1258439012054601800>', '10C': '<:cardClubs_10:1258439013522473094>', '11C': '<:cardClubs_A:1258439015154188429>', '2C': '<:cardClubs_J:1258439016819462267>', '3C': '<:cardClubs_Q:1258439064265166948>', '4D': '<:cardDiamonds_K:1258439117432422564>', '6D': '<:cardDiamonds_6:1258439119084716062>', '7D': '<:cardDiamonds_7:1258439120380760167>', '8D': '<:cardDiamonds_8:1258439122264264857>', '9D': '<:cardDiamonds_9:1258439123887456309>', '10D': '<:cardDiamonds_10:1258439125673967712>', '11D': '<:cardDiamonds_A:1258439127557210222>', '2D': '<:cardDiamonds_J:1258439129092325518>', '3D': '<:cardDiamonds_Q:1258439154337972325>', '4H': '<:cardHearts_K:1258439224584048790>', '6H': '<:cardHearts_6:1258439226194661479>', '7H': '<:cardHearts_7:1258439227436437555>', '8H': '<:cardHearts_8:1258439229176938643>', '9H': '<:cardHearts_9:1258439231957766174>', '10H': '<:cardHearts_10:1258439233652396112>', '11H': '<:cardHearts_A:1258439235472592987>', '2H': '<:cardHearts_J:1258439237166956585>', '3H': '<:cardHearts_Q:1258439257656262758>', '4S': '<:cardSpades_K:1258439336840396871>', '6S': '<:cardSpades_6:1258439338241425470>', '7S': '<:cardSpades_7:1258439340506218597>', '8S': '<:cardSpades_8:1258439342540718152>', '9S': '<:cardSpades_9:1258439344448868474>', '10S': '<:cardSpades_10:1258439346361470976>', '11S': '<:cardSpades_A:1258439348357959690>', '2S': '<:cardSpades_J:1258439350128218132>', '3S': '<:cardSpades_Q:1258439406021509150>'}
				return d.get(sumbol)
class ochko:
		def __init__(self,_id,stavka = None) -> None:
				self._id = _id
				print("check0")
				if stavka is None:
						print("check1")
						self.stavka = save_load.read(self._id,f"{self._id}bj_stavka",None)
						if not (self.stavka is None):
								self.stavka = int(self.stavka)
						self._deck = deck(save_load.read(self._id,f"{self._id}bj_deck",None))
						self._hand = deck(save_load.read(self._id,f"{self._id}bj_hand",None))
						self._dealer = deck(save_load.read(self._id,f"{self._id}bj_dealer",None))
				else:
						self.stavka = stavka
						self._deck = deck()
						self._hand = deck([])
						self._dealer = deck([])
						self.dealer()
						self.update()
		def exist(self)->bool:
				print("check exist")
				if self.stavka is None:
						return False
				else:
						return True
		def update(self):
						save_load.write(self._id,f"{self._id}bj_stavka",self.stavka)
						save_load.write(self._id,f"{self._id}bj_deck",self._deck.list())
						save_load.write(self._id,f"{self._id}bj_hand",self._hand.list())
						save_load.write(self._id,f"{self._id}bj_dealer",self._dealer.list())
		def take(self):
				card = self._deck.take()
				self._hand.append(card)
				self.update()
				a,b = self._deck.value(card)
				return f"{a}{b}"
		def dealer(self):
				while self._dealer.score() < 17:
						card = self._deck.take()
						self._dealer.append(card)
						self.update()
		def check_winer(self):
				if self._hand.score() > 21:
						return -1
				elif self._dealer.score() > 21:
						return 1
				elif self._dealer.score() > self._hand.score():
						return -1
				elif self._dealer.score() < self._hand.score(): 
						return 1
				else:
						return 0
		def print(self,show_dealer = False)->str:
				mes = "**ОЧКО СТАТУС**\n"
				mes+="Рука дилера\n"
				back_e = "<:cardBackRed:1258496673483853906>"
				if show_dealer:
						for i in self._dealer.list():
								a,b = self._dealer.value(i)
								emoji = self._dealer.emoji(f"{a}{b}")
								mes += f"{emoji} "
								
								print("card",emoji,"ab",a,b,"id",i)
						mes += f"\nколичество очков:**{self._dealer.score()}/21**\n"
				else:
						mes += back_e * len(self._dealer.list())
				mes += '\n'
				mes += "Ваша рука\n"
				for i in self._hand.list():
						
						a,b = self._hand.value(i)
						emoji = self._hand.emoji(f"{a}{b}")
						mes += f"{emoji} "
						print("card",emoji,"ab",a,b,"id",i)
				mes += '\n'
				mes += f"количество очков:**{self._hand.score()}/21**\n"
				return mes
		def game_end(self):
				save_load.write(self._id,f"{self._id}bj_stavka",None)

@bot.command(name = "очко",aliases=["21","блэкджек","bj","blackjack"])
async def game21(ctx,comand = "help", num = 10):

		class Button(discord.ui.View):
			@discord.ui.button(label = "взять",style=discord.ButtonStyle.primary)
			async def button_other_callback(self,inter,button):
				UM = inter.user.id
				if UM == ctx.author.id:
					game = ochko(ctx.author.id)
					if not game.exist():
							button.disabled = True
							await inter.response.edit_message(content="игры не существует, напишите ?очко начать 20",view = None)
					else:
							game.take()
							if game._hand.score() > 21:
									button.disabled = True
									await inter.response.edit_message(content = f"перебор, **ты проиграл**\n{game.print()}",view=None)
									game.game_end()
							else:
									await inter.response.edit_message(content = game.print(),view = self)
			@discord.ui.button(label = "хватит",style=discord.ButtonStyle.danger)
			async def button_callback(self,inter,button):
				UM = inter.user.id
				if UM == ctx.author.id:
					game = ochko(ctx.author.id)
					if not game.exist():
							button.disabled = True
							await inter.response.edit_message(content = "игры не существует, напишите ?очко начать 20",view = None)
					else:
							win = game.check_winer()
							W = Wallet(ctx.author.id)
							mes = game.print(True)
							if win == 1:
									mes+=f"ты выиграл {game.stavka}{VALUTE}"
									W.give(game.stavka*2)
							elif win == -1:
									mes+=f"ты проиграл"
							else:
									mes+=f"ничья, деньги возращены на счет"
									W.give(game.stavka)
							game.game_end()
							button.disabled = True
							await inter.response.edit_message(content = mes,view = None)
					
			
		if comand in ["начать","старт","н","с","стартуем"]:
				num = num
				game = ochko(ctx.author.id)
				W = Wallet(ctx.author.id)
				if not game.exist():
						if num == "все" or num == "всё" or num == "all":
								num = W.check_balance()
								print(num)
						try:
								num = int(num)
						except:
								await ctx.reply("ставка должна быть целым числом")
								return 0
						else:
								
								if (num >= 10) and (W.check_balance() >= num):
										W.give(-num)
										game = ochko(ctx.author.id,num)
										await ctx.reply(f"игра началась\n{game.print()}",view = Button())
								else:
										await ctx.reply(f"минимальная ставка 10{VALUTE}")
										return 0

				else:
						await ctx.reply("игра уже идет")
		elif comand in ["взять","еще","ещё","в"]:
				game = ochko(ctx.author.id)
				if not game.exist():
						await ctx.reply("игры не существует, напишите ?очко начать 20")
				else:
						game.take()
						if game._hand.score() > 21:
								await ctx.reply(f"перебор, **ты проиграл**\n{game.print()}",view = Button())
								game.game_end()
						else:
								await ctx.reply(game.print())
		elif comand in ["хватит","стоп","х"]:
				game = ochko(ctx.author.id)
				if not game.exist():
						await ctx.reply("игры не существует, напишите ?очко начать 20")
				else:
						win = game.check_winer()
						W = Wallet(ctx.author.id)
						mes = game.print(True)
						if win == 1:
								mes+=f"ты выиграл {game.stavka}{VALUTE}"
								W.give(game.stavka*2)
						elif win == -1:
								mes+=f"ты проиграл"
						else:
								mes+=f"ничья, деньги возращены на счет"
								W.give(game.stavka)
						game.game_end()
						await ctx.reply(mes)
		elif comand in ["карты","карт","показать"]:
				game = ochko(ctx.author.id)
				if not game.exist():
						await ctx.reply("игры не существует, напишите ?очко начать 20")
				else:
						await ctx.reply(game.print())
		else:
				spravka = "**Правила игры**\nИгра идет против дилера, цель набрать больше очков, чем он, но не перебрать 21.\nТуз - 11 очков, Валет - 2, Дама - 3, Король - 4, остальные по номиналу\n"
				comands = "*Команды*\n?очко начать (ставка) - начинает игру, ставка должна быть больше 10\n" 
				comands +="?очко взять - взять карту\n"
				comands +="?очко карты - выводит ваши карты\n"
				comands +="?очко хватит - останавливает игру, если вы считаете что у вас достаточно карт\n"
				comands +="?очко помощь - выводит это сообщение\n"
				await ctx.reply(spravka+comands)


@bot.command()
async def emoji(ctx):
		await ctx.reply("<:cardClubs_7:1258439008569135105>")  
		mes = "1"
		emojiname = ""   
		i = 0 
		count = 0 
		see = bot.get_guild(1258438924133466142)
		#emoji = discord.utils.get(i.emojis, name=emojiname)
		list = [] 
		for i in see.emojis:
				a = f"<:{i.name}:{i.id}>\n"
				list.append(a)
		dict = {}
		count = 0
		for i in ["C","D","H","S"]:
				for j in range(0,9):
						if j == 0:
								q = 4
						elif j == 8:
								q = 3
						elif j == 7:
								q = 2
						else:
								q = j + 5
						dict.update({f"{q}{i}":f"{list[count]}"})
						count+=1
				

		print(dict)  
		await ctx.send(dict)

@bot.command(name = "click",aliases=["хомяк","тапать","кирпичи","клик"])
async def click(ctx):
	class View(discord.ui.View):
		val = 0.0
		clicked = 0
		k = 1
		@discord.ui.button(label = "кирпич",style=discord.ButtonStyle.primary, emoji="🧱")
		async def brick(self,inter,button):
				UM = inter.user.id
				mes = ""
				if UM == ctx.author.id:
					self.clicked +=1
					if random.randint(0,round(25*pow(self.k,self.k))) == 0:
						self.k += 0.1
						self.k = round(self.k,2)
					summa = round(random.uniform(0.1,0.5),2)
					mnoj = round(self.k * summa,2)
					self.val = round(self.val + mnoj,2)
					mes =f"**Клик** {self.clicked}\nЗа этот клик вы взяли {summa} x {self.k} = **{mnoj}**🧱\nНажмите 'вывод' чтобы закончить и вывести **{self.val}🧱**\n||Чем дольше кликаешь тем больше получаешь||"
					await inter.response.edit_message(content=mes, view=self)
		@discord.ui.button(label = "вывод",style=discord.ButtonStyle.danger)
		async def out(self,inter,button):
				UM = inter.user.id
				if UM == ctx.author.id:
					W = Wallet(ctx.author.id)
					sum = round(self.val)
					W.give(sum)
					self.val = 0
					mes =f"**Клик**\nпоздравляю вы спиздили со стройки {sum}🧱\nКликнуто **{self.clicked}**"
					await inter.response.edit_message(content=mes, view=None)
	await ctx.send("Нажми на кирпич",view = View(timeout=None))

				

print("wordle.py работает")


