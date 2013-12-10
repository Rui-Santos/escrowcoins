'''
utility functions
'''
import settings
import requests

def send_simple_message(to,sender,message,subject):
    return requests.post(
        "https://api.mailgun.net/v2/samples.mailgun.org/messages",
        auth=("api",settings.MAILGUN_ACCESS_KEY),
        data={"from": sender,
              "to": to,
              "subject": subject,
              "text": message})


send_simple_message("madradavid@gmail.com","madradavid@yahoo.com","screw you","you too")