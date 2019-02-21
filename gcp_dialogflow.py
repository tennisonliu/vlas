import pyaudio
import wave
import time
from queue import Queue
import dialogflow_v2 as dialogflow
import json
import uuid
import sys
import importlib

## Speech engine for voice-based feedback
speech_engine = importlib.import_module('speech_engine')
## Buffer to hold audio data from microphone input
intent_queue = Queue()

def detect_intent_stream(cred_path):
	## 
	# Function that streams audio input to dialogflow agent continuously until an intent is detected
	# If no intent is detected, function will call itself to start a new streaming audio input
	# @param cred_path: file path to the credentials file to access Google Cloud Platform
	# @return the query intent detected from streaming input

	intent_detected = False

	# parse json data to obtain relevant credentials
	with open(cred_path) as json_data:
		creds = json.load(json_data)
		project_id = creds['project_id']
	session_id = str(uuid.uuid4())
	language_code = 'en-US'

	# create session_client and session_path based on credentials
	from google.oauth2.service_account import Credentials
	credentials = Credentials.from_service_account_file(cred_path)
	session_client = dialogflow.SessionsClient(credentials=credentials)
	session_path = session_client.session_path(project_id, session_id)
	print('Session path: {}\n'.format(session_path))

	# audio stream configuration parameters
	audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
	sample_rate_hertz = 16000

	def request_generator(audio_config):
		##
		# Generator that continuously yields StreamingDetectIntentRequest() objects
		# When starting a new stream, the first object generated should include relevant
		# audio_config file. Objects generated after do not need to include config information
		# @param audio_config: audio stream configuration information
		# @return yielded chunks of HTTP requests to dialogflow with chunks of audio data
		
		query_input = dialogflow.types.QueryInput(audio_config=audio_config)
		yield dialogflow.types.StreamingDetectIntentRequest(
			session=session_path, query_input=query_input, single_utterance = True)
		while True:
			chunk = intent_queue.get()
			if not chunk:
				break
				print('not chunk!')
			yield dialogflow.types.StreamingDetectIntentRequest(input_audio = chunk,
																single_utterance = True)
	# audio configuaration
	audio_config = dialogflow.types.InputAudioConfig(
		audio_encoding=audio_encoding, language_code=language_code,
		sample_rate_hertz=sample_rate_hertz)
	
	requests = request_generator(audio_config)
	responses = session_client.streaming_detect_intent(requests)

	print('=' * 20)
	
	for response in responses:
		query_result = response.query_result
		print("Query Result: ", query_result)
		print('Intermediate transcript: "{}".'.format(
				response.recognition_result.transcript))
		print('\nQuery text: {}'.format(query_result.query_text))
		print('Detected intent: {} (confidence: {})\n'.format(
			query_result.intent.display_name,
			query_result.intent_detection_confidence))
		print('Fulfillment text: {}\n'.format(
			query_result.fulfillment_text))
		print(query_result.fulfillment_text)
		# if query_result indicates that intent has been detected, return
		if query_result.all_required_params_present==True \
			and query_result.intent.display_name != "Default Fallback Intent":
			intent_detected = True
			print("Intent detected, returning to main processing loop")
			print(query_result)
			return query_result
	# should have returned as soon as intent detected, but instead executes another intent-stream
	print('=' * 10)
	print("Reactivating dialogflow agent")
	# if intent has not been detected, restart streaming requests
	if intent_detected == False:
		detect_intent_stream(cred_path)

def stt_callback(in_data):
	##
	# Callback function that reads chunks of data from microphone and put
	# chunks in shared queue
	# @param in_data: new chunk of audio data
	# @return in_data and pyaudio flag to continue callback
	
	intent_queue.put(in_data)    
	return in_data, pyaudio.paContinue

def start_dialogflow_agent():
	##
	# Function to activate dialogflow agent, opens and starts pyaudio microphone stream
	# @return detected intent in query

	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, 
					channels = 1,
					rate = 16000,
					input = True,
					output = False,
					input_device_index = 1,
					frames_per_buffer = 2048,
					stream_callback = stt_callback)

	stream.start_stream()
	print('Input latency: ', stream.get_input_latency())

	speech_engine.speak("Virtual Agent Activated")
	final_query_result = detect_intent_stream('gcp_csiro_vlas_creds.json')
	print("%" * 40)
	print(final_query_result)
	return final_query_result
	stream.stop_stream()
	stream.close()
	intent_queue.queue.clear()