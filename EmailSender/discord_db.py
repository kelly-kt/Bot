import pymongo
from pymongo import MongoClient
import pprint


client = None
message_table = None


def initialise_db(url):
    global client
    global message_table

    print("Connecting to Mongo DB -", url)
    client = pymongo.MongoClient(url)

    message_table = client["ProjectDisbot"]["ChatLogs"]

    x = message_table.find()

    msg_list = []

    for data in x:

        msg_list.append(data)

    with open('badlanguage.json', 'w+') as f:
        print(msg_list, file=f)


def insert_message(userName, channelName, msgContent, timeStamp, attachment=None):
    print("Adding message to DB:", userName, ":",
          channelName, ":", msgContent, ":", timeStamp)
    post = {"user_name": userName, "channel_name": channelName, "message_content": msgContent, "created_at": timeStamp
            }
    message_table.insert_one(post)
