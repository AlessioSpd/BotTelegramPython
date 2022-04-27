#!/usr/bin/python3
import Constants as keys
from telegram.ext import *
from telegram import *
from datetime import datetime
from pprint import pprint
import random
import re
import bs4, requests, webbrowser
import os

# Main Code
stato = 'IDLE'
fileName = ""
url = "https://www.google.it/search?q=pathToReplace&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjJ8rfZsKj3AhW-k_0HHUtBCwAQ_AUoAXoECAIQAw&biw=639&bih=600&dpr=1.5"
print("Bot started...")

# Ogni funzione svolge il compito di rispondere ad un certo tipo di messaggio
def start_command(update, contex):
	start_text = "Benvenuto, sono un bot in sviluppo, usa il comando /help per sapere cosa posso fare. BuonBot!!"
	# buttons = [[KeyboardButton("ciao")], [KeyboardButton("salve")]]
	contex.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
	contex.bot.send_message(chat_id=update.effective_chat.id, text=start_text)#,
	# reply_markup=ReplyKeyboardMarkup(buttons))
	# update.message.reply_text("Type something to get started)

def help_command(update, contex):
	contex.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
	update.message.reply_text("Digitando /search, svolgerò una ricerca di immagini riferite alla parola/frase che mi darai")

def create_list_command(update, contex):
	global stato
	if stato == 'IDLE':
		contex.bot.send_message(chat_id=update.effective_chat.id, text="Dammi il nome della lista:")
		stato = 'WAITING_NEW_LIST_NAME'
	elif stato == 'WAITING_NEW_LIST_NAME':
		new_name = str(update.message.text).lower()
		new_name = new_name.replace(" ","")
		os.system(f"./fileHandler.pl {keys.CREATE_LIST} {new_name}")
		contex.bot.send_message(chat_id=update.effective_chat.id, text="Lista creata con successo!")
		stato = 'IDLE'

def print_all_list_command(update, contex):
	list_of_file = os.popen(f'./fileHandler.pl {keys.PRINT_LIST}').read()
	list_of_file = list_of_file.split('\n')
	list_of_file.pop()
	
	if len(list_of_file) == 0:
		contex.bot.send_message(chat_id=update.effective_chat.id, text="Non esiste alcuna lista! Usa il comando /create_new_list per crearne una nuova!")
		return;
	else:
		list_of_nameList = "Le tue liste:"
		for name in list_of_file:
			list_of_nameList = list_of_nameList + f"\n- {name}"
		contex.bot.send_message(chat_id=update.effective_chat.id, text=list_of_nameList)
		contex.bot.send_message(chat_id=update.effective_chat.id, text="usa i comandi:\n/add_to_list\n/remove_from_list\n/delete_list\n/print_list\nper modificare o visualizzare una lista a tua scelta!")

def print_list_command(update, contex):
	global stato

	if stato == 'WAITING_LIST_NAME_TO_PRINT':
		path = f"{str(update.message.text)}"
		value_from_file = str(os.popen(f'./fileHandler.pl {keys.READ_FILE} {path}').read())
		values_from_file = value_from_file.split('\n')
		values_from_file.pop()

		if(len(values_from_file) == 0):
			toSend = "Non ci sono ancora elementi all' interno della lista, usa il comando /add_to_list per aggiungere elementi alle tue liste!"
		else:
			toSend = "Gli elementi della lista:"

		for value in values_from_file:
			toSend = toSend + f"\n- {value}"
		contex.bot.send_message(chat_id=update.effective_chat.id, text=toSend)
		stato = 'IDLE'
	else:
		list_of_file = os.popen(f'./fileHandler.pl {keys.PRINT_LIST}').read()
		list_of_file = list_of_file.split('\n')
		list_of_file.pop()

		if len(list_of_file) == 0:
			contex.bot.send_message(chat_id=update.effective_chat.id, text="Non esiste alcuna lista! Usa il comando /create_new_list per crearne una nuova!")
			return;
		else:
			buttons = []
			for name in list_of_file:
				buttons.append([KeyboardButton(str(name))])
			contex.bot.send_message(chat_id=update.effective_chat.id, text="scegli la lista da visualizzare",
			reply_markup=ReplyKeyboardMarkup(buttons))
			stato = 'WAITING_LIST_NAME_TO_PRINT'

