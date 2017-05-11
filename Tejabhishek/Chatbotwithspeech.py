import os
import time
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import unicodedata    
import random
import MySQLdb
from slackclient import SlackClient
from PyDictionary import PyDictionary
import speech_recognition
dictionary=PyDictionary()



db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="abhishek",
                     db="chatbot")


cur = db.cursor()



# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

cur.execute("SELECT * FROM solutions where questions like '%teacher%'")
for row in cur.fetchall():
	m = row[0]
"""mentor info"""

z= ['professor','assistant','lecturer','tutor']
final1=[]

for i in z:
 list1=dictionary.synonym(i)
 list1 = [str(i).strip() for i in list1]

 final1.append(list1)
 
 """Greetings info"""
greetings= [ 'hi', 'hi there', 'hey', 'how are you', 'whats up?', 'greetings','good evening', 'goodday', 'hello']

#subject details

office=['location','office']

meeting=['hours', 'meeting']

locationtime=['class timings','lecture hall']

course=['website',' link']
department=['department','division']


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


def handle_command(command, channel):

	for i in greetings:
		
		if i==command:
			#print i
			cur.execute("SELECT * FROM solutions where questions like '%hey%'")
			for row in cur.fetchall():
					response = row[1]
		else:
			response = ""
		slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)
	for i in final1:
		#print i
		for j in i:
			if j in command:
				cur.execute("SELECT * FROM solutions where questions like '%teacher%'")
				for row in cur.fetchall():
					response = row[1]
			else:
				response = ""
			slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)
	if 'course' in command or 'description' in command:
		cur.execute("SELECT * FROM solutions where questions like '%coursedescription%'")
		for row in cur.fetchall():
			response = row[1]
	else:
		response = ""
	slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)
		

	if 'subject'==command:
		#print i
		cur.execute("SELECT * FROM solutions where questions like '%subject%'")
		for row in cur.fetchall():
			response = row[1]
	else:
		response = ""
	slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)
	for i in office:
		if i in command:
			#print i
			cur.execute("SELECT * FROM solutions where questions like '%office%'")
			for row in cur.fetchall():
					response = row[1]
		else:
			response = ""
		slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)
	if 'mail' in command:
		#print i
		cur.execute("SELECT * FROM solutions where questions like '%mail%'")
		for row in cur.fetchall():
			response = row[1]
	else:
		response = ""
	slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)

	for i in meeting:
		if i in command:
			#print i
			cur.execute("SELECT * FROM solutions where questions like '%hours%'")
			for row in cur.fetchall():
					response = row[1]
		else:
			response = ""
		slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)

	for i in locationtime:
		if i in command:
			#print i
			cur.execute("SELECT * FROM solutions where questions like '%class timings%'")
			for row in cur.fetchall():
					response = row[1]
		else:
			response = ""
		slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)

	for i in course:
		if i in command:
			#print i
			cur.execute("SELECT * FROM solutions where questions like '%website%'")
			for row in cur.fetchall():
					response = row[1]
		else:
			response = ""
		slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)
	for i in department:
		if i in command:
			#print i
			cur.execute("SELECT * FROM solutions where questions like '%department%'")
			for row in cur.fetchall():
					response = row[1]
		else:
			response = ""
		slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)

if __name__ == "__main__":

    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        import speech_recognition as sr
        print("StarterBot connected and running!")
        while True:
            # obtain audio from the microphone
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)
            try:
                command, channel = r.recognize_google(audio)

            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

