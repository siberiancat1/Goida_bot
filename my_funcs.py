from token_and_bot import TOKEN,bot;
import re
def minmax(minimal,value,maximum):
    return min(maximum,max(minimal,value))

def GetUserfromMention(friend):
    try:
        a = Int(friend)
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


async def Remove_Role(user,role_id):
    try:
        role = get(user.guild.roles, id = role_id) 
    except:
        print("role issue")
        return 0;
    try:
        await bot.remove_roles(user, role)
        return 1;
    except:
        print("per. issue")
        return 0;

async def Give_Role(user,role_id):
    try:
        role = get(user.guild.roles, id = role_id) 
    except:
        print("role issue")
        return 0;
    try:
        await bot.add_roles(user, role)
        return 1;
    except:
        print("per. issue")
        return 0;
print("my_funcs work")