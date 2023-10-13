from twilio.rest import Client
import os




# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def send_sms(user_code, phone):
     message = client.messages \
                .create(
                     body=f"Hi! Your email and verification code is {user_code}.",
                     from_='+14846737900',
                     to=f'{phone}')
     print(message.sid)

