import discord;
from token_and_bot import TOKEN,bot; 
import save_load
from discord.ext import commands;
from my_funcs import GetUserfromMention,toInt,BeaTime,UserCdParent,Give_Role,Remove_Role,Decorated
import random
import datetime
import time

VALUTE = "🧱"

class UserCdDaily(UserCdParent):
	name_for_file = "UserCdDaily"

class Num:
	def __init__(self):
		self.balance = 99
		self.bank = 100
		self.luck = 101
		self.dmg = 102
		self.df = 103
		self.factory = 104
		self.armor = 105
		self.city = 106
		self.country = 107
		self.people = 108
	def array(self):
		return [self.luck, self.dmg, self.df, self.factory, self.armor, self.city, self.country, self.people]
NUM = Num()

class Shop:
	def __init__(self,serv:int) -> None:
		self._id = serv
		self.load_list = save_load.read(self._id,"shop",[])
		self.true_list = self.list_for_default() + self.load_list
		print(self.true_list)
	def add_new(self,obj):
		self.load_list.append(obj)
		self.true_list.append(obj)
		save_load.write(self._id,"shop",self.load_list)
	def del_role(self,name):
		for i in self.load_list:
			if i.name == name:
				self.load_list.remove(i)
				save_load.write(self._id,"shop",self.load_list)
				return True
		return False
	@staticmethod
	def list_for_default():
		default = []
		default.append(product("Завод",750,"Позволяет получать ежедневную награду"))
		default.append(product("Город",7500,"Счастье анкапа, приности в 15 раз больше денег чем завод"))
		default.append(product("Страна",75000,"Счастье анкапа, приности в 15 раз больше денег чем город"))
		default.append(product("Урон",275,"Не придумал смешное название(((((. Повышает время мута и кол-во денег которое вы можете украсть"))
		default.append(product("ПВО",325,"Понижает время мута и кол-во денег которое у вас можно украсть"))
		default.append(product("Чипсы",500,"Очень вкусные чипсы лейс с крабом. Повышает удачу"))
		default.append(product("Люди",500,"Увеличивают награду за сообщения на 60 кирпичей, что ты выберишь людей или чипсы?"))
		default.append(product("Умиротворятель",100,"Одноразовый.Защищает от резни.",koef=1.1))
		return default

	
class product:
	def __init__(self,name,price,disc ="",koef = 1.2) -> None:
		self.name = name
		self.price = price
		self.disc = disc
		self.aliases = []
		self.koef = koef
	def get_price(self,wallet:int,value:int = 1)->int:
		now_value = Wallet(wallet).get(self.get_ID())
		summa = 0
		for i in range(0,value):
			summa += self.price * pow(self.koef,now_value)
			now_value += 1
			print(summa,now_value)
		return round(summa)
	def __getstate__(self) -> dict: 
		dict = {}
		dict["name"] = self.name
		dict["price"] = self.price
		dict["disc"] = self.disc
		dict["aliases"] = self.aliases
		dict["koef"] = self.koef
		return dict
	def __setstate__(self,dict:dict):
		self.name = dict["name"]
		self.price = dict["price"]
		self.disc = dict["disc"]
		self.aliases = dict["aliases"]
		self.koef = dict["koef"]
	def is_me(self,what):
		return (self.name.lower() == what.lower() or what.lower in self.aliases)
	def add_aliases(self,list:list):
		self.aliases.append(list)
	def get_ID(self)->int:
		attributes = {
			NUM.dmg: "Урон",
			NUM.luck: "Чипсы",
			NUM.df: "ПВО",
			NUM.factory: "Завод",
			NUM.armor: "Умиротворятель",
			NUM.city: "Город",
			NUM.country: "Страна",
			NUM.people: "Люди"
		}
		
		keys = [key for key, value in attributes.items() if value == self.name]
		print("selfname",self.name,"keys",keys)
		return keys[0]
	async def buy(self,ctx):
		W = Wallet(ctx.author.id)
		W.set(self.get_ID(),1)

