#!/usr/bin/python3
import Constants as keys
from telegram.ext import *
from telegram import *
from datetime import datetime
from pprint import pprint
import random
import re
import bs4, requests, webbrowser

# Main Code
stato = 'IDLE'
url = "https://www.google.it/search?q=pathToReplace&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjJ8rfZsKj3AhW-k_0HHUtBCwAQ_AUoAXoECAIQAw&biw=639&bih=600&dpr=1.5"
print("Bot started...")

# Ogni funzione svolge il compito di rispondere ad un certo tipo di messaggio
def start_command(update, contex):
	start_text = "Benvenuto, sono un bot in sviluppo, usa il comando /help per sapere cosa posso fare. BuonBot!!"
	# buttons = [[KeyboardButton("ciao")], [KeyboardButton("salve")]]
	contex.bot.send_message(chat_id=update.effective_chat.id, text=start_text)#,
	# reply_markup=ReplyKeyboardMarkup(buttons))
	# update.message.reply_text("Type something to get started)

def help_command(update, contex):
	update.message.reply_text("Digitando /search, svolgerò una ricerca di immagini riferite alla parola/frase che mi darai")

def search_command(update, contex):
	global stato
	if stato == 'IDLE':
		contex.bot.send_message(chat_id=update.effective_chat.id, text="Dammi una parola chiave per la ricerca")
		stato = 'WAITING_SEARCHING_KEY'
		return

	user_message = str(update.message.text).lower()

	# pattern = re.compile(r"^/search (.+)$")
	# if re.search(pattern, user_message) is None:
	# 	update.message.reply_text("Termini di ricerca errati, usare il comando non basta, abbina una parola con cui fare la ricerca!")
	# 	return
	# else:
	# semi_path = re.search(pattern, user_message).group(1)

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
	contex.bot.send_photo(chat_id=update.effective_chat.id, photo=(re.search(pattern, str(title[rand])).group(1)))		
	# contex.bot.sendDocument(chat_id=update.effective_chat.id, document=(re.search(pattern, str(title[rand])).group(1)))
	stato = 'IDLE'

def info_command(update, contex):
	user = update.message.from_user
	print(f'You talk with user {user["username"]} and his user ID: {user["id"]}')
	# print('You talk with user {} and his user ID: {} '.format(user['username'], user['id']))

# questa funzione rimanda al file Responses che gestisce i messaggi normali (non comandi)
def handle_message(update, contex):
	global stato

	if stato == 'WAITING_SEARCHING_KEY':
		search_command(update, contex)
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