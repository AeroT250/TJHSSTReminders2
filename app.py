#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import os 
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    
dayofweek = datetime.datetime.today().weekday()
   if(dayofweek == 1):
       return "Hi! Thanks for checking in. Today is Tuesday, a blue day. This means that you have periods" \
              "1, 2, 3, and 4, with a break between periods 2 and 3. You don't have to fill out any special" \
              "form today. Here are the times when each class starts: 1st pd is from 8:40 AM - 10:05 AM. 2nd period" \
              "is from 10:25 - 11:50. You have a lunch break from 12:00 PM - 12:40 PM. Pd 3 is from 12:50 PM" \
              "- 2:15 PM. Finally, your last class of the day, pd 4, is from 2:35 PM - 4:00 PM. Have a great day!"
   if(dayofweek == 2):
       return "Hi! Thanks for checking in. Today is Wednesday, a red day. This means that you have periods" \
              "5, 6, 7, and 8 (Clubs!), with a break between periods 6 and 7. You don't need to fill out any " \
              "forms today. Here are the times for each class: 1st pd is from 8:40 AM - 10:05 AM. 2nd period" \
              "is from 10:25 - 11:50. You have a lunch break from 12:00 PM - 12:40 PM. Pd 3 is from 12:50 PM" \
              "- 2:15 PM. Then, the first 8th period block is from 2:30 PM - 3:10 PM. To end the day, we have " \
              "8th period B block, from 3:20 PM - 4:00 PM. Have an amazing day! "
   if(dayofweek == 3):
       return "Hi! Thanks for checking in. Today is Thursday, a blue day. This means that you have periods" \
              "1, 2, 3, and 4, with a break between periods 2 and 3. You don't have to fill out any special" \
              "form today. Here are the times when each class starts: 1st pd is from 8:40 AM - 10:05 AM. 2nd period" \
              "is from 10:25 - 11:50. You have a lunch break from 12:00 PM - 12:40 PM. Pd 3 is from 12:50 PM" \
              "- 2:15 PM. Finally, your last class of the day, pd 4, is from 2:35 PM - 4:00 PM. Have a great day!"
   if(dayofweek == 4):
       return "Hi! Thanks for checking in. Today is Wednesday, a red day. This means that you have periods" \
              "5, 6, 7, and 8 (Clubs!), with a break between periods 6 and 7. You don't need to fill out any " \
              "forms today. Here are the times for each class: 1st pd is from 8:40 AM - 10:05 AM. 2nd period" \
              "is from 10:25 - 11:50. You have a lunch break from 12:00 PM - 12:40 PM. Pd 3 is from 12:50 PM" \
              "- 2:15 PM. Then, the first 8th period block is from 2:30 PM - 3:10 PM. To end the day, we have " \
              "8th period B block, from 3:20 PM - 4:00 PM. Have an amazing day! "
   if(dayofweek == 5):
       return "It's the weekend (Saturday)! Time to relax, read a book, play with a pet, or let's be honest, spend 8 hours a " \
              "day doing homework. Make sure to schedule your time to include plenty of breaks, and if you have time," \
              "be sure to take a day off just to relax. See you next week!"
   if (dayofweek == 6):
       return "It's the weekend (Sunday)! Time to relax, read a book, play with a pet, or let's be honest, spend 8 hours a " \
              "day doing homework. Make sure to schedule your time to include plenty of breaks, and if you have time," \
              "be sure to take a day off just to relax. See you next week!"
   if(dayofweek == 0):
       return "Oh boy: it's monday. At least we have a 3 day weekend! Today is pretty much like Saturday or Sunday, but" \
              "be sure to fill out the Monday Attendance Form so you don't get marked as absent. " \
              "Here's the link: https://tinyurl.com/monday-check-in-2020"



#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
