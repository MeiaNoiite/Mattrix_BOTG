from logging import exception
import discord,colorama,sys,json,typing,glob,os,time,psutil,random,asyncio
from discord.errors import Forbidden

from datetime import datetime
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions as missperm
from discord.ext.commands import *
from discord.ext.commands import DefaultHelpCommand
import discord.ext.commands.help
from Scripts.envcontroller import ReturnEnv as config
from Scripts.garc import Initgc
from pretty_help import PrettyHelp
pid = os.getpid()
py = psutil.Process(pid)
print('Starting UP....\n')
xy = open('./a.txt','r')
TK =""
for line in xy:
  TK += line
os.system('rm -rf /tmp/koderun/')
time.sleep(0.1)
os.system('mkdir /tmp/koderun/')
def rtk():
    pass
#config = json.loads(config_t)
client = discord.Client()
started = time.perf_counter()
total_commands = 0
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele +"\n" 
    
    # return string   
    return str1  
commands_loaded=0
pcmds = []

def returncmds():
    return listToString(pcmds)
def get_prefix(bot, message):
    with open('./data/prefixes.json', 'r') as f:
        prefixes = json.load(f) 
    if not message.guild:
        return ("dm! ")
    try:
        return prefixes[str(message.guild.id)]
    except KeyError:
        with open('./data/prefixes.json', 'w') as f:
            print("Criando Novo Prefixo....")
            prefixes[str(message.guild.id)] = config('PREFIX')
            json.dump(prefixes, f, indent=4)
            return prefixes[str(message.guild.id)]
    
bot = commands.Bot(command_prefix=get_prefix,
help_command=PrettyHelp(),
description="Um Simples bot do discord!"
)
cmds:list = []
cmd_folders = []

for r,s,files in os.walk("./Commands"):
    for folders in s:
        cmd_folders.append(folders)
    for folder in cmd_folders:
       for file in os.listdir(f"./Commands/{folder}"):
         if file.endswith(".py"):
            command = file.replace('.py',"")
            cmds.append(command)
            for cmd in cmds:
                try:
                    try:
                        bot.load_extension(f'Commands.{folder}.{command}')
                        commands_loaded += 1
                        pcmds.append(command)
                    except ExtensionAlreadyLoaded:
                            pass
                except Exception as e:
                    print(f"[{colorama.Fore.LIGHTYELLOW_EX}!!!{colorama.Fore.WHITE}] Ocorreu um erro ao carregar um comando: {e}")
                    exit(1)
end = time.perf_counter()
sys.stdout.write(f"\r[BOT.Main/CommandLoader/Ready] Carregado {commands_loaded} Comandos em {end - started:4f} Segundos.")
print(' ')
sys.stdout.write("\r[BOT.Main/INFO] Conectando com a api...")

@bot.event
async def on_message(message):
  if message.author.bot:
      return
  if message.author.id == bot.user.id:
      return
  if f"<@!{bot.user.id}>" in message.content:
        await message.channel.send(f"Olá, **{message.author.mention}**, Meu prefixo nesse server é `{get_prefix(message.guild.id,message)}`! digite `{get_prefix(message.guild.id,message)}help` para ver meus comandos!")

  try:
     open(f'./data/config/{message.guild.id}.json','r')
  except FileNotFoundError:
      f = open(f'./data/config/{message.guild.id}.json','w')
      a = {
          "cmdchannel":"any"
      }
      print("***\narquivo de configuração criado!\n**")
      json.dump(a,f)
      f.close()
  f = open(f'./data/config/{message.guild.id}.json','r')
 
  j = json.load(f)
  f.close()
  if message.content.startswith(get_prefix(message.guild.id,message)):
    if j['cmdchannel'] == 'any' or message.author.guild_permissions.administrator:
          pass
    elif j['cmdchannel'] != str(message.channel.id):
      await message.reply(f"Esse canal não pode executar comandos! o unico canal que pode executar comandos é <#{j['cmdchannel']}>")
      await asyncio.sleep(1)
      return
  await bot.process_commands(message)
@bot.event
async def on_command_error(ctx,e):

    if isinstance(e,CommandNotFound):
        await ctx.reply("Desculpe esse comando não existe.")
    elif isinstance(e,TimeoutError):
        await ctx.reply("[*]Info tempo limite excedido")
    elif isinstance(e,missperm) or isinstance(e,Forbidden):
        await ctx.reply("Sem  permissão.")
    else:
        em:discord.Embed = discord.Embed()
        em.title = ":("
        em.description = "Ocorreu um erro ao executar esse comando!"
        em.add_field(name="ERRO: ",value=f"`{e}`")
        em.color = 0x0000ff
        em.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
        em.timestamp = datetime.utcnow()
        await ctx.reply(embed=em)

@bot.event
async def on_guild_join(guild): #when the bot joins the guild
    with open('./data/prefixes.json', 'r') as f: #read the prefix.json file
        prefixes = json.load(f) #load the json file

    prefixes[str(guild.id)] = config('PREFIX')

    with open('./data/prefixes.json', 'w') as f: #write in the prefix.json "message.guild.id": "bl!"
        json.dump(prefixes, f, indent=4) #the indent is to make everything look a bit neater

@bot.event
async def on_guild_remove(guild): #when the bot is removed from the guild
    with open('./data/prefixes.json', 'r') as f: #read the file
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) #find the guild.id that bot was removed from

    with open('./data/prefixes.json', 'w') as f: #deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)
@bot.event
async def on_ready():
    os.system('rm -rf *.txt')

    sys.stdout.write(f"\r{colorama.Fore.GREEN}[BOT.Main/Ready] Conectado com a api BOT: {bot.user} PREFIXO PADRÃO: {config('PREFIX')}{ colorama.Fore.WHITE}\n")
    from Scripts.RedditController import reddit
   
    
    print(f"Conectado com a api do reddit! {reddit.update_checked}")
    await bot.change_presence(
        activity=discord.Game(name="Bot Reiniciado!"),
        status=discord.Status.online)
    time.sleep(5)
    bot.loop.create_task(change_s())
    bot.loop.create_task(run_memc())
async def run_memc():
    await Initgc()

async def change_s():

  games:list = ["Roblox", "Minecraft", "A alpha 1.2.4 do minecraft Já existiu?", "O Herobrines Já existiu?",
             "Minecraft Bedrock Edition", "Minecraft java Edition"]
  while True:
        
        selected_status = random.choice(games)
        await bot.change_presence(activity=discord.Game(name=f"Uso de ram: {round( py.memory_info()[0]  / 1000000):.2f}MB "),status=discord.Status.online)
        await asyncio.sleep(10)
        await bot.change_presence(
            activity=discord.Game(name=selected_status),
            status=discord.Status.online)
        await asyncio.sleep(10)
        await bot.change_presence(
      activity=discord.Game(name="Feito em Python!"),
      status=discord.Status.online)
        await asyncio.sleep(10)

try:
    bot.run(TK)
except Exception as e:
    print(f"\n\nBot Desligado Motivo: {e}\n\n")