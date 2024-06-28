import discord;
from token_and_bot import TOKEN,bot; 
import save_load
from discord.ext import commands;
from my_funcs import GetUserfromMention,toInt
import random
import datetime
import time

VALUTE = "🧱"

class UserCdDaily:
    def __init__(self,_id:int):
        self._id = _id
        self.cd_time = float(save_load.read(self._id,"UserCdDaily", 0))
        print("UserCd ",self._id,"UserCdDaily ",self.cd_time)
    def get_cd(self)->float:
        return (self.cd_time-time.time());
    def set_cd(self,value:float):
        self.cd_time = time.time() + value;
        save_load.write(self._id,"UserCdDaily",self.cd_time)
    def is_cd(self)->bool:
        return (self.cd_time >= time.time());

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

class product:
	def __init__(self,what) -> None:
			self._id = what
			if what == NUM.factory:
				self.price = 750
				self.name = "Завод"
				self.disc = "Позволяет получать ежедневную награду"
				self.aliases = ["завод","кирпичный","з",4]
			elif what == NUM.luck:
				self.price = 500
				self.name = "Чипсы"
				self.disc = "Очень вкусные чипсы лейс с крабом. Повышает удачу."
				self.aliases = ["чипсы","ч","Чипсы",1]
			elif what == NUM.dmg:
				self.price = 275
				self.name = "Урон"
				self.disc = "Не придумал смешное название(((((. Повышает время мута и кол-во денег которое вы можете украсть"
				self.aliases = ["dmg","урон",2]
			elif what == NUM.df:
				self.price = 325
				self.name = "ПВО"
				self.disc = "повышает защиту, уменьшает время мута и кол-во денег которое можно украсть у вас"
				self.aliases = ["пво","защита","def",3]
			elif what == NUM.armor:
				self.price = 100
				self.name = "Умиротворятель"
				self.disc = "Одноразовый. Защищает от резни."
				self.aliases = ["умиротворятель","защита","броня","у",5]
			elif what == NUM.city:
				self.price = 7500
				self.name = "Город"
				self.disc = "Счастье анкапа, приности в 15 раз больше денег чем завод"
				self.aliases = ["город","city","городов",6]
			elif what == NUM.country:
				self.price = 75000
				self.name = "Страна"
				self.disc = "Счастье анкапа, приности в 15 раз больше денег чем город"
				self.aliases = ["с","страна","стран","страну",7]
			elif what == NUM.people:
				self.price = 500
				self.name = "Люди"
				self.disc = "Увеличивают награду за сообщения на 60 кирпичей, что ты выберишь людей или чипсы?"
				self.aliases = ["люди","людей","детей","черные","дети",8]
			else:
				self.price = 9999999;
				self.aliases = [];
				self.name = ""
				self.disc = "если вы читаете это что-то работает неправильно"

	def alias(self,req:str)->bool:
		req = req.lower() 
		return ((req in self.aliases) or (req == self.name))
		

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
		mes = f"{VALUTE}Баланс: **{self.balance}**{VALUTE} \n🏦Банк: **{self.bank}**{VALUTE}"
		if self.factory > 0:
			mes+= f"\n🏭Заводов: **{self.factory}** шт."
		if self.city > 0:
			mes+= f"\n🏙️Городов: **{self.city}** шт."
		if self.country > 0:
			mes+= f"\n🏴Стран:  **{self.country}** шт."
		if self.people > 0:
			mes+= f"\n🕺~~Рабов~~ Наемных рабочих: **{self.people}** шт."
		if self.armor > 0:
			mes+= f"\n🧻Умиротворителей  **{self.armor}** шт."
		mes+=f"\n🔪**{self.dmg}** | 🛡️**{self.df}** | 🍀**{self.luck}**"
		mes+=f"\n\n*Примерный капитал прожиточного минимума* **{self.get_capital()}**{VALUTE}"
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
	def get_price(self,what:int,price:int,value:int = 1,for_all = False)->int:
		if for_all:
			now_value = 0
		else:
			now_value = self.get(what)
		summa = 0
		for i in range(0,value):
			summa += price * pow(1.20,now_value)
			now_value += 1
			print(summa,now_value)
		return round(summa)
	def get_capital(self)->int:
		summa = self.get(NUM.balance) + self.get(NUM.bank)
		for i in NUM.array():
			prod = product(i)
			summa += self.get_price(i,prod.price,self.get(i),True)
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
		dif = datetime.timedelta(seconds=U.get_cd())
		await ctx.reply(f"кд еще {dif} сек")
	else:
		W = Wallet(ctx.author.id)
		summa = round(random.uniform(100,500 * (1 + W.get(NUM.luck)/25)));
		W.give(summa);
		mes = ""
		mes += ("вы получили " + str(summa) + f"{VALUTE} от кирпичного бога")
		Zavod = W.get(NUM.factory)
		i = 0
		if Zavod > 0:
			summa = 0;
			for i in range(0,min(1024,Zavod)):
				summa +=round(random.uniform(75,100 * (1 + W.get(NUM.luck)/25)) )
			mes += f"\nвы получили {summa}{VALUTE} с {i+1} заводов"
			W.give(summa)
		City = W.get(NUM.city)
		if City > 0:
			summa = 0;
			for i in range(0,min(1024,City)):
				summa +=round(random.uniform(1125,1500*(1 + W.get(NUM.luck)/25)))
			mes += f"\nвы получили {summa}{VALUTE} с {i+1} городов"
			W.give(summa)
		Country = W.get(NUM.country)
		if Country > 0:
			summa = 0;
			for i in range(0,min(1024,Country)):
				summa +=round(random.uniform(16875,22500 * (1 + W.get(NUM.luck)/20)))
			mes += f"\nвы получили {summa}{VALUTE} с {i+1} стран"
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
		if summa > 0:
			summa *= -1;
			final_summa = thief.transfer(victim,summa)
			if final_summa > 0:
				mes = "Вы перевели " + str(final_summa) + f" {VALUTE} пользователю " + str(member) + " " + reason;
			else:
				mes = "Денег нет, но вы держитесь"
		else:
			mes = "накидал тебе за щеку, проверяй"
			m_member = ctx.guild.get_member(ctx.author.id)
			time = (datetime.timedelta(seconds=60))
			await m_member.timeout(time, reason="пидор")
		await ctx.reply(mes);
	except Exception as ER:
		print(ER)

