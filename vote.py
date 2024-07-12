from token_and_bot import TOKEN,bot; 
import save_load
class vote:
    def __init__(self,mes):
        self.mes = mes
        self.val = save_load.read(mes,f'vote{mes}',False)
    def exist(self)->bool:
        return self.val
    def create(self,ctx = None,who = None, duration = None,reason = None, ban = False)->None:
        if not self.val:
            save_load.write(self.mes,f'vote{self.mes}',True)
            self.author = ctx.author.id
            self.accused = who
            self.duration = duration
            self.ban = ban
            save_load.write(self.mes,f'vote_duration{self.mes}', duration)
            save_load.write(self.mes,f'vote_accused{self.mes}', who)
            save_load.write(self.mes,f'vote_author{self.mes}', self.author)
            save_load.write(self.mes,f'vote_ban{self.mes}', ban)
        else:
            self.duration = save_load.read(self.mes,f'vote_duration{self.mes}', None)
            self.accused = save_load.read(self.mes,f'vote_accused{self.mes}', None)
            self.author  = save_load.read(self.mes,f'vote_author{self.mes}', None)
            self.ban = save_load.read(self.mes,f'vote_ban{self.mes}', None)
    def update(self):
        pass


@bot.command(name = "vote")
async def voted(ctx,who,duration,*,reason="которую не хочет разглошать"):
    string = f"**Голосование** \n{ctx.author.mention} предлагает замутить {who} на {duration} минут по причине {reason}"
    mes = (await ctx.send(string)).id
    await mes.add_reaction("✅")
    await mes.add_reaction("❌")
    obj_vote = vote(mes)
    obj_vote.create(ctx,who,duration,reason,False)

def check(id):
    obj_vote = vote(id)
    if obj_vote.exist():
        obj_vote.update()    