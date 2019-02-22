import time
import os

def save_file(conv_hist, trans_hist):
	##
	# Function that saves files to directory on Desktop
	# @param conv_hist: log of conversation history
	# @param trans_hist: transcription history

	desktop = os.path.expanduser("~\\Desktop")
	save_file_path = str(desktop) + "\\SaveFile"
	if not os.path.exists(save_file_path):
		os.makedirs(save_file_path)
	save_file_path = save_file_path + "\\test.txt"
	with open (str(save_file_path), 'w') as file:
		file.write(str(conv_hist))
		file.write(str(trans_hist))
