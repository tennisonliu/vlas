import pyaudio
import wave
import time
import sys
import os

def countdown(t):
	while t:
		mins, secs = divmod(t, 60)
		timeformat = '{:02d}:{:02d}'.format(mins, secs)
		print(timeformat, end='\r')
		time.sleep(1)
		t -= 1

def recording(output_fp, samprate, num_channels, dev_ind):
	FORMAT = pyaudio.paInt16 #2 bytes audio encoding
	CHANNELS = num_channels
	RATE = int(samprate)
	CHUNK = 1024 #? 
	RECORD_TIME = 20 # record for 20 seconds
	WAVE_OUTPUT_FILENAME = output_fp
	# start recording
	stream = p.open(format = FORMAT, input_device_index=int(dev_ind), channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
	print("Recording...")
	frames = []
	
	for i in range(0, int(RATE/CHUNK*RECORD_TIME)):
		data = stream.read(CHUNK)
		frames.append(data)
	print("Finished Recording.\n")
	
	stream.stop_stream()
	stream.close()
	
	#write output file
	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(p.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()
	print("New wav file created.")

if __name__ == "__main__":
	path = input("Please specify which directory you wish to save your audio training samples\n")

	p = pyaudio.PyAudio()
	for ind in range (0, p.get_device_count()):
		info = p.get_device_info_by_index(ind)
		print(info)

	dev_ind = input("Which device do you wish to connect to?\n")
	info = p.get_device_info_by_index(int(dev_ind))
	samprate = info['defaultSampleRate']
	num_channels = info['maxInputChannels']
	print('sampling rate: ', samprate, ' num_channels: ', num_channels)
	time.sleep(1)

	voice_name = input("What is your name?\n")

	# Create directory
	dirName = path+'/'+voice_name
	 
	try:
		# Create target Directory
		os.mkdir(dirName)
		print(dirName ,  " Created ") 
	except FileExistsError:
		print(dirName ,  " already exists")

	print('Please repeat the activation phrase around 10-12 times, pause between each sample: \n')
	dirName = dirName + '/recorded.wav'

	recording(dirName, samprate, num_channels, dev_ind)


	p.terminate()
