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
from virl import start_sim
from virl import stop_sim
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




## Define logging parameters
#log = logging.getLogger('VIRL')
## change this to logging.ERROR for silence
#log.setLevel(logging.DEBUG)
#FORMAT = '%(asctime)s %(funcName)s(): %(message)s'
#logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

# Define global parameters
print('Setting global parameters.')
URL = "https://api.ciscospark.com/v1"
# BOT'S ACCESS TOKEN
bearer = "Zjk4Yjk0NWItZDZlMC00ZTJlLWIzZDYtMTA3YzBkMTc5MDBiOGNmNjNkNGQtNDI0"
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


def send_spark_get(url, payload=None, js=True):

  if payload == None:
    request = requests.get(url, headers=headers)
  else:
    request = requests.get(url, headers=headers, params=payload)
  if js == True:
    request = request.json()
  return request


def send_spark_post(url, data, js=True):

  request = requests.post(url, json.dumps(data), headers=headers)
  if js:
    request = request.json()
  return request


def send_spark_delete(url, js=False):

  request = requests.delete(url, headers=headers)
  if js != False:
    request = request.json()
  return request


def send_spark_put(url, data, js=False):

  request = requests.put(url, data=json.dumps(data), headers=headers)
  if js:
    request = request.json()
  return request


def help_me():

  return "Sure! I can help. Below are the commands that I understand:<br/>" \
    "`Run [attached file]` - I will run attached virl file.<br/>" \
    "`Start [simulation file name]` - I will start specified simulation<br/>" \
    "`Stop [simulation id]` - I will stop simulation with specified ID<br/>" \
    "`List` - I will provide a list of VIRL files present on local HDD<br/>" \
    "`Check VIRL` - I will check VIRL and see if any simulations are running<br/>"


def greetings():

  return "Hi my name is %s.<br/>" \
    "Type `Help me` to see what I can do.<br/>" % bot_name


def handle_text(text, filename=None):
  result = None
  if text.lower().startswith('hello'):
    result = greetings()
  if text.lower().startswith('help me'):
    result = help_me()
  if text.lower().startswith('run') and not filename:
    result = "Please don't forget to upload a VIRL file with your `run` command"
  elif text.lower().startswith('run') and not filename.endswith(".virl"):
    result = "I can't run a non VIRL file. Type `Help Me` to see what I can do"
  elif text.lower().startswith('run') and filename.endswith(".virl"):
    sim_id = start_sim(filename)
    if sim_id[0]:
      result = ("Simulation `%s` was successfully started.<br/>"\
        "To access your simulation navigate to [http://198.18.134.1:19400/simulation/guest/%s/](http://198.18.134.1:19400/simulation/guest/%s/) URL</br>"\
        "Live visualization is accessible via [http://198.18.134.1:19402/?sim_id=%s](http://198.18.134.1:19402/?sim_id=%s) URL" % (sim_id[1],sim_id[1],sim_id[1],sim_id[1],sim_id[1]))
    else:
      result = ("Something went wrong while I was trying to start the simulation.<br/>" \
        "VIRL returned %s error code.<br/>Also, VIRL provided a reason which is <br/>**%s**" % (response[1], response[2]))
  if text.lower().startswith('stop') and len(text) > 5:
    response = stop_sim(text.split(" ")[1])
    if response:
      result = "The simulation was successfully stopped!"
    else:
      result = "Something went wrong while I was trying to stop a simulation.\n" \
        "Please make sure provided simulation ID is correct!"
  if text.lower().startswith('start') and len(text) > 6:
    response = start_sim(text.split(" ")[1])
    if response[0]:
      result = ("Simulation `%s` was successfully started.<br/>"\
        "To access your simulation navigate to [http://198.18.134.1:19400/simulation/guest/%s/](http://198.18.134.1:19400/simulation/guest/%s/) URL</br>"\
        "Live visualization is accessible via [http://198.18.134.1:19402/?sim_id=%s](http://198.18.134.1:19402/?sim_id=%s) URL" % (response[1],response[1],response[1],response[1],response[1]))
    else:
      result = ("Something went wrong while I was trying to start the simulation.<br/>" \
        "VIRL returned %s error code.<br/>Also, VIRL provided a reason which is <br/>**%s**" % (response[1], response[2]))
  if text.lower().startswith('list'):
    result = virl_files()
  if text.lower().startswith('check virl'):
    result = check_virl()
  if result == None:
    result = "I did not understand your request. Please type `Help me` to see what I can do"
  return result


