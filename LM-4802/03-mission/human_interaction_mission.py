#!/usr/bin/python3

# Import necessary modules
from pprint import pprint
import requests
import json
import sys
import subprocess
import platform
import zipfile
import logging
import time
import os
import argparse
# Attempt to import flask module
try:
  from flask import Flask
  from flask import request
# If fails attempt to install the module
except:
  try:
    if platform.system() == "Windows":
      flask_install = subprocess.check_output("pip3 install Flask")
    else:
      flask_install = subprocess.check_output(["pip3 install Flask"], shell=True)
    from flask import Flask
    from flask import request
    print("Flask was successfully imported")
  except PermissionError as e:
    print("You don't have permissions to install flask library.\n"
        "Try to run the script with elevated privileges.")
    print(e)
    exit()



print('Setting global parameters.')
URL = "https://api.ciscospark.com/v1"
# BOT'S ACCESS TOKEN
bearer = "NGFhOWEwMzktYmJhMS00NjllLWEyNDQtNmQ1NWJjNjE1YzVhYzQxODIwZWYtNTUy"
headers = {
  "Accept": "application/json",
  "Content-Type": "application/json; charset=utf-8",
  "Authorization": "Bearer " + bearer
}

parser = argparse.ArgumentParser()
parser.add_argument('-e','--email', help='Provide email address for webhook filtering',required=True)
args = parser.parse_args()

if '@' in args.email:
  EMAIL=args.email
else:
  exit("Please provide an email address for webhook filtering.\n"\
    "Use '-h' to get help.")