class product_role(product):
	def __init__(self,name,price,disc ="",koef = 1,roleID:int = None) -> None:
		self.name = name
		self.price = price
		self.disc = disc
		self.aliases = []
		self.koef = koef
		self.roleID = roleID
	def get_price(self,wallet,value):
		return self.price
	def __getstate__(self) -> dict: 
		dict = {}
		dict["name"] = self.name
		dict["price"] = self.price
		dict["disc"] = self.disc
		dict["aliases"] = self.aliases
		dict["koef"] = self.koef
		dict["roleID"] = self.roleID
		return dict
	def __setstate__(self,dict:dict):
		self.name = dict["name"]
		self.price = dict["price"]
		self.disc = dict["disc"]
		self.aliases = dict["aliases"]
		self.koef = dict["koef"]
		self.roleID = dict["roleID"]
	async def buy(self,ctx):
		print(self.__dict__)
		await Give_Role(ctx,self.roleID)

class Wallet:
	def __init__(self,_id:int):
		self._id = _id
		self.balance = int(save_load.read(_id,"$", 1))
		self.bank = int(save_load.read(_id,"bank", 100))
		self.luck = int(save_load.read(_id,"luck", 0))
		self.dmg = int(save_load.read(_id,"dmg", 0))
		self.df = int(save_load.read(_id,"df", 0))
		self.factory = int(save_load.read(_id,"factory", 0))
		self.armor = int(save_load.read(_id,"armor", 0))
		self.city = int(save_load.read(_id,"city", 0))
		self.country = int(save_load.read(_id,"country", 0))
		self.people = int(save_load.read(_id,"people", 0))
		print(self._id," $:",self.balance,"B:",self.bank)
	def __str__(self):
		mes = f"{VALUTE}Баланс: **{self.balance:,}**{VALUTE} \n🏦Банк: **{self.bank:,}**{VALUTE}"
		if self.factory > 0:
			mes+= f"\n🏭Заводов: **{self.factory:,}** шт."
		if self.city > 0:
			mes+= f"\n🏙️Городов: **{self.city:,}** шт."
		if self.country > 0:
			mes+= f"\n🏴Стран:  **{self.country:,}** шт."
		if self.people > 0:
			mes+= f"\n🕺~~Рабов~~ Наемных рабочих: **{self.people:,}** шт."
		if self.armor > 0:
			mes+= f"\n🧻Умиротворителей  **{self.armor:,}** шт."
		mes+=f"\n🔪**{self.dmg:,}** | 🛡️**{self.df:,}** | 🍀**{self.luck:,}**"
		mes+=f"\n\n*Примерный капитал прожиточного минимума* **{self.get_capital():,}**{VALUTE}"
		return mes;
	def get(self, what: int) -> int:
		attributes = {
			NUM.balance: self.balance,
			NUM.bank: self.bank,
			NUM.luck: self.luck,
			NUM.dmg: self.dmg,
			NUM.df: self.df,
			NUM.factory: self.factory,
			NUM.armor: self.armor,
			NUM.city: self.city,
			NUM.country: self.country,
			NUM.people: self.people
		}
		print ("atr",attributes.get(what))
		return (attributes.get(what))
	def reset(self):
		self.bank = 0
		self.balance = 0
		self.luck = 0
		self.dmg = 0
		self.df = 0
		self.factory = 0
		self.armor = 0
		self.city = 0
		self.country = 0
		self.people = 0
	def set(self, what: int, value: int):
		attributes = {
			NUM.balance: "balance",
			NUM.bank: "bank",
			NUM.dmg: "dmg",
			NUM.luck: "luck",
			NUM.df: "df",
			NUM.factory: "factory",
			NUM.armor: "armor",
			NUM.city: "city",
			NUM.country: "country",
			NUM.people: "people"
		}
		if what in attributes:
			setattr(self, attributes[what], getattr(self, attributes[what]) + value)
			self.update()
	def check_balance(self)->int:
		print("self.balance",self.balance)
		return self.balance;
	def check_bank(self)->int:
		print("self.bank",self.bank)
		return self.bank;
	def give(self,summa:int)->int:
		self.balance += summa;
		self.update();
		return summa;
	def update(self):
		save_load.write(self._id,"$",self.balance);
		save_load.write(self._id,"bank",self.bank);
		save_load.write(self._id,"luck",self.luck);
		save_load.write(self._id,"dmg",self.dmg);
		save_load.write(self._id,"df",self.df);
		save_load.write(self._id,"factory",self.factory);
		save_load.write(self._id,"armor",self.armor);
		save_load.write(self._id,"city",self.city);
		save_load.write(self._id,"country",self.country);
		save_load.write(self._id,"people",self.people);
	def banking(self, summa: int) -> int:
		if summa > 0:
			withdraw = min(self.balance, summa)
			self.balance -= withdraw
			self.bank += withdraw
			self.update()
			return withdraw
		else:
			summa = abs(summa)
			withdraw = min(self.bank, summa)
			self.bank -= withdraw
			self.balance += withdraw
			self.update()
			return withdraw
	def transfer(self, who, summa: int) -> int:
		# переводим деньги из кошелька who в наш
		summa = min(summa, who.balance)
		summa = max(summa, -self.balance)
		
		who.balance -= summa
		self.balance += summa
		self.update()
		who.update()
		
		return abs(summa)
	def is_armor(self)->bool:
		if self.get(NUM.armor)> 0:
			self.set(NUM.armor,-1)
			return True
		else:
			return False
	def get_capital(self)->int:
		summa = self.get(NUM.balance) + self.get(NUM.bank)
		for i in Shop.list_for_default():
			summa += i.get_price(self._id,self.get(i.get_ID()))
		return summa


