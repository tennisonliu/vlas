import pyttsx3

def speak(speech_text):
	##
	# Speech engine based on pyttsx3, performs text-to-speech
	# @param speech_text: text to be translated into speech
	engine = pyttsx3.init()
	engine.say(speech_text)
	engine.runAndWait()