def ngrok():
  if platform.system() == "Windows":
    print("Downloading ngrok for Windows OS from website...")
    win_ngrok = requests.get(
      "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip")
    print("Success!")
    print("Unzipping ngrok.zip file....")
    with open("ngrok.zip", "wb") as f:
      f.write(win_ngrok.content)
    with zipfile.ZipFile("ngrok.zip", "r") as z:
      z.extractall("./")
      print("Success!")
    return True
  elif platform.system() == "Linux":
    try:
      print("Checking if ngrok is present in current folder...")
      check_ngrok = subprocess.check_output(
        ["ls -al ./ | grep ngrok"], shell=True).decode("utf-8")
      if "x" in check_ngrok:
        print("Success!")
        return True
    except subprocess.CalledProcessError as e:
      print("ngrok was not found.")
      print("Downloading ngrok for UNIX OS from website...")
      set_ngrok = subprocess.Popen(
        ["wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip " \
         "&& unzip ngrok-stable-linux-amd64.zip "], shell=True)
      while set_ngrok.poll() is None:
        continue
      check_ngrok = subprocess.check_output(
        ["ls -al ./ | grep ngrok"], shell=True).decode("utf-8")
      if "x" in check_ngrok:
        print(
          "ngrok was successfully downloaded to current folder")
        return True
      else:
        print("Something went wrong!")
        return False
  else:
    print("Checking if ngrok is present in current folder...")
    check_ngrok = subprocess.Popen(["ls -al ./ | grep ngrok"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    check_ngrok = check_ngrok.stdout.read().decode("utf-8")
    if "x" in check_ngrok:
      print("Success!")
      return True
    else:
      print("ngrok was not found.")
      print("Downloading ngrok for MacOS from website...")
      set_ngrok = subprocess.Popen(
        ["wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip" \
         "&& unzip ngrok-stable-darwin-amd64.zip"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      while set_ngrok.poll() is None:
        continue
      check_ngrok = subprocess.Popen(["ls -al ./ | grep ngrok"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      check_ngrok = check_ngrok.stdout.read().decode("utf-8")
      if "x" in check_ngrok:
        print(
          "ngrok was successfully downloaded to current folder")
        return True
      else:
        print("Something went wrong!")
        return False


def send_webex_get(url, payload=None, js=True):

  if payload == None:
    request = requests.get(url, headers=headers)
  else:
    request = requests.get(url, headers=headers, params=payload)
  if js == True:
    request = request.json()
  return request


def send_webex_post(url, data, js=True):

  request = requests.post(url, json.dumps(data), headers=headers)
  if js:
    request = request.json()
  return request


def send_webex_delete(url, js=False):

  request = requests.delete(url, headers=headers)
  if js != False:
    request = request.json()
  return request


def send_webex_put(url, data, js=False):

  request = requests.put(url, data=json.dumps(data), headers=headers)
  if js:
    request = request.json()
  return request


def help_me():

  return "Sure! I can help. Below are the commands that I understand:<br/>" \
    "`/joke` - I will tell you a Chuck Norris joke.<br/>" \
    "`/movie_quote` - I will give you a quote of the day from a movie<br/>" \


def greetings():

  return "Hi my name is %s.<br/>" \
    "Type `/help` to see what I can do.<br/>" % bot_name


def handle_text(cmd, filename=None):
  result = None

  if '/joke' in cmd:
    result = requests.get(url="http://api.icndb.com/jokes/random/").json()["value"]["joke"]

  elif '/movie_quote' in cmd:
    result = requests.get(url="http://quotes.rest/qod.json").json()["contents"]["quotes"][0]["quote"]
  elif  '/help' in cmd:
    result = help_me()
  if result == None:
    result = "I did not understand your request. Please type `/help` to see what I can do"
  return result

def webhook():

  url = URL + "/webhooks"
  webhooks = {}
  resources = ["messages", "memberships"]
  webhook_name = "Webhook for demo"
  event = "created"
  status = None
  name = "Webhook Demo"
  target_url = ""

  ngrok_url = requests.get(
    "http://127.0.0.1:4040/api/tunnels", headers={"Content-Type": "application/json"}).json()
  for urls in ngrok_url["tunnels"]:
    if "https://" in urls['public_url']:
      target_url = urls['public_url']

  check_webhook = send_webex_get(url, js=False)
  if check_webhook.ok:
    check_webhook = check_webhook.json()
    if len(check_webhook["items"]) > 0:
      for items in check_webhook["items"]:
        webhooks[items["id"]] = [items["id"], items["resource"], items["filter"]]
  if len(webhooks) == 0:
    for resource in resources:
      payload = {"name": name, "targetUrl": target_url,
             "resource": resource, "event": "created", "filter" : "personEmail="+EMAIL}
      webhook = send_webex_post(url, payload, js=False)
      if webhook.ok:
        status = True
        print("Webhook was successfully created")
      else:
        status = False
        print(
          "Something went wrong. I was unable to create the webhook")
  else:
    for webhook_id in webhooks:
      for item in webhooks[webhook_id]:
        if EMAIL in item:
          send_webex_delete(url+"/"+webhook_id)
          print("Webhook was removed")
    for resource in resources:
      payload = {"name": name, "targetUrl": target_url,
         "resource": resource, "event": "created", "filter" : "personEmail="+EMAIL}
      webhook=send_webex_post(url, payload, js=False)
      if webhook.ok:
        status = True
        print("Webhook was successfully created")
  return status



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def webex_webhook():
  if request.method == 'POST':
    webhook = request.get_json(silent=True)
    resource = webhook['resource']
    senders_email = webhook['data']['personEmail']
    room_id = webhook['data']['roomId']

    msg = None
    if senders_email != bot_email:
      result = send_webex_get(
        URL + '/messages/{0}'.format(webhook['data']['id']))
      in_message = result.get('text', '')
      try:
        in_message = in_message.replace(bot_name.split(" ")[0] + " ", "")
      except:
        in_message = in_message.replace(bot_name.lower() + " ", '')
      msg = handle_text(in_message)
      if msg != None:
        send_webex_post(URL + "/messages",
                {"roomId": room_id, "markdown": msg})
    return "true"
  elif request.method == 'GET':
    message = "<center><img src=\"http://bit.ly/SparkBot-512x512\" alt=\"Webex Teams Bot\" style=\"width:256; height:256;\"</center>" \
      "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
      "<center><b><i>Please don't forget to create Webhooks to start receiving events from Webex Teams!</i></b></center>" % bot_name
    return message


def main():
  global bot_email, bot_name
  if len(bearer) != 0:
    test_auth = send_webex_get(URL + "/people/me", js=False)
    if test_auth.status_code == 401:
      print("Looks like provided access token is not correct. \n"
          "Please review it and make sure it belongs to your bot account.\n"
          "Do not worry if you have lost the access token. "
          "You can always go to https://developer.webex.com/apps.html "
          "URL and generate a new access token.")
      sys.exit()
    if test_auth.status_code == 200:
      test_auth = test_auth.json()
      bot_name = test_auth.get("displayName", "")
      bot_email = test_auth.get("emails", "")[0]
  else:
    print("'bearer' variable is empty! \n"
        "Please populate it with bot's access token and run the script again.\n"
        "Do not worry if you have lost the access token. "
        "You can always go to https://developer.webex.com/apps.html "
        "URL and generate a new access token.")
    sys.exit()

  if ("@sparkbot.io" or "@webex.bot") not in bot_email:
    print("You have provided access token which does not belong to your bot.\n"
        "Please review it and make sure it belongs to your bot account.\n"
        "Do not worry if you have lost the access token. "
        "You can always go to https://developer.webex.com/apps.html "
        "URL and generate a new access token.")
    sys.exit()
  else:
    app.run(host='localhost', port=8080)

if __name__ == "__main__":
  if ngrok():
    if platform.system() != "Windows":
      ngrok_run = subprocess.Popen(
        ["./ngrok http 8080"], shell=True,
         stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
           universal_newlines=True)
      print("Waiting for ngrok to come up ...")
      time.sleep(2)
      print("Success! Ngrok is up")
      if webhook():
        main()
    elif platform.system() == "Windows":
      ngrok_run = os.popen("ngrok http 8080", mode='r', buffering=-1)
      print("Waiting for ngrok to come up ...")
      time.sleep(2)
      print("Success! Ngrok is up")
      if webhook():
        main()