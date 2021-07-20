##################################################
# File: keep_alive.py
#
# This file manages the main file for the bot to keep running
##################################################
# Version: 1.00
# Date:    25 May 2021
##################################################

from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Hello, I'm alive"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
