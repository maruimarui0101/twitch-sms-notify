import requests
from twilio.rest import Client

import os 
from dotenv import load_dotenv

load_dotenv()

# https://discuss.dev.twitch.tv/t/oauth-token-is-missing/27612

AutParams = {'client_id': f"{os.getenv('TWITCH_CLIENT_ID')}"
, 'client_secret': f"{os.getenv('TWITCH_SECRET')}"
, 'grant_type': 'client_credentials'}

AutURL ="https://id.twitch.tv/oauth2/token"
AutCall = requests.post(url=AutURL, params=AutParams)

data1 = AutCall.json()
access_token = data1['access_token']
print(access_token)

# Twitch API documentation https://dev.twitch.tv/docs
# version used: v5
endpoint = "https://api.twitch.tv/helix/streams?"
headers = {"Client-Id": f"{os.getenv('TWITCH_CLIENT_ID')}",
"Authorization": f"Bearer {access_token}"}
params = {"user_login": f"{os.getenv('FOLLOW_TWITCH_ID')}"}

response = requests.get(endpoint, params=params, headers=headers)
json_response = response.json()
print(json_response)
streams = json_response.get('data')

# # test if streamer is live or not 
is_active = lambda stream: stream.get('type') == 'live'
streams_active = filter(is_active, streams)
at_least_one_active = (any(streams_active))
# print(at_least_one_active)

twilio_acc_sid = f"{os.getenv('TWILIO_SID')}"
twilio_auth_token = f"{os.getenv('TWILIO_AUTH_TOKEN')}"
twilio_number = f"{os.getenv('TWILIO_NUMBER')}"
my_number = f"{os.getenv('SEND_TO')}"

client = Client(twilio_acc_sid, twilio_auth_token)
last_messages_sent = client.messages.list(limit=1)


if last_messages_sent:
    last_message_id = last_messages_sent[0].sid
    last_message_data = client.messages(last_message_id).fetch()    
    last_message_content = last_message_data.body
    online_notified = "LIVE" in last_message_content
    offline_notified = not online_notified
else:
    	online_notified, offline_notified = False, False


if at_least_one_active and not online_notified:
    	client.messages.create(body='LIVE !!!',from_=twilio_number,to=my_number)
if not at_least_one_active and not offline_notified:
	client.messages.create(body='OFFLINE !!!',from_=twilio_number,to=my_number)