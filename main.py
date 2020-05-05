import requests
from twilio.rest import Client

# Twitch API documentation https://dev.twitch.tv/docs
# version used: v5
endpoint = "https://api.twitch.tv/helix/streams/"
headers = {"Client-ID": "<twitch client id>"}
params = {"user_login": "<twitch user to follow>"}

response = requests.get(endpoint, params=params, headers=headers)
json_response = response.json()
streams = json_response.get('data')

# # test if streamer is live or not 
is_active = lambda stream: stream.get('type') == 'live'
streams_active = filter(is_active, streams)
at_least_one_active = (any(streams_active))
# print(at_least_one_active)

twilio_acc_sid = "<twilio acccount sid>"
twilio_auth_token = "<twilio auth token>"
twilio_number = "<number to send notification to>"
my_number = "<twilio test number>"

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