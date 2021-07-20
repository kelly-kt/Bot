
# The keep_alive library allows the bot to keep running even when the brower has been shut down
from keep_alive import keep_alive

# Import modules required by the bot
import Config
import discord_db
import discord_client
import badwords

# This function will initialise the entire bot program
# First we load the configuration file which stores all settings for the program
# Then we initialise the database module/library with the URL details of the database from the configuration file


def initialise_bot():
    print("Initialising Discord Bot")
    Config.load_configuration('config.ini')

    discord_db.initialise_db(Config.config["database"]["mongo"])

    badwords.initialise(Config.config["badwords"]["url"])

# This function runs the main file of the program


def main():
    initialise_bot()

    keep_alive()

    discord_client.start_bot()


# if __main__ == "__main__":
main()