@bot.command(name = "купить",aliases=["покупка","магазин"])
async def shop(ctx,who = None,value = 1):
	value = round(value)
	mes = "ошибка"
	if who is None:
		#список товаров
		W = Wallet(ctx.author.id)
		embed = discord.Embed(title="Магазин")
		for i in NUM.array():
			num = i - 100
			prod = product(i)
			embed.add_field(name=f"#{num}. {prod.name} {W.get_price(i,prod.price)} {VALUTE} ({prod.price} {VALUTE})", value=prod.disc, inline=False)
		await ctx.reply(embed=embed)
	else:
		#собственно покупка
		if False:
			mes = "в магазине нихуя нет"
		else:
			W = Wallet(ctx.author.id)
			Z = Wallet(800598406149701634)
			i = 0
			for i in NUM.array():
				prod = product(i)
				if prod.alias(who):
					break
			else:
				await ctx.reply("товар не найден")
				return 0
			prod = product(i)
			price = W.get_price(i,prod.price,value)
			if (price <= W.check_balance()) and value>0:
				W.transfer(Z,-price)
				W.set(i,value)
				print("W.set(i,value)",i,value)
				print("get",W.get(i))
				mes = f"вы успешно купили {prod.name} в кол-ве {value} за {price}{VALUTE}"
			else:
				mes = f"для вас {prod.name} в кол-ве {value} будет стоить {price}{VALUTE}"
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
				mes = "вы положили " + str(final_summa) + f" {VALUTE} в банк" 
			else:
				mes = "вы сняли " + str(final_summa) + f" {VALUTE}" 
			await ctx.reply(mes);
		except Exception as err:
			print(err)
			await ctx.reply("сумма должна быть целым числом")
	else:
		await ctx.reply("у банков в субботу выходной, шабат")


@bot.command(name ="топ", aliases=["лидеры","Топ","ТОП","Лидеры"]) 
async def top(ctx): 
	await ctx.send("ok")
	guild = ctx.message.guild
	mes = "**КИРПИЧНЫЕ МАГНАТЫ:**" + '\n'
	my_dict = {}
	for member in guild.members:
		W = Wallet(member.id)
		if (W.check_balance() + W.check_bank() > 1) and not (member.id == 800598406149701634):
			value = W.get_capital()
			print(value)
			user = member
			my_dict[user] = value
	sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1],reverse=True))
	count = 0
	for i in sorted_dict:
		count+=1
		name = i.display_name
		mes +=f"#{count} {name}: {sorted_dict[i]}{VALUTE}\n"
	print(mes)
	await ctx.reply(mes)


print("bank.py work")
