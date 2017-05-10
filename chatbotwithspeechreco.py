import os
import time
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


z= ['professor','assistant','lecturer','tutor']
final1=[]

for i in z:
 list1=dictionary.synonym(i)
 list1 = [str(i).strip() for i in list1]

 final1.append(list1)





def handle_command(command, channel):
	print final1
	for i in final1:
		print i
		for j in i:
			if j in command:
				print j
				if command in final1[0] or command in final1[1] or final1[2] or command in final1[3]  or command in final1[4] :
					cur.execute("SELECT * FROM solutions where questions like '%teacher%'")
					for row in cur.fetchall():
						response = row[1]
						
						
				else:
					response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
                   "* command with numbers, delimited by spaces."
			else:
				response = ""
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
    import speech_recognition as sr
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            
            # obtain audio from the microphone
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)

            try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    
                command = r.recognize_google(audio)
                print("Google Speech Recognition thinks you said " + command)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
