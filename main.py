from discord import Intents, Client, Message, Guild
from discord.ext import commands
import discord
import requests
from responses import get_response, get_facts
import os
from dotenv import load_dotenv
from typing import Final


# load token from .env
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents) 

# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    report_to_mods = False
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return
    try:
        response: str = get_response(message, user_message)
        if response.startswith("inappropriate language detected:"):
            report_to_mods = True
        if report_to_mods:
            try:
                guild = message.guild  # Get the server
                mod_role = discord.utils.get(guild.roles, name="mod")  # Find the mod role
                mod_members = [member for member in guild.members if mod_role in member.roles]
                for member in mod_members:
                    try:
                        await member.send(response)  # DM all mods
                    except discord.Forbidden:
                        print(f"Could not send DM to {member.name} (DMs disabled)")
                await message.channel.send("message has been flagged and the moderators have been alerted")
                await message.channel.send(response)
            except Exception:
                print("there seems to be a problem with alerting the mods...")
    except Exception as e:
        print(e)
'''
    try:
        response: str = get_response(user_message)
        if is_private:
            await message.author.send(response)
        elif send_to_mod:
            try:
                guild = message.guild  # Get the server
                mod_role = discord.utils.get(guild.roles, name="mod")  # Find the mod role
                mod_members = [member for member in guild.members if mod_role in member.roles]
                for member in mod_members:
                    try:
                        await member.send(response)  # DM all mods
                    except discord.Forbidden:
                        print(f"Could not send DM to {member.name} (DMs disabled)")
                await message.channel.send("message has been flagged and the moderators have been alerted")
            except Exception:
                print("there seems to be a problem with alerting the mods...")
        else:
            await message.channel.send(response) # this is the part that actually sends the discord message 
    except Exception as e:
        print(e)'''


# STEP 3: HANDLING THE STARTUP FOR OUR BOT
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')


# STEP 4: HANDLING INCOMING MESSAGES
@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    ctx = await bot.get_context(message)
    await bot.process_commands(message)

    if ctx.command is None:
        await send_message(message, user_message)
 


@bot.command()
async def factcheck(ctx, *, claim: str = None):

    if ctx.message.reference: # basically if the message is a reply
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)  # Get the original message
        claim = replied_message.content  # Extract the text from the replied message

    if not claim:
        await ctx.send("Please provide a claim or reply to a message to be factcheck'ed")
        return

    factuality = get_facts(claim)
    await ctx.channel.send(factuality)


# STEP 5: MAIN ENTRY POINT
def main() -> None:
    bot.run(TOKEN)


if __name__ == '__main__':
    main()