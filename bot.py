import telebot
import pyowm
bot = telebot.TeleBot("", parse_mode=None)

from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM('7a9a9583a439e56a2c6a0148d88a2e56', config_dict)
mgr = owm.weather_manager()

welcome_message = "Привет!" + "\n" + "Я покажу тебе погоду в любом городе и подскажу, как одеваться!" + "\n" + "Введи любой город..." 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, welcome_message)

@bot.message_handler(content_types=['text'])
def send_echo(message):
	try:
		observation = mgr.weather_at_place(message.text)
		w = observation.weather
		temp = w.temperature('celsius')["temp"]
		wind = w.wind()["speed"]
		
		answer ="В городе " + message.text + " сейчас " + w.detailed_status +"\n"
		answer += "Температура: " + str(temp) + " градусов" +"\n" 
		answer += "Скорость ветра: " + str(wind) + " м/с" + "\n\n"

		if temp < -20:
			answer += "Чета капец как холодна >_< " + "\n" + "Лучше на улицу не выходить"
		elif temp < -10 :
			answer += "Холодрыга на улице, лучше одеться потеплее "
		elif temp < 0 :
			answer += "На улице холодно, одевайтесь! "
		elif temp < 10 :
			answer += "На улице прохладно, лучше одеть куртку "
		elif temp < 20 :
			answer += "На улице тепло, но возьмите с собой кофту "
		elif temp < 30 :
			answer += "На улице отличная погода, можно идти в шортах "	
		else:
			answer += "Жарковато "

		bot.send_message(message.chat.id, answer)
	except:
		bot.send_message(message.chat.id, "Ошибка! Нет такого города." + "\n" + "Попробуйте еще")

bot.polling( none_stop = True )



