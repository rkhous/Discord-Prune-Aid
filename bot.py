import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix="=")
admin_id = "" #ID of the user that will be controlling the bot
server_id = "" #server id of the server this bot will be doing work on
everyone_id = "" #id for @everyone role so it can be ignored
on_ready_complete_channel = "" #channel ID the bot will send a message to once it grabs all users and their roles
token = "" #your bots token

@bot.event
async def on_ready():
    server = bot.get_server(server_id)
    userDict = {}
    for m in server.members:
        roles = []
        for r in m.roles:
            if r.id != everyone_id:
                roles.append(r.id)
        userDict[m.id] = roles
    with open("roles.json", "w") as f:
        f.write(json.dumps(userDict))
    await bot.send_message(destination=discord.Object(id=on_ready_complete_channel), content="Hey <@!" + str(admin_id) + ">, `roles.json` has been created. "
                  "Use `=checklist` to get the number of users I stored data on..")

@bot.command(pass_context=True)
async def checklist(ctx):
    if ctx.message.author.id == admin_id:
        try:
            with open("roles.json", "r") as f:
                dic = json.loads(f.read())
                await bot.say("There are currently " + str(len(dic)) + " users and their roles saved in `roles.json`!")
        except Exception as error:
            await bot.say("Error occurred.\n"
                          "```" + str(error) + "```")
    else:
        await bot.say("You are not an admin of this bot.")

@bot.command(pass_context=True)
async def delete(ctx):
    if ctx.message.author.id == admin_id:
        with open("roles.json", "r") as f:
            dic = json.loads(f.read())
            for n in dic:
                try:
                    await bot.remove_roles(n, dic[n])
                except Exception as error:
                    with open("logs.txt", "a") as f:
                        f.write(str(error) + "\n\n")
    else:
        await bot.say("You are not an admin of this bot.")

@bot.command(pass_context=True)
async def readd(ctx):
    if ctx.message.author.id == admin_id:
        await bot.say("Re-adding roles...")
        with open("roles.json", "r") as f:
            dic = json.loads(f.read())
            for n in dic:
                try:
                    await bot.add_roles(n, dic[n])
                except Exception as error:
                    with open("logs.txt", "a") as f:
                        f.write(str(error) + "\n\n")
        await bot.say("Done. I've added everyone's roles back. Shutting myself down.")
        await bot.close()
    else:
        await bot.say("You are not an admin of this bot.")




bot.run(token)
