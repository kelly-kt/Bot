##################################################
# File: discord_client.py
#
# This file manages the bot and all its functions that are carried out in the discord
##################################################
# Version: 1.00
# Date:    25 May 2021
##################################################

import json
import random
import discord
from discord.ext import commands
import Config
import discord_db
import badwords

# The discord client and bot are Python object that is use to send various commands to the Discord's server.
client = discord.Client()
bot = commands.Bot("!")


# The event is defined for the bot
# This code will only run in response to the specific event instead of running the entire code
@bot.event
# The on_ready() function is used to connect the program to the discord server
async def on_ready():
    print('Connected to Discord')


@bot.event
async def on_message(message):
    # if the message is sent by bot it will return and do nothing
    if message.author == bot.user:
        return

    print('Checking:', message.content)

    # Check message for bad language
    response = {"api-error": True,
                "api-error-msg": "language detector disabled"}
    response = badwords.check_message(message.content)

    # Check outcome of bad language detection
    if "api-error" in response:
        # Bad language detection failed, display error to system and save message to DB
        print("Error:", response['api-error-msg'])
        discord_db.insert_message(
            message.author.name, message.channel.name, message.content, message.created_at)

    elif response["is-bad"]:
        # Message contains bad language, respond in discord and add message to bad language DB
        warning_msg = random.choice(json.loads(
            (Config.config['badwords']['responses']))) + "\n"
        warning_msg += "**User**: " + message.author.name + "\n"
        warning_msg += "**Message Content**: " + \
            response["censored-content"] + "\n"
        print("Message is bad")
        print(warning_msg)
        # This function will send the warning_msg to the channel when badwords are detected
        await message.channel.send(warning_msg)
        # This function automatically adds reaction to message that contains bad words
        await message.add_reaction('⚠️')
        discord_db.insert_bad_message(message.author.name, message.channel.name,
                                      message.content, message.created_at, response["bad-words-list"])

    else:
        # Message contains NO bad language, add message to DB
        print("Message is OK:", message.content)
        discord_db.insert_message(
            message.author.name, message.channel.name, message.content, message.created_at)


# The step is to prevent overriding the default provided in the on_message() function that forbids running extra commands
    await bot.process_commands(message)

# Runs the bot using the bot's token


def start_bot():
    bot.run(Config.config['discord']['token'])
