#!/bin/env python3
# VK, Telegram messages synchronization implementation.
# Every bot polls the events of messages and sends 'em to the rest of bots.

# VK API
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType

# Telegram API
import telebot

import threading
import json

class ConvSyncBot:
	# Basic class for chat bots in conversations.
	def __init__(self, config, other_bots):
		print("Initializing API.")
	def send_text(self, username, text):
		# The function to send just text messages in general chats
		# of other bots.
		print("Sending '%s' from '%s'." % (text, username))
	def run(self):
		# The function that is supposed to be threaded.
		print("Conversation syncing bot is running.")

class VKConvSyncBot(ConvSyncBot):
	def __init__(self, config):
		self.vk_token = config["vk_token"]
		self.vk_group_id = int(config["vk_group_id"])
		self.vk_server = config["vk_server"]
		self.vk_key = config["vk_key"]
		self.vk_ts = config["vk_ts"]
		self.chat_ids = config["vk_chat_ids"]
		
		# Ininialization.
		self.vk_session = vk_api.VkApi(token=self.vk_token)
		self.vk_longpoll = VkBotLongPoll(self.vk_session, self.vk_group_id)
		self.vk = self.vk_session.get_api()

	def send_text(self, username, text):
		for chat_id in self.chat_ids :
			self.vk.messages.send(
				vk_key=self.vk_key, vk_server=self.vk_server, vk_ts=self.vk_ts,
				random_id=vk_api.utils.get_random_id(),
				message=("%s : %s")%(username, text),
				chat_id=chat_id
			)
	def run(self):
		for ev in self.vk_longpoll.listen() :
			if not ev.chat_id in self.chat_ids :
				return
			if ev.type==VkBotEventType.MESSAGE_NEW and ev.from_chat :
				print(ev)
				from_id = ev.object.message['from_id']
				user = self.vk.users.get(user_ids=from_id)
				print(user)
				username = ("%s %s" 
				% (user[0]['first_name'], 
					user[0]['last_name'])
				)
				print(username)
				for bot in self.other_bots :
					bot.send_text(username, ev.object["message"]["text"])
		
class TelegramConvSyncBot(ConvSyncBot):
	def __init__(self, config):
		self.t_token = config["t_token"]
		self.chat_ids = config["t_chat_ids"]
		self.t = telebot.TeleBot(self.t_token)

	def send_text(self, username, text):
		for chat_id in self.chat_ids :
			self.t.send_message(chat_id, text="%s : %s" % (username, text))

	def run(self):
		@self.t.message_handler(content_types=['text'])
		def on_text_message(message):
			if not message.chat.id in self.chat_ids :
				return
			username="%s %s" % (message.from_user.first_name, message.from_user.last_name)
			for bot in self.other_bots :
				bot.send_text(username, message.text)
		self.t.polling()
		
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
	for bot in bots :
		thread = threading.Thread(target=bot.run, args=())
		thread.start()

if __name__ == "__main__" :
	main()

