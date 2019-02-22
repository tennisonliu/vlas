from __future__ import division
import re
import sys
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

class MicrophoneStream(object):
	##
	# Streaming audio input from microphone built on Pyaudio library
	
	def __init__(self, rate, chunk):
		##
		# Constructor
		
		self._rate = rate
		self._chunk = chunk
		print(rate, chunk)
		self._buff = queue.Queue()
		self.closed = True

	def __enter__(self):
		##
		# Initialise pyaudio stream for streaming microphone recording
		
		self._audio_interface = pyaudio.PyAudio()
		self._audio_stream = self._audio_interface.open(
			format=pyaudio.paInt16,
			channels=1, rate=self._rate,
			input=True, output=False, input_device_index=1,
			frames_per_buffer=self._chunk,
			stream_callback=self._fill_buffer,
		)

		self.closed = False

		return self

	def __exit__(self, type, value, traceback):
		##
		# Function to close stream and stop recording
		
		self._audio_stream.stop_stream()
		self._audio_stream.close()
		self.closed = True
		self._buff.put(None)
		self._audio_interface.terminate()

	def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
		## 
		# Puts recorded audio data into buffer
		
		self._buff.put(in_data)
		return None, pyaudio.paContinue

	def generator(self):
		##
		# Generator that yields chunks of streaming audio data
		
		while not self.closed:
			chunk = self._buff.get()
			if chunk is None:
				return
			data = [chunk]
			while True:
				try:
					chunk = self._buff.get(block=False)
					if chunk is None:
						return
					data.append(chunk)
				except queue.Empty:
					break

			yield b''.join(data)


def listen_print_loop(responses, queue):
	##
	# Obtain the HTTP response from Google Speech API and iterate through responses
	# until user decides to exit the system. Prints out the intermediate transcripts to GUI
	# @param responses: list of HTTP responses from Google Speech API after streaming audio chunks
	# @param queue: gui_queue which updates widgets on the GUI

	num_chars_printed = 0
	exit = False
	for response in responses:
		if exit == True:
			return
		else:
			if not response.results:
				continue
			result = response.results[0]
			if not result.alternatives:
				continue
			transcript = result.alternatives[0].transcript
			overwrite_chars = ' ' * (num_chars_printed - len(transcript))

			# if transcription result is not final, continue transcribing
			if not result.is_final:
				sys.stdout.write(transcript + overwrite_chars + '\r')
				sys.stdout.flush()
				num_chars_printed = len(transcript)
			# if transcription result is final
			else:
				print(transcript + overwrite_chars)
				# perform regex search to detect if user wants to stop transcription
				if re.search(r'\b(exit transcription|quit transcription|exit|quit)\b', transcript, re.I):
					print('Exiting..')
					exit = True
					return
				# if user does not want to quit, update gui and keep transcribing notes
				else:
					if exit != True:
						trans_hist = transcript + overwrite_chars
						queue.put({
							"widget": "transcription",
							"widget_update": trans_hist
							})
				num_chars_printed = 0

def streaming_transcribe(queue):
	##
	# Function that performs speech-to-text on streaming audio input
	# @param queue: gui_queue which will be updated

	## sampling rate for microphone input
	RATE = 16000
	## size of each chunk of data
	CHUNK = RATE / 10
	## file path to credentials file
	cred_path = 'gcp_csiro_vlas_creds.json' 
	language_code = 'en-US'     
	
	# create speechclient() based on credentials
	from google.oauth2.service_account import Credentials
	credentials = Credentials.from_service_account_file(cred_path)
	client = speech.SpeechClient(credentials=credentials)
	
	# configuration of input audio stream
	config = types.RecognitionConfig(
		encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
		sample_rate_hertz=RATE,
		language_code=language_code)
	streaming_config = types.StreamingRecognitionConfig(
		config=config,
		interim_results=True)

	with MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()
		requests = (types.StreamingRecognizeRequest(audio_content=content)
					for content in audio_generator)

		responses = client.streaming_recognize(streaming_config, requests)
		listen_print_loop(responses, queue)