def get_files(file_urls, room_id):

  for file_url in file_urls:
    response = send_spark_get(file_url, js=False)
    content_disp = response.headers.get('Content-Disposition', None)
    if content_disp is not None:
      filename = content_disp.split("filename=")[1].replace('"', '')
    if filename.endswith('.virl'):
      with open("./sims/" + filename, 'wb') as f:
        f.write(response.content)
        send_spark_post(URL + "/messages",
                {"roomId": room_id, "markdown": ' Received and saved - ' + filename})
        return filename
    else:
      send_spark_post(URL + "/messages",
              {"roomId": room_id, "markdown": '**Sorry but I only accept VIRL files**'})


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

  check_webhook = send_spark_get(url, js=False)
  if check_webhook.ok:
    check_webhook = check_webhook.json()
    if len(check_webhook["items"]) > 0:
      for items in check_webhook["items"]:
        webhooks[items["id"]] = [items["id"], items["resource"], items["filter"]]
  if len(webhooks) == 0:
    for resource in resources:
      payload = {"name": name, "targetUrl": target_url,
             "resource": resource, "event": "created", "filter" : "personEmail="+EMAIL}
      webhook = send_spark_post(url, payload, js=False)
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
          send_spark_delete(url+"/"+webhook_id)
          print("Webhook was removed")
    for resource in resources:
      payload = {"name": name, "targetUrl": target_url,
         "resource": resource, "event": "created", "filter" : "personEmail="+EMAIL}
      webhook=send_spark_post(url, payload, js=False)
      if webhook.ok:
        status = True
        print("Webhook was successfully created")
  return status


def virl_files():

  contents = ""
  num = 0
  file_name = None
  for file in os.listdir("./sims/"):
    if file.endswith(".virl"):
      num += 1
      contents += str(num) + ". " + str(file) + "<br/>"
      if file_name == None:
        file_name = file
  if num == 0:
    return "**No VIRL files are present on local HDD.<br/>" \
      "Use `run` command to upload a file and run it."
  return "**Found " + str(num) + " VIRL file(s) on local HDD**.<br/>" + contents + \
    "> **Note:** You can say `start " + file_name + \
    "` and I will start the simulation for you."

def check_virl():

  # Combine the url and the API call
  URL = "http://198.18.134.1:19399/simengine/rest/list"

  headers = {'content-type': 'text/xml'}

  # Make a request call with method get to the VIRL server
  response = requests.get(
    URL, auth=("guest", "guest"), headers=headers).json()

  # Print how many active simulations were found.
  if len(response["simulations"]) == 0:
    message = "There are no running simulations on VIRL"
    return message
  else:
    message = ("**VIRL reports " +
      str(len(response["simulations"])) + " active simulation(s).**<br/>")
    sim_name = None
    # Iterate over the response and print each simulation to the user.
    # If user recognizes the simulation return it.
    for i, sim in enumerate(response["simulations"]):
      if not sim_name:
        sim_name = sim
      message += str(i+1) + ". "+ sim + "<br/>"
    message += "> **Note:** You can say `stop " + sim_name + "` and I will stop the simulation for you."
  return message


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def spark_webhook():
  if request.method == 'POST':
    webhook = request.get_json(silent=True)
    resource = webhook['resource']
    senders_email = webhook['data']['personEmail']
    room_id = webhook['data']['roomId']

    if senders_email != bot_email:
      pprint(webhook)
    if resource == "memberships" and senders_email == bot_email:
      send_spark_post(URL + "/messages",
              {
                "roomId": room_id,
                "markdown": (greetings() +
                       "**Note This is a group room and you have to call "
                       "me specifically with `@%s` for me to respond**" % bot_name)
              }
              )

    msg = None
    filename = None
    if senders_email != bot_email:
      if "files" in webhook['data']:
        filename = get_files(webhook['data']['files'], room_id)
      result = send_spark_get(
        URL + '/messages/{0}'.format(webhook['data']['id']))
      in_message = result.get('text', '')
      print("Received " + in_message + " from spark. Processing...")
      try:
        in_message = in_message.replace(bot_name.split(" ")[0] + " ", "")
      except:
        in_message = in_message.replace(bot_name.lower() + " ", '')
      if filename != None:
        msg = handle_text(in_message, filename=filename)
      else:
        msg = handle_text(in_message)
      if msg != None:
        send_spark_post(URL + "/messages",
                {"roomId": room_id, "markdown": msg})
    return "true"
  elif request.method == 'GET':
    message = "<center><img src=\"http://bit.ly/SparkBot-512x512\" alt=\"Spark Bot\" style=\"width:256; height:256;\"</center>" \
      "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
      "<center><b><i>Please don't forget to create Webhooks to start receiving events from Cisco Spark!</i></b></center>" % bot_name
    return message


def main():
  global bot_email, bot_name
  if len(bearer) != 0:
    test_auth = send_spark_get(URL + "/people/me", js=False)
    if test_auth.status_code == 401:
      print("Looks like provided access token is not correct. \n"
          "Please review it and make sure it belongs to your bot account.\n"
          "Do not worry if you have lost the access token. "
          "You can always go to https://developer.ciscospark.com/apps.html "
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
        "You can always go to https://developer.ciscospark.com/apps.html "
        "URL and generate a new access token.")
    sys.exit()

  if "@sparkbot.io" not in bot_email:
    print("You have provided access token which does not belong to your bot.\n"
        "Please review it and make sure it belongs to your bot account.\n"
        "Do not worry if you have lost the access token. "
        "You can always go to https://developer.ciscospark.com/apps.html "
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