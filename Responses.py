from datetime import datetime

#qua scrivo le funzioni per le risposte ai messaggi normali
def sample_responses(input_text):
	user_message = str(input_text).lower()

	if user_message in ("hello", "hi", "sup"):
		return "hey! How is it going?"

	if user_message in ("who are you", "who are you?"):
		return "I am the bot"

	if user_message in ("time", "time?"):
		now = datetime.now()
		date_time = now.strftime("%d/%m/%y, %H:%M:%S")

		return str(date_time)

	return "i dont s understand you."