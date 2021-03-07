# guildsaver, a discord server/guild exporter
# file created: november 13 2020
# last updated: march 7 2021
# written by moxniso

import discord
import os
from sys import argv
from shutil import rmtree

intents = discord.Intents.all()
client = discord.Client(intents=intents)
guildid = 0
treeflag = 0
token = None
msglimit = 0

@client.event
async def on_ready():
    print("Succesfully connected to discord.com:443\nAccount: {}#{}".format(client.user.name, client.user.discriminator))
    await main(0)
    await client.logout()

def tryrmtree(name):
    try:
        rmtree(name)
    except OSError:
        print("\nFailed to delete directory " + name)
        treeflag = 1

async def main(errflag):
    msgcount = 0
    chancount = 0

    guild = client.get_guild(guildid)
    if guild == None:
        print("\nGuild not found!")
        return
    chanlen = len(guild.text_channels)
    
    if errflag == 0:
        if os.path.isdir(guild.name):
            print("A directory named " + guild.name + " already exists.")
            if (input("Do you want to overwrite it? (y/n):") == "y"):
                print("Overwriting...")
                tryrmtree(guild.name)
            else:
                return
    else:
        tryrmtree(guild.name)

    if treeflag == 1:
        return

    try:
        os.makedirs(guild.name)
    except OSError:
        print("\nUnable to create directory " + guild.name)
        return
    os.chdir(guild.name)

    print("Guild: " + guild.name)
    while (1):     
        for chan in guild.text_channels:
            print("Saving " + chan.name + "...")
            try:
                log = open(chan.name + ".txt", "w", encoding="utf-8")
            except OSError:
                print("File {} cannot be opened!".format(chan.name + ".txt"))
                break
            async for message in chan.history(limit=msglimit):
                log.write("[{}] {}: {}\n".format(message.created_at, message.author, message.content))
                msgcount += 1
            log.close()
            chancount += 1
        break
        
    if (chancount < (chanlen/2)):
        if (input("\nLess than half of the channels were saved ({}/{})\nWould you like to try again? (y/n):".format(chancount, chanlen)) == "y"):
            main(1)
            return # So the Done! msg isn't shown twice
        else:
            return
            
    print("\nDone!\nChannels saved: {}/{}\nMessages saved: {}".format(chancount, chanlen, msgcount))

if __name__ == "__main__":
    print("guildsaver, a Discord server/guild exporter\n2020 moxniso\n")
    try:
        token = argv[1]
        guildid = int(argv[2])
        msglimit = int(argv[3])
    except IndexError:
        print("Usage: guildsaver [token] [server ID] [msg per channel limit]")
        exit()
    except ValueError:
        print("Invalid server ID passed")
        exit()

    try:
        client.run(token, bot=False)
    except OSError:
        print("Failed to connect to discord.com:443")

