import numpy as np
from pydub import AudioSegment
import random
import sys
import io
import os
import glob
from td_utils import *
import pyaudio
from queue import Queue
from threading import Thread
import sys
import time

def detect_triggerword_spectrum(model, x):
	##
	# Function to predict existence of trigger word in spectrogram sample
	# @param model: DNN model used to predict for trigger word
	# @param x: frequency spectrogram diagram
	# @return predictions made over sample

	x = x.swapaxes(0,1)
	x = np.expand_dims(x, axis = 0)
	predictions = model.predict(x)
	return predictions.reshape(-1)

def has_triggerword(predictions, chunk_duration, feed_duration, threshold=0.5):
	##
	# Function to predict if trigger word exists
	# @param predictions: probability distribution of existence of trigger word over entire sample
	# @param chunk_duration: size of chunk
	# @param feed_duration: size of entire feed, 10 seconds
	# @param threshold: threshold used to compare against prediction probability
	# @return boolean value to indicate chunk has trigger word

	predictions = predictions>threshold
	chunk_predictions_samples = int(len(predictions)*chunk_duration/feed_duration)
	chunk_predictions = predictions[-chunk_predictions_samples:]
	level = chunk_predictions[0]
	for pred in chunk_predictions:
		if pred > level:
			return True
		else:
			level = pred
	return False

def get_spectrogram(data):
	##
	# Function that generates frequency spectrogram based on input audio data
	# @param data: input audio file
	# @return frequency spectrogram of audio file
	
	nfft = 200 # Length of each window segment
	fs = 8000 # Sampling frequencies
	noverlap = 120 # Overlap between windows
	nchannels = data.ndim
	if nchannels == 1:
		pxx, _, _ = mlab.specgram(data, nfft, fs, noverlap = noverlap)
	elif nchannels == 2:
		pxx, _, _ = mlab.specgram(data[:,0], nfft, fs, noverlap = noverlap)
	return pxx

def detect_twd():
	##
	# Function to start listening to streaming microphone input
	# and predict if trigger word is present
	
	model = load_model("./demo_model/ok_1.h5")
	chunk_duration = 0.5
	fs = 44100
	chunk_samples = int(fs*chunk_duration)

	feed_duration = 10
	feed_samples = int(fs*feed_duration)

	q = Queue()
	data = np.zeros(feed_samples, dtype = 'int16')
	run = True

	def callback(in_data, frame_count, time_info, status):
		global data
		data0 = np.frombuffer(in_data, dtype = 'int16')
		data = np.append(data, data0)
		if len(data)>feed_samples:
			data = data[-feed_samples:]
			q.put(data)
		return(in_data, pyaudio.paContinue)

	p = pyaudio.PyAudio()
	stream = p.open(
				format=pyaudio.paInt16,
				channels=1,
				rate = fs,
				input = True,
				frames_per_buffer = chunk_samples,
				input_device_index = 1,
				stream_callback = callback)

	stream.start_stream()

	try:
		while run:
			data = q.get()
			spectrum = get_spectrogram(data)
			preds = detect_triggerword_spectrum(model, spectrum)
			new_trigger = has_triggerword(preds, chunk_duration, feed_duration)
			if new_trigger:
				print('1', end=''),
				run = False
				print('Trigger Word Activated, returning to main processing loop')
			else:
				print('-', end = ''),

	except(KeyboardInterrupt, SystemExit):
		stream.stop_stream()
		stream.close()
		q.queue.clear()
		run = False
	print('Returning to main loop')
	stream.stop_stream()
	stream.close()
	q.queue.clear()
	return