import os
import time
import unicodedata    
import random
import pymysql
from slackclient import SlackClient
from PyDictionary import PyDictionary
dictionary=PyDictionary()



db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="kc",
                     db="chatbot")


cur = db.cursor()



# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


z= ['professor','assistant','lecturer','fellow','tutor']
final1=[]

for i in z:
 list1=dictionary.synonym(i)
 list1 = [str(i).strip() for i in list1]

 final1.append(list1)





def handle_command(command, channel):
			if command in final1[0] or command in final1[1] or final1[2] or command in final1[3]  or command in final1[4] :
				cur.execute("SELECT * FROM solutions where questions like '%teacher%'")
				for row in cur.fetchall():
					response = row[1]
			else:
				response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
                   "* command with numbers, delimited by spaces."
			slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
