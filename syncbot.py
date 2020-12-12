#!/bin/env python3
# VK, Telegram messages synchronization implementation.
# Every bot polls the events of messages and sends 'em to the rest of bots.

# VK API
import vk_api, vk, json
from vk_api.vk_keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType

# Telegram API
import telebot

class ConvSyncBot:
	# Basic class for chat bots in conversations.
	def __init__(self, config, other_bots):
		print("Initializing API.")
	def send_text(self, text):
		# The function to send just text messages in general chats
		# of other bots.
		print("Sending '%s'." % (text))
	def run(self):
		# The function that is supposed to be threaded.
		print("Conversation bot is running.")

class VKConvSyncBot(ConvSyncBot)
	def __init__(self, config):
		self.vk_token = config["vk_token"]
		self.vk_group_id = int(config["vk_group_id"])
		self.vk_server = config["vk_server"]
		self.vk_key = config["vk_key"]
		self.vk_ts = config["vk_ts"]
		self.chat_ids = config["vk_chat_ids"]
		
		# Ininialization.
		self.vk_session = vk_api.VkApi(vk_token=self.vk_token)
		self.vk = self.vk_session.get_api()
		self.vk_longpoll = VkBotLongPoll(vk_session, vk_group_id)
		
		self.other_bots = []


	def send_text(self, text):
		for chat_id in chat_ids :
			self.vk.messages.send(
				vk_key=self.vk_key, vk_server=vk_server, vk_ts=self.vk_ts,
				random_id=get_random_id(), message=text, chat_id=chat_id
			)
		
class TelegramConvSyncBot(ConvAPI)
	def __init__(self, config):
		self.t_token = config["t_token"]
		self.chat_ids = config["t_chat_ids"]
		self.t = telebot.TeleBot(t_token)
		self.other_bots = []
	

	def send_text(self, text):
		for chat_id in chat_ids :
			self.t.send_message(chat_id, text=text)

	def run(self):
		

msg.chat.id

@t_bot.message_handler(content_types['text'])
def get_text_messages(msg):
    t_bot.send_message(msg.chat.id, text=resptext)

def handle_VK_events():
    for event in longpoll.listen() :
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat :
        	for bot in other_bots :
	        	bot.send_text(text)
            vk.messages.send(vk_key=vk_key, vk_server=vk_server, vk_ts=vk_ts, random_id=get_random_id(),
                message='Yes, it works. Stop typing.', chat_id = event.chat_id)
def main():
	config_path = "config.json"
	with open(config_path, "r") as read_file :
	    config = json.load(read_file)
	bots = []
	vk_bot = VKConvSyncBot(config)
	telegram_bot = TelegramConvSyncBot(config)
	vk_bot.other_bots = [telegram_bot]
	telegram_bot.other_bots = [vk_bot]
	bots = [vk_bot, telegram_bot]
	# Threading.
	for bot in bots :
		

if __name__ == "__main__" :
	main()