async def mes_reward(ctx):
	await ctx.add_reaction("🧱")
	W = Wallet(ctx.author.id);
	mes_len = min(300,len(ctx.content))
	summa = round(((random.randint(1,round(int((mes_len)+1) * (1 + W.get(NUM.luck)/20)) )) +  W.get(NUM.people)*30) * 2)
	W.give(summa);
	print(f"вы получили {summa} {VALUTE}")


@bot.command(name = "награда",aliases=["дэйлик","завод"])
async def daily(ctx):
	U = UserCdDaily(ctx.author.id)
	if U.is_cd():
		print(U.get_cd())
		await ctx.reply(f"кд еще {BeaTime(U.get_cd())} сек")
	else:
		W = Wallet(ctx.author.id)
		summa = round(random.uniform(100,500 * (1 + W.get(NUM.luck)/25)));
		W.give(summa);
		mes = ""
		mes +=f"вы получили {summa:,}{VALUTE} от кирпичного бога"
		Zavod = W.get(NUM.factory)
		i = 0
		if Zavod > 0:
			summa = 0
			for i in range(0,min(1024,Zavod)):
				summa +=round(random.uniform(75,100 * (1 + W.get(NUM.luck)/25)) )
			mes += f"\nвы получили {summa:,}{VALUTE} с {i+1} заводов"
			W.give(summa)
		City = W.get(NUM.city)
		if City > 0:
			summa = 0;
			for i in range(0,min(1024,City)):
				summa +=round(random.uniform(1125,1500*(1 + W.get(NUM.luck)/25)))
			mes += f"\nвы получили {summa:,}{VALUTE} с {i+1} городов"
			W.give(summa)
		Country = W.get(NUM.country)
		if Country > 0:
			summa = 0;
			for i in range(0,min(1024,Country)):
				summa +=round(random.uniform(16875,22500 * (1 + W.get(NUM.luck)/20)))
			mes += f"\nвы получили {summa:,}{VALUTE} с {i+1} стран"
			W.give(summa)
		U.set_cd(3600*8)
		await ctx.reply(mes)
	

@bot.command(name = "перевод",aliases=["СБП","cбп","СПБ","спб"])
async def trans(ctx,member,summa = 1,*,reason = ''):
	try:
		Umember = GetUserfromMention(member).id;
		thief = Wallet(ctx.author.id);
		victim = Wallet(Umember);
		mes = ""
		summa = min(summa,9999)
		if summa > 0:
			summa *= -1;
			final_summa = thief.transfer(victim,summa)
			if final_summa > 0:
				mes =f"Вы перевели {final_summa:,}{VALUTE} пользователю {member} {reason}"
			else:
				mes = "Денег нет, но вы держитесь"
		else:
			mes = "накидал тебе за щеку, проверяй"
			m_member = ctx.guild.get_member(ctx.author.id)
			time = (datetime.timedelta(seconds=60))
			await m_member.timeout(time, reason="hb")
		await ctx.reply(mes);
	except Exception as ER:
		print(ER)

