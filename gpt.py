import g4f.client 
import g4f
from g4f.client import Client
from token_and_bot import TOKEN,bot;
from g4f.cookies import set_cookies


gpt_memory=[] 
def write(x:str): #память для чатХПТ
    if len(gpt_memory)>8:
        gpt_memory.pop(0);
    gpt_memory.append(x)
def read()->str:
    memory = ""
    count = 0;
    for i in gpt_memory:
        count += 1;
        memory += str(count) + " " + str(i) + " " + '\n'
    return memory;

def ask_gpt(promt:str)->str:
    try:
        client = Client(provider= g4f.Provider.GptTalkRu		) #provider=g4f.Provider.DuckDuckGo 

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": promt}],
        )
        answer = (response.choices[0].message.content)
        return answer;
    except:
         return "функция временно? не работают, потому что капиталисты пидорасы."

def ask_gpt4(promt:str)->str:
    client = Client(provider=g4f.Provider.You)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": promt}],
    )
    answer = (response.choices[0].message.content)
    return answer;

async def respond_to_user(ctx,memory:bool,mes:str):
    print ("хпт старт")
    if memory:
        task = str("Ты дискорд бот по имени Гойда ответь максимально неформально пользователю " + str(ctx.author.name) + ".Он говорит: '" + str(mes) + str("'"));
        task = "Вот что было в вашем диалоге, ЗАПОМНИ: " + read() + " " + task;
    else:
        task = mes;
    answer = ask_gpt(task);
    if memory:
        write("ТЕБЯ СПРОСИЛИ: " + str(mes));
        write("ТЫ ОТВЕТИЛ: " + str(answer));
    answer = answer.replace("@everyone", "ПИВО")
    answer = answer.replace("@here", "ПИВО")
    await ctx.reply(answer) 

#команды
@bot.command()
async def gpt(ctx,*, mes = "привет"):
    await respond_to_user(ctx,True,mes);

async def on_mention(ctx):
    mes = ctx.content.replace("<@800598406149701634>", "Гойда")
    await respond_to_user(ctx,True,mes);
    
@bot.command()
async def reset(ctx):
        gpt_memory.clear();
        print (gpt_memory);
        await ctx.reply("пон")

@bot.command()
async def memory(ctx):
        answer = "все что я помню: " + '\n' + read(); 
        await ctx.reply(answer);
        
@bot.command() #без промта и памяти
async def Tgpt(ctx,*, mes = "привет"):
    await respond_to_user(ctx,False,mes);


print ("gpt.py work")