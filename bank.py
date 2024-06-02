import discord;
from token_and_bot import TOKEN,bot; 
import save_load
from discord.ext import commands;
from my_funcs import GetUserfromMention,toInt
import random
import datetime


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
	#def array(self):
		#return [self.balance, self.bank, self.luck, self.dmg, self.df, self.factory, self.armor]
NUM = Num()


class Wallet:
	def __init__(self,_id:int):
		self._id = _id;
		self.balance = int(save_load.read(_id,"$", 1))
		self.bank = int(save_load.read(_id,"bank", 100))
		self.luck = int(save_load.read(_id,"luck", 0))
		self.dmg = int(save_load.read(_id,"dmg", 0))
		self.df = int(save_load.read(_id,"df", 0))
		self.factory = int(save_load.read(_id,"factory", 0))
		self.armor = int(save_load.read(_id,"armor", 0))
		self.city = int(save_load.read(_id,"city", 0))
		print(self._id," $:",self.balance,"B:",self.bank)
	def __str__(self):
		return f'🧱Баланс: **{self.balance}**🧱 \n🏦Банк: **{self.bank}**🧱 \n🏭Заводов **{self.factory}** шт.\n🏙️Городов **{self.city}** шт.\n🔪**{self.dmg}** | 🛡️**{self.df}** | 🍀**{self.luck}**'
	def get(self, what: int) -> int:
		attributes = {
			NUM.balance: self.balance,
			NUM.bank: self.bank,
			NUM.luck: self.luck,
			NUM.dmg: self.dmg,
			NUM.df: self.df,
			NUM.factory: self.factory,
			NUM.armor: self.armor,
			NUM.city: self.city
		}
		print (attributes.get(what))
		return (attributes.get(what))

	def set(self, what: int, value: int):
		if what == NUM.balance:
			self.balance+= value
		elif what == NUM.bank:
			self.bank+= value
		elif what == NUM.dmg:
			self.dmg+= value
		elif what == NUM.luck:
			self.luck+= value #код херня надо переделать
		elif what == NUM.df:
			self.df+=value
		elif what == NUM.factory:
			self.factory+=value
		elif what == NUM.armor:
			self.armor+=value
		elif what == NUM.city:
			self.city+=value
		self.update()
	def check_balance(self)->int:
		print(self.balance)
		return self.balance;
	def check_bank(self)->int:
		print(self.bank)
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
		
		return summa
	def is_armor(self)->bool:
		if self.get(NUM.armor)> 0:
			self.set(NUM.armor,-1)
			return True
		else:
			return False

async def mes_reward(ctx):
	W = Wallet(ctx.author.id);
	mes_len = min(300,len(ctx.content))
	print(mes_len)
	summa = round((random.randint(1,int(mes_len)+1) )* 2 * pow(1.1,W.get(NUM.luck)))
	W.give(summa);
	print("вы получили " + str(summa) + " 🧱")


@commands.cooldown(1, 12*3600, commands.BucketType.user)
@bot.command(name = "награда",aliases=["дэйлик","завод"])
async def daily(ctx):
	W = Wallet(ctx.author.id)
	summa =round(random.randint(25,250) * pow(1.1,W.get(NUM.luck)));
	W.give(summa);
	mes = ""
	mes += ("вы получили " + str(summa) + "🧱 от кирпичного бога")
	Zavod = W.get(NUM.factory)
	if Zavod > 0:
		summa = 0;
		for i in range(0,Zavod):
			summa +=round(random.randint(50,75) * pow(1.1,W.get(NUM.luck)))
		mes += f"\nвы получили {summa}🧱 с {Zavod} заводов"
		W.give(summa)
	City = W.get(NUM.city)
	if City > 0:
		summa = 0;
		for i in range(0,City):
			summa +=round(random.randint(750,1125)*pow(1.1,W.get(NUM.luck)))
		mes += f"\nвы получили {summa}🧱 с {City} городов"
		W.give(summa)
	await ctx.reply(mes)
	

@bot.command(name = "перевод",aliases=["СБП","cбп","СПБ","спб"])
async def trans(ctx,member,summa = 1,*,reason = ''):

	try:
		print('skwasfkfffd')
		Umember = GetUserfromMention(member).id;
		thief = Wallet(ctx.author.id);
		victim = Wallet(Umember);
		mes = "eror"
		print('skwasfkfffd')
		if summa > 0:
			print('skwasfkfffd')
			summa *= -1;
			final_summa = thief.transfer(victim,summa)
			if final_summa > 0:
				mes = "Вы перевели " + str(final_summa) + " 🧱 пользователю " + str(member) + " " + reason;
			else:
				mes = "Денег нет, но вы держитесь"
		else:
			print('penis')
			mes = "накидал тебе за щеку, проверяй"
			m_member = ctx.guild.get_member(ctx.author.id)
			time = (datetime.timedelta(seconds=60))
			await m_member.timeout(time, reason="пидор")
		await ctx.reply(mes);
	except Exception as ER:
		print(ER)