def add_to_list_command(update, contex):
	global stato
	global fileName

	if stato == 'WAITING_LIST_NAME_TO_ADD' and update.message.text != '/add_to_list':
		fileName = f'{str(update.message.text)}'
		contex.bot.send_message(chat_id=update.effective_chat.id, text="Scrvi l elemento che vuoi aggiungere alla lista\nNB: ogni messaggio che scriverai sarà contanto come elemento che vuoi aggiungere,\nse vuoi smettere di aggiungere elementi digita /stop_add_item !")
		stato = 'WAITING_ITEM_TO_ADD_IN_LIST'
	elif stato == 'WAITING_ITEM_TO_ADD_IN_LIST':
		os.popen(f"./fileHandler.pl {keys.WRITE_FILE} {fileName} '{str(update.message.text)}'").read()
		contex.bot.send_message(chat_id=update.effective_chat.id, text="elemento aggiunto!")
	else:
		list_of_file = os.popen(f'./fileHandler.pl {keys.PRINT_LIST}').read()
		list_of_file = list_of_file.split('\n')
		list_of_file.pop()

		if len(list_of_file) == 0:
			contex.bot.send_message(chat_id=update.effective_chat.id, text="Non esiste alcuna lista! Usa il comando /create_new_list per crearne una nuova!")
		else:
			buttons = []
			for name in list_of_file:
				buttons.append([KeyboardButton(str(name))])
			contex.bot.send_message(chat_id=update.effective_chat.id, text="scegli la lista alla quale aggiungere un elemento",
			reply_markup=ReplyKeyboardMarkup(buttons))
			stato = 'WAITING_LIST_NAME_TO_ADD'

def remove_from_list_command(update, contex):
	global stato
	global fileName

	if stato == 'WAITING_LIST_NAME_TO_MODIFY' and update.message.text != '/remove_from_list':
		fileName = f'{str(update.message.text)}'
		contex.bot.send_message(chat_id=update.effective_chat.id, text="Scrvi l elemento che vuoi rimuovere dalla lista\nNB: ogni messaggio che scriverai sarà contanto come elemento che vuoi eliminare,\nse vuoi smettere di eliminare elementi digita /stop_remove_item !")
		stato = 'WAITING_ITEM_TO_REMOVE_FROM_LIST'
	elif stato == 'WAITING_ITEM_TO_REMOVE_FROM_LIST':
		result = os.popen(f"./fileHandler.pl {keys.MODIFY_FILE} {fileName} '{str(update.message.text)}'").read()
		if "errore" in result:
			contex.bot.send_message(chat_id=update.effective_chat.id, text="Errore, probabilmente questo elemento non era presente nelle lista!")
		else:
			contex.bot.send_message(chat_id=update.effective_chat.id, text="Elemento rimosso!")
	else:
		list_of_file = os.popen(f'./fileHandler.pl {keys.PRINT_LIST}').read()
		list_of_file = list_of_file.split('\n')
		list_of_file.pop()

		if len(list_of_file) == 0:
			contex.bot.send_message(chat_id=update.effective_chat.id, text="Non esiste alcuna lista! Usa il comando /create_new_list per crearne una nuova!")
			return;
		else:
			buttons = []
			for name in list_of_file:
				buttons.append([KeyboardButton(str(name))])
			contex.bot.send_message(chat_id=update.effective_chat.id, text="scegli la lista da modificare",
			reply_markup=ReplyKeyboardMarkup(buttons))
			stato = 'WAITING_LIST_NAME_TO_MODIFY'

def delete_list_command(update, contex):
	global stato

	if stato == 'WAITING_LIST_NAME_TO_DELETE':
		fileName = f'{str(update.message.text)}'
		result = os.popen(f"./fileHandler.pl {keys.DELETE_LIST} {fileName}").read()
		if "errore" in result:
			contex.bot.send_message(chat_id=update.effective_chat.id, text="Errore, probabilmente questa lista non era presente!")
		else:
			contex.bot.send_message(chat_id=update.effective_chat.id, text="Lista rimossa!")
		stato = 'IDLE'
	else:
		list_of_file = os.popen(f'./fileHandler.pl {keys.PRINT_LIST}').read()
		list_of_file = list_of_file.split('\n')
		list_of_file.pop()

		if len(list_of_file) == 0:
			contex.bot.send_message(chat_id=update.effective_chat.id, text="Non esiste alcuna lista! Usa il comando /create_new_list per crearne una nuova!")
			return;
		else:
			buttons = []
			for name in list_of_file:
				buttons.append([KeyboardButton(str(name))])
			contex.bot.send_message(chat_id=update.effective_chat.id, text="scegli la lista da modificare",
			reply_markup=ReplyKeyboardMarkup(buttons))
			stato = 'WAITING_LIST_NAME_TO_DELETE'

def stop_add_item_command(update, contex):
	global stato
	if stato == 'WAITING_ITEM_TO_ADD_IN_LIST':
		stato = 'IDLE';
		update.message.reply_text("Lista perfettamente aggiornata!\nDigita /print_list per vedere la tua lista!")

def stop_remove_item_command(update, contex):
	global stato
	if stato == 'WAITING_ITEM_TO_REMOVE_FROM_LIST':
		stato = 'IDLE';
		update.message.reply_text("Lista perfettamente aggiornata!\nDigita /print_list per vedere la tua lista!")

