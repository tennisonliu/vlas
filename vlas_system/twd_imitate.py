import time
import importlib
## imported speech_engine module
speech_engine = importlib.import_module('speech_engine')

def twd_imitate(queue):
	##
	# Function that imitates the functionality of the trigger word detection engine
	# waits 5 seconds before returning, mimicking the system waking up after detecting
	# trigger words
	
	# user_input = input("Please press 1 if you intend to activate the system")
	time.sleep(5)

	print("twd activated")
	queue.put({
		"widget" : "assistant_status_LED",
		"widget_update": True
		})
	queue.put({
		"widget" : "assistant_status",
		"widget_update": True
		})
	speech_engine.speak("Hello, what can I do for you?")
	return