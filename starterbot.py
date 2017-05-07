import os
import time
import pymysql
from slackclient import SlackClient

db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="kc",
                     db="kiran")


cur = db.cursor()



# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))



def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    
    
    if "teacher" in command:
       
        cur.execute("SELECT * FROM grammar1 where keyword = 'teacher'")
        for row in cur.fetchall():
            response = row[1]
    elif "lecturer" in command:
       
        cur.execute("SELECT * FROM grammar1 where keyword = 'lecturer'")
        for row in cur.fetchall():
        	response = row[1]
        
    elif "professor" in command:
       
        cur.execute("SELECT * FROM grammar1 where keyword = 'professor'")
        for row in cur.fetchall():
        	response = row[1]
    elif "guide" in command:
       
        cur.execute("SELECT * FROM grammar1 where keyword = 'guide'")
        for row in cur.fetchall():
        	response = row[1]
    elif (command == "hi"):
        response = "Hi!!  How are you!!"
    
    elif (command == "i am good"):
        response = "Cheers!!  How can I help you"
    elif (command == "how are you"):
        response = "I am fine! How can I help you"
    else:
        print("feefeg")
        response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
                   "* command with numbers, delimited by spaces."
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


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
