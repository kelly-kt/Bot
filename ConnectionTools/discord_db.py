##################################################
# File: discord_db.py
#
# This file manages the database and it will be added as a function in the bot to collect and store data in mongodb
##################################################
# Version: 1.00
# Date:    25 May 2021
##################################################

import pymongo

client = None
message_table = None
bad_message_table = None


def initialise_db(url):
    global client
    global message_table
    global bad_message_table

    print("Connecting to Mongo DB -", url)
    client = pymongo.MongoClient(url)

    # Setting the location of the database into the variables, message_table and bad_message_table
    message_table = client["ProjectDisbot"]["ChatLogs"]
    bad_message_table = client["ProjectDisbot"]["BadLang"]

# To find/retrieve data
    x = message_table.find()

    msg_list = []

    for data in x:

        # to add the data into the msg_list
        msg_list.append(data)

    # Creates a json file and stores all the messages collected from the discord channel
    # with open('badlanguage.json', 'w') as f:
    #    print(msg_list, file = f)

# This function insert message to mongodb


def insert_message(userName, channelName, msgContent, timeStamp, attachment=None):
    global message_table

    print("Adding message to DB:", userName, ":",
          channelName, ":", msgContent, ":", timeStamp)
    post = {"user_name": userName, "channel_name": channelName, "message_content": msgContent, "created_at": timeStamp
            }
    message_table.insert_one(post)

# This function insert bad message to mongodb


def insert_bad_message(userName, channelName, msgContent, timeStamp, bad_words, attachment=None):
    global bad_message_table

    print("Adding BAD message to DB:", userName, ":", channelName,
          ":", msgContent, ":", timeStamp, ":", bad_words)
    post = {"user_name": userName, "channel_name": channelName, "message_content": msgContent, "created_at": timeStamp, "bad_word_list": bad_words
            }
    bad_message_table.insert_one(post)
