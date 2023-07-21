import json
import logging
import requests
from steam.client import SteamClient
from steam.enums import EResult
from steam.enums.emsg import EMsg
from steam.utils.proto import proto_to_dict
from steam.steamid import SteamID
from steam.webapi import WebAPI

try:
	with open("config.json", 'r') as config_file: config = json.load(config_file)
except:
	print("Failed to open config.json")
	exit()

logging.basicConfig(format="%(asctime)s | %(message)s", level=logging.INFO)
LOG = logging.getLogger()
api = WebAPI(config['apikey'])
client = SteamClient()

#disabled until auth is fixed
#client.set_credential_location(".")

@client.on("error")
def handle_error(result):
    LOG.info("Logon result: %s", repr(result))
#disabled until auth is fixed
"""
if not client.relogin_available:
	client.wait_event(client.EVENT_NEW_LOGIN_KEY, timeout=10)
	client.wait_event(EMsg.ClientNewLoginKey,timeout=10)
	relogin_credentials = client.username, client.login_key
	print(relogin_credentials)
"""

for account in config['accounts']:
	LOG.info("On account: %s", account['username'])
	client.cli_login(username=account['username'],password=account['password'])
	sessions_req=client.send_um_and_wait("FriendMessages.GetActiveMessageSessions#1")
	sessions_dict=proto_to_dict(sessions_req.body)
	total_chats = 0
	total_messages = 0
	if 'manage_sessions' in sessions_dict:
		account_ids = [session['accountid_friend'] for session in sessions_dict['message_sessions'] if session['last_message']>account['timestamp']]
		for account_id in account_ids:
			total_chats+=1
			sender_info = api.call('ISteamUser.GetPlayerSummaries', steamids=str(SteamID(account_id).as_64))
			sender_name = sender_info['response']['players'][0]['personaname']
			sender_avatar = sender_info['response']['players'][0]['avatar']
			recent_messages_req=client.send_um_and_wait("FriendMessages.GetRecentMessages#1", {'steamid1':client.steam_id.as_64,'steamid2':SteamID(account_id).as_64})
			recent_messages_dict=proto_to_dict(recent_messages_req.body)
			for message in recent_messages_dict['messages'][::-1]:
				if (message['timestamp']>account['timestamp']) and (message['accountid']!=client.steam_id.id):
					total_messages+=1
					requests.post(config['webhook'], json={"content": message['message'], "username": f"{sender_name} ({account['username']})","avatar_url":sender_avatar})
	LOG.info("Account %s had: %d friend requests and %d messages across %d chats", account['username'], len([x for x in client.friends if x.relationship==2]), total_messages, total_chats)
	account['timestamp']=sessions_dict['timestamp']
	try:
		with open("config.json", 'w') as config_file: json.dump(config,config_file,indent=2)
	except:
		print("Failed to save config.json")
	client.logout()
