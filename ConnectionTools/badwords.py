# The requests library is imported to retrieve messages from the discord channel
import requests
import json

url = None
headers = None


def initialise(badwords_api_url):
    global url
    global headers

    url = badwords_api_url
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "db57621136mshd9c16f34d317677p131ebbjsn21a8535f3f4f",
        'x-rapidapi-host': "neutrinoapi-bad-word-filter.p.rapidapi.com"
    }


def check_message(msg):
    payload = "censor-character=*&content=" + msg

    response = requests.request("POST", url, data=payload, headers=headers)

    response = json.loads(response.text)

    return response