@bot.command(name = "купить",aliases=["покупка","магазин"])
async def shop(ctx,who = None,value = 1):
	value = round(value)
	
	S  = Shop(ctx.guild.id)

	if who is None:
		#список товаров
		W = Wallet(ctx.author.id)
		embed = discord.Embed(title="Магазин")
		count = 0
		for i in S.true_list:
			count+=1
			prod = i
			embed.add_field(name=f"#{count}. {prod.name} {prod.get_price(ctx.author.id,1):,} {VALUTE} ({prod.price} {VALUTE})", value=prod.disc, inline=False)
		await ctx.reply(embed=embed)
	else:
		#собственно покупка
		if False:
			mes = "в магазине нихуя нет"
		else:
			W = Wallet(ctx.author.id)
			Z = Wallet(800598406149701634)
			i = None
			for prod in S.true_list:
				if prod.is_me(who):
					break
			else:
				await ctx.reply("товар не найден")
				return 0
			price = prod.get_price(ctx.author.id,value)
			if (price <= W.check_balance()) and value>0:
				W.transfer(Z,-price)
				for i in range(0,value):
					await prod.buy(ctx)
				mes = f"✔️ вы успешно купили {prod.name} в кол-ве {value} за {price:,}{VALUTE}"
			else:
				mes = f"❌ для вас {prod.name} в кол-ве {value} будет стоить {price:,}{VALUTE}"
		await ctx.reply(mes)


@bot.command(name = "баланс",aliases=["бал","счет"])
async def my_bal(ctx,who = None):
	try:
		i = 0
		mes = ""
		print("баланс воркинг")
		if who == None:
			i = Wallet(ctx.author.id)
			User = ctx.author.mention;
		else:
			i = Wallet(GetUserfromMention(who).id)
			User = who
		mes = f"**Баланс пользователя** {User}: \n{i}"
		await ctx.reply(mes)
	except:
		mes = f"Ошибка \nвызов команды должен выглядить так: \n?баланс @кто-нибудь"
		await ctx.reply(mes)


@bot.command(name = "банк",aliases=["вклад","вывод"])
@Decorated(Bank=True)
async def bank(ctx,summa = "все"):
	now = datetime.datetime.now()  
	if datetime.datetime.weekday(now)!=5:
		print("bank")
		W = Wallet(ctx.author.id)
		if summa == "все":
			summa = W.check_balance();
		try:
			summa = int(summa)
			print("bank2")
			final_summa = W.banking(summa)
			if summa>0:
				mes =f"вы положили {final_summa:,} {VALUTE} в банк" 
			else:
				mes =f"вы cняли {final_summa:,} {VALUTE}"
			await ctx.reply(mes);
		except Exception as err:
			print(err)
			await ctx.reply("❌ сумма должна быть целым числом")
	else:
		await ctx.reply("❌ у банков в субботу выходной, шабат")


@bot.command(name ="топ", aliases=["лидеры","Топ","ТОП","Лидеры"]) 
async def top(ctx): 
	await ctx.send("ok")
	guild = ctx.message.guild
	mes = "**КИРПИЧНЫЕ МАГНАТЫ:**" + '\n'
	my_dict = {}
	for member in guild.members:
		W = Wallet(member.id)
		if (W.get_capital() > 10) and not (member.id == 800598406149701634):
			value = W.get_capital()
			print(value)
			user = member
			my_dict[user] = value
	sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1],reverse=True))
	count = 0
	for i in sorted_dict:
		count+=1
		name = i.display_name
		mes +=f"#{count} {name}: {sorted_dict[i]:,}{VALUTE}\n"
	print(mes)
	await ctx.reply(mes)
@commands.has_permissions(administrator = True)
@bot.command(name = "добавить_роль",aliases=["д_р","add_role"])
async def add_role(ctx,roleID,price,name = "Роль",*,desc=""):
	try:
		price = int(price)
		roleID = int(roleID)
	except:
		await ctx.reply(f"Цена должна быть целым числом\nПример ?add_role 391032392102302 1000 имя_в_одно_слово описание")
	else:
		if price<1:
			await ctx.reply(f"Цена должа быть больше 1\nПример ?add_role 391032392102302 1000 имя_в_одно_слово описание")
		else:
			try:
				await Give_Role(ctx,roleID)
				await Remove_Role(ctx,roleID)
			except Exception as err:
				await ctx.reply("Не могу выдать эту роль")
				print(err)
			else:
				name = name.replace(" ","_")
				print("SDSDSDSDS")
				S = Shop(ctx.guild.id)
				obj = product_role(name,price,desc,1,roleID)
				S.add_new(obj)
				await ctx.reply("Роль добавленна в магазин")
@commands.has_permissions(administrator = True)
@bot.command(name = "удалить_роль",aliases=["у_р","remove_role"])
async def remove_role(ctx,name):
	S = Shop(ctx.guild.id)
	if S.del_role(name):
		await ctx.reply("успешно удаленно")	
	else:
		await ctx.reply("не нашел такой роли\nПопробуйте ?remove_role имя_в_одно_слово")	

print("bank.py work")