def search_command(update, contex):
	global stato
	if stato == 'IDLE':
		contex.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
		contex.bot.send_message(chat_id=update.effective_chat.id, text="Dammi una parola chiave per la ricerca")
		stato = 'WAITING_SEARCHING_KEY'
		return

	user_message = str(update.message.text).lower()

	#creo l url per la ricerca
	semi_path = user_message.replace(" ", "+")
	complete_path = url.replace("pathToReplace", semi_path)
	
	# scarico il sorgente
	res = requests.get(complete_path)
	html_page = bs4.BeautifulSoup(res.text, 'html.parser')
	title = html_page.select('img')

	# cerco i link
	pattern = re.compile(r".*src=\"(.*);")
	rand = random.randint(1,21)

	# invio l immagine
	contex.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
	contex.bot.send_photo(chat_id=update.effective_chat.id, photo=(re.search(pattern, str(title[rand])).group(1)))		
	# contex.bot.sendDocument(chat_id=update.effective_chat.id, document=(re.search(pattern, str(title[rand])).group(1)))
	stato = 'IDLE'

def info_command(update, contex):
	user = update.message.from_user
	print(f'You talk with user {user["username"]} and his user ID: {user["id"]}')
	# print('You talk with user {} and his user ID: {} '.format(user['username'], user['id']))

def random_hentai_command(update, contex):
	url = "https://hanime.tv/browse/random?r="
	res = requests.get(url)

	html = bs4.BeautifulSoup(res.text, 'html.parser')
	a_element = html.find_all("a", {"class":"hvc2 pb-3 flex row wrap justify-left align-left noselect card"})
	pattern = re.compile(r'.*href="/videos/hentai/(.+)" ')
	names = []
	count = 0

	for stringa in a_element:
		names.append(re.search(pattern, str(stringa)).group(1))
	
	rand = random.randint(0,23)
	pre_link_path = "https://hanime.tv/videos/hentai/"
	contex.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
	contex.bot.send_message(chat_id=update.effective_chat.id, text=pre_link_path+names[rand])

# questa funzione rimanda al file Responses che gestisce i messaggi normali (non comandi)
def handle_message(update, contex):
	global stato

	if stato == 'WAITING_SEARCHING_KEY':
		search_command(update, contex)
		return
	elif stato == 'WAITING_NEW_LIST_NAME':
		create_list_command(update, contex)
		return
	elif stato == 'WAITING_LIST_NAME_TO_PRINT':
		print_list_command(update, contex)
		return
	elif stato == 'WAITING_LIST_NAME_TO_ADD' or stato == 'WAITING_ITEM_TO_ADD_IN_LIST':
		add_to_list_command(update, contex)
		return
	elif stato == 'WAITING_LIST_NAME_TO_MODIFY' or stato == 'WAITING_ITEM_TO_REMOVE_FROM_LIST':
		remove_from_list_command(update, contex)
		return
	elif stato == 'WAITING_LIST_NAME_TO_DELETE':
		delete_list_command(update, contex)
		return
	update.message.reply_text("Usa i comandi per usare il bot al meglio!\n/start\n/search")

	# if user_message in ("hello", "hi", "sup"):
	# 	response = "hey! How is it going?"

	# if user_message in ("who are you", "who are you?"):
	# 	response = "I am the bot"

	# if user_message in ("time", "time?"):
	# 	now = datetime.now()
	# 	date_time = now.strftime("%d/%m/%y, %H:%M:%S")
	# 	response = str(date_time)

	# if response == "":
	# 	response = "i dont s understand you."

	# update.message.reply_text(response)

# gestore errore
def error(update, contex):
	print(f"Update {update} caused error {contex_error}")

# gestore handler
def main():
	updater = Updater(keys.API_KEY, use_context=True)
	dp = updater.dispatcher

	# handler dei comandi --------------------------------
	dp.add_handler(CommandHandler("start", start_command))
	dp.add_handler(CommandHandler("help", help_command))
	dp.add_handler(CommandHandler("search", search_command))
	dp.add_handler(CommandHandler("info", info_command))
	dp.add_handler(CommandHandler("random_hentai", random_hentai_command))
	dp.add_handler(CommandHandler("create_new_list", create_list_command))
	dp.add_handler(CommandHandler("print_all_list", print_all_list_command))
	dp.add_handler(CommandHandler("print_list", print_list_command))
	dp.add_handler(CommandHandler("add_to_list", add_to_list_command))
	dp.add_handler(CommandHandler("stop_add_item", stop_add_item_command))
	dp.add_handler(CommandHandler("stop_remove_item", stop_remove_item_command))
	dp.add_handler(CommandHandler("remove_from_list", remove_from_list_command))
	dp.add_handler(CommandHandler("delete_list", delete_list_command))
	# ----------------------------------------------------
	
	# handler messaggi normali ---------------------------------
	dp.add_handler(MessageHandler(Filters.text, handle_message))
	# ----------------------------------------------------------

	# handler errori ----------
	dp.add_error_handler(error)
	#  ------------------------

	updater.start_polling()
	updater.idle()

main()