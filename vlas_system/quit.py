import sys
import importlib
## imported save_file module
save_file = importlib.import_module('save_file')
## imported speech_engine module
speech_engine = importlib.import_module('speech_engine')

def quit_detect_intent(conv_hist, trans_hist):
	##
	# Function that saves conv_hist and trans_hist to disk before quitting
	# the system
	# @param conv_hist: conversation history log
	# @param trans_hist: transcription log

	speech_engine.speak("Quitting now. Your files have been saved")
	save_file.save_file(conv_hist, trans_hist)
	sys.exit()