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
		print(self._id," $:",self.balance,"B:",self.bank)
	def __str__(self):
		return f'🧱Баланс: **{self.balance}**🧱 \n🏦Банк: **{self.bank}**🧱 \n🏭Заводов **{self.factory}** штук'
	def get(self,what:int)->int:
		if what == NUM.balance:
			return self.balance;
		elif what == NUM.bank:
			return self.bank;
		elif what == NUM.luck:
			return self.luck;
		elif what == NUM.dmg:
			return self.dmg;
		elif what == NUM.df:
			return self.df;
		elif what == NUM.factory:
			return self.factory;
		else:
			return self._id;
	def set(self,what:int,value:int):
		if what == NUM.balance:
			self.balance += value;
		elif what == NUM.bank:
			self.bank += value;
		elif what == NUM.luck:
			self.luck += value;
		elif what == NUM.dmg:
			self.dmg += value;
		elif what == NUM.df:
			self.df += value;
		elif what == NUM.factory:
			self.factory += value;
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
	def banking(self,summa:int)->int:
		#снимает сумму с баланса и кидает ее в банк
		if summa>0:
			if self.balance >= summa:
				self.balance -= summa;
				self.bank += summa;
				self.update();
				return summa;
			else:
				i = self.balance;
				self.bank += i;
				self.balance = 0;
				self.update();
				return i;
		else:
			summa = abs(summa)
			if self.bank >= summa:
				self.bank -= summa;
				self.balance += summa;
				self.update();
				return summa;
			else:
				i = bank;
				self.balance += i;
				self.bank = 0;
				self.update();
				return i;
	def transfer(self,who,summa:int)->int:
		#переводим деньги из кошельк who в наш
		if summa >= 0:
			if who.balance > summa:
				who.balance -= summa;
				self.balance += summa;
				self.update();
				who.update();
				return summa;
			else:
				i = who.balance
				who.balance = 0;
				self.balance += i;
				self.update();
				who.update();
				return i;
		else:
			summa = abs(summa)
			who.thansfer(self,summa)


async def mes_reward(ctx):
	W = Wallet(ctx.author.id);
	mes_len = min(300,len(ctx.content))
	print(mes_len)
	summa = random.randint(1,int(mes_len)+1) * 2
	W.give(summa);
	print("вы получили " + str(summa) + " 🧱")


@commands.cooldown(1, 12*3600, commands.BucketType.user)
@bot.command(name = "награда",aliases=["дэйлик","завод"])
async def daily(ctx):
	W = Wallet(ctx.author.id)
	summa = random.randint(25,250);
	W.give(summa);
	mes += ("вы получили " + str(summa) + "🧱 от кирпичного бога")
	Zavod = W.get(NUM.factory)
	if Zavod > 0:
		summa = 0;
		for i in range(0,Zavod):
			summa += random.randint(50,75)*Zavod
		mes += f"\nвы получили {summa}🧱 с {Zavod} заводов"
		W.give(summa)
	ctx.reply(mes)
	

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
async def shop(ctx,who = None,value = 1):
	if who == None:
		ctx.reply("на данный момент можно купить только завод за 500🧱\n пропишите ?купить завод")
	elif who == "завод" or who == "з" or who == "кирпичный завод":
		W = Wallet(ctx.author.id)
		if W.check_balance() >= 500:
			W.transfer(800598406149701634,-500);
			W.set(NUM.factory,1);
			mes = "вы теперь счастливый обладатель завода"
		else:
			mes = "денег нет но вы держитесь"
	ctx.reply(mes)


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
			value = W.check_balance() + W.check_bank();
			user = member;
			my_dict[user] = value;
	sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1],reverse=True))
	count = 0
	for i in sorted_dict:
		count+=1
		name = i.display_name
		mes +="**#" + str(count) + "**: " + str(name) + ": " + str(sorted_dict[i]) + "🧱"+ '\n';	
	await ctx.reply(mes)



print("bank.py work")
