import Constants as keys
from telegram.ext import *
import Responses as R

# Main Code

print("Bot started...")

# Ogni funzione svolge il compito di rispondere ad un certo tipo di messaggio
# <comando>.command risponde ai messaggi "comando" es. /start
def start_command(update, contex):
	update.message.reply_text("Type something to get started!")

def help_command(update, contex):
	update.message.reply_text("If u need help!, you should ask for it on google!")

def ciao_command(update, contex):
	update.message.reply_text("hai scritto ciao")

def bestemmia_command(update, contex):
	update.message.reply_text("non si bestemmia porcoddio fra")

# questa funzione rimanda al file Responses che gestisce i messaggi normali (non comandi)
def handle_message(update, contex):
	text = str(update.message.text).lower()
	response = R.sample_responses(text)

	update.message.reply_text(response)

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
	# dp.add_handler(MessageHandler(Filters.text, handle_message))
	# ----------------------------------------------------------

	# handler errori ----------
	dp.add_error_handler(error)
	#  ------------------------

	updater.start_polling()
	updater.idle()

main()