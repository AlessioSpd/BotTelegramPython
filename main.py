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
url = "https://www.google.it/search?q=pathToReplace&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjJ8rfZsKj3AhW-k_0HHUtBCwAQ_AUoAXoECAIQAw&biw=639&bih=600&dpr=1.5"
print("Bot started...")

# Ogni funzione svolge il compito di rispondere ad un certo tipo di messaggio
# <comando>.command risponde ai messaggi "comando" es. /start
def start_command(update, contex):
	buttons = [[KeyboardButton("ciao")], [KeyboardButton("salve")]]
	contex.bot.send_message(chat_id=update.effective_chat.id, text="welcome",
	reply_markup=ReplyKeyboardMarkup(buttons))
	# update.message.reply_text("Type something to get started)

def help_command(update, contex):
	update.message.reply_text("If u need help!, you should ask for it on google!")

def ciao_command(update, contex):
	update.message.reply_text("hai scritto ciao")

def bestemmia_command(update, contex):
	update.message.reply_text("non si bestemmia porcoddio fra")

# questa funzione rimanda al file Responses che gestisce i messaggi normali (non comandi)
def handle_message(update, contex):
	response = ""
	user_message = str(update.message.text).lower()
	semi_path = user_message.replace(" ", "+")
	complete_path = url.replace("pathToReplace", semi_path)
	
	# scarico il sorgente
	res = requests.get(complete_path)
	html_page = bs4.BeautifulSoup(res.text, 'html.parser')
	title = html_page.select('img')

	pattern = re.compile(r".*src=\"(.*);")

	rand = random.randint(1,21)

	contex.bot.send_photo(chat_id=update.effective_chat.id, photo=(re.search(pattern, str(title[rand])).group(1)))	



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
	dp.add_handler(CommandHandler("ciao", ciao_command))
	dp.add_handler(CommandHandler("bestemmia", bestemmia_command))
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