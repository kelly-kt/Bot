import pymongo
from datetime import datetime, timedelta

today_date = datetime.now()
extraction_date = today_date - \
    timedelta(days=1)

client = None
message_table = None
bad_message_table = None


def initialise_db(url):
    global client
    global message_table
    global bad_message_table

    print("Connecting to Mongo DB -", url)
    client = pymongo.MongoClient(url)

    message_table = client["ProjectDisbot"]["ChatLogs"]
    bad_message_table = client["ProjectDisbot"]["BadLang"]


def retrieve_messages_since(extraction_date):
    print('Retrieving all messages from', extraction_date, 'to now')

    return message_table.find()


def retrieve_bad_messages_since(extraction_date):
    print('Retrieving all bad messages from', extraction_date, 'to now')

    return bad_message_table.find()