@bot.command(name = "купить",aliases=["покупка","магазин"])
async def shop(ctx,who = "",value = 1):
	class product:
		def __init__(self,what) -> None:
			self._id = what
			if what == NUM.factory:
				self.price = 750
				self.name = "Завод"
				self.disc = "Позволяет получать ежедневную награду"
				self.aliases = ["завод","кирпичный","з",4]
			elif what == NUM.luck:
				self.price = 300
				self.name = "Чипсы"
				self.disc = "Очень вкусные чипсы лейс с крабом. Повышает удачу."
				self.aliases = ["чипсы","ч","Чипсы",1]
			elif what == NUM.dmg:
				self.price = 275
				self.name = "Урон"
				self.disc = "Не придумал смешное название(((((. Повышает время мута и кол-во денег которое вы можете украсть"
				self.aliases = ["Урон","Dmg","урон",2]
			elif what == NUM.df:
				self.price = 325
				self.name = "ПВО"
				self.disc = "повышает защиту, уменьшает время мута и кол-во денег которое можно украсть у вас"
				self.aliases = ["ПВО","пво","защита","def",3]
			elif what == NUM.armor:
				self.price = 100
				self.name = "Умиротворятель"
				self.disc = "Одноразовый. Защищает от резни."
				self.aliases = ["умиротворятель","защита","броня","у",5]
			elif what == NUM.city:
				self.price = 7500
				self.name = "Город"
				self.disc = "Счастье анкапа, приности в 15 раз больше денег чем завод"
				self.aliases = ["город","city",6]
			else:
				self.price = 9999999;
				self.aliases = [];
				self.name = ""
				self.disc = "если вы читаете это что-то работает неправильно"

		def alias(self,req)->bool:
			if req in self.aliases or req == self.name:
				return True;
			else:
				return False;

	mes = "ошибка"
	if who == "":
		#список товаров
		embed = discord.Embed(title="Магазин") #,color=Hex code
		for i in range(101,106+1):
			num = i - 100
			prod = product(i)
			embed.add_field(name=f"#{num}. {prod.name} {prod.price} 🧱", value=prod.disc, inline=False)
		await ctx.reply(embed=embed)
	else:
		#собственно покупка
		W = Wallet(ctx.author.id)
		Z = Wallet(800598406149701634)
		i = 0
		for i in range(101,106+1):
			prod = product(i)
			if prod.alias(who):
				break
		else:
			await ctx.reply("товар не найден")
			return 0
		prod = product(i)
		if prod.price * value <= W.check_balance():
			W.transfer(Z,-prod.price)
			W.set(i,value)
			print("W.set(i,value)",i,value)
			print("get",W.get(i))
			mes = f"вы успешно купили {prod.name}"
		else:
			mes = "денег нет но вы держитесь"
		await ctx.reply(mes)


@bot.command(name = "баланс",aliases=["бал","счет"])
async def my_bal(ctx,who = None):
	try:
		i = 0;
		mes = ""
		print("баланс воркинг")
		if who == None:
			i = Wallet(ctx.author.id)
			User = ctx.author.mention;
		else:
			i = Wallet(GetUserfromMention(who).id);
			User = who;
		mes = "**Баланс пользователя** " + User + ":" + '\n' + str(i)
		await ctx.reply(mes)
	except:
		mes = "Ошибка" + '\n' + "вызов команды должен выглядить так" + '\n' + "?баланс @кто-нибудь";
		await ctx.reply(mes)


@bot.command(name = "банк",aliases=["вклад","вывод"])
async def bank(ctx,summa = "все"):
	print("bank")
	W = Wallet(ctx.author.id)
	if summa == "все":
		summa = W.check_balance();
	try:
		summa = int(summa)
		print("bank2")
		final_summa = W.banking(summa)
		if summa>0:
			mes = "вы положили " + str(final_summa) + " 🧱 в банк" 
		else:
			mes = "вы сняли " + str(final_summa) + " 🧱" 
		await ctx.reply(mes);
	except Exception as err:
		print(err)
		await ctx.reply("сумма должна быть целым числом")


@bot.command(name ="топ", aliases=["лидеры","Топ","ТОП","Лидеры"]) 
async def top(ctx): 
	await ctx.send("ok")
	guild = ctx.message.guild
	mes = "**КИРПИЧНЫЕ МАГНАТЫ:**" + '\n'
	my_dict = {}
	for member in guild.members:
		W = Wallet(member.id)
		if not (W.check_balance() == 1 and W.check_bank() == 100) and not (member.id == 800598406149701634):
			value = W.check_balance() + W.check_bank() + 750*W.get(NUM.factory);
			user = member;
			my_dict[user] = value;
	sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1],reverse=True))
	count = 0
	for i in sorted_dict:
		count+=1
		name = i.display_name
		mes +="**#" + str(count) + "**: " + str(name) + ": " + str(sorted_dict[i]) + "🧱"+ '\n';	
	await ctx.reply(mes)

W.update();
print("bank.py work")
