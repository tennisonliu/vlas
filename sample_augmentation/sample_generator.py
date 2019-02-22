
import numpy as np
# from home.liu181\.local.lib.python3\.4.site-packages.pydub import AudioSegment
# from pydub import AudioSegment
import random
import sys
sys.path.append("/home/liu181/.local/lib/python3.4/site-packages")
from pydub import AudioSegment
import io
import os
import glob
from td_utils import *

def get_random_time_segment(segment_ms):
    """
    Gets a random time segment of duration segment_ms in a 10,000 ms audio clip.
    
    Arguments:
    segment_ms -- the duration of the audio clip in ms ("ms" stands for "milliseconds")
    
    Returns:
    segment_time -- a tuple of (segment_start, segment_end) in ms
    """
    
    segment_start = np.random.randint(low=0, high=10000-segment_ms)   # Make sure segment doesn't run past the 10sec background 
    segment_end = segment_start + segment_ms - 1
    
    return (segment_start, segment_end)

def is_overlapping(segment_time, previous_segments):
    """
    Checks if the time of a segment overlaps with the times of existing segments.
    
    Arguments:
    segment_time -- a tuple of (segment_start, segment_end) for the new segment
    previous_segments -- a list of tuples of (segment_start, segment_end) for the existing segments
    
    Returns:
    True if the time segment overlaps with any of the existing segments, False otherwise
    """
    
    segment_start, segment_end = segment_time
    overlap = False
    for previous_start, previous_end in previous_segments:
        if segment_start <= previous_end and segment_end >= previous_start:
            overlap = True

    return overlap

def insert_audio_clip(background, audio_clip, previous_segments):
    """
    Insert a new audio segment over the background noise at a random time step, ensuring that the 
    audio segment does not overlap with existing segments.
    
    Arguments:
    background -- a 10 second background audio recording.  
    audio_clip -- the audio clip to be inserted/overlaid. 
    previous_segments -- times where audio segments have already been placed
    
    Returns:
    new_background -- the updated background audio
    """
    
    segment_ms = len(audio_clip)
    segment_time = get_random_time_segment(segment_ms)
    while is_overlapping(segment_time, previous_segments):
        segment_time = get_random_time_segment(segment_ms)
    previous_segments.append(segment_time)
    new_background = background.overlay(audio_clip, position = segment_time[0])
    
    return new_background, segment_time

def insert_ones(y, segment_end_ms):
    """
    Update the label vector y. The labels of the 50 output steps strictly after the end of the segment 
    should be set to 1. By strictly we mean that the label of segment_end_y should be 0 while, the
    50 followinf labels should be ones.
    
    
    Arguments:
    y -- numpy array of shape (1, Ty), the labels of the training example
    segment_end_ms -- the end time of the segment in ms
    
    Returns:
    y -- updated labels
    """
    segment_end_y = int(segment_end_ms * Ty / 10000.0)
    for i in range(segment_end_y + 1, segment_end_y + 51):
        if i < Ty:
            y[0, i] = 1
    
    return y

def load_samples(act_path, neg_path, back_path):
    activates = []
    backgrounds = []
    negatives = []
    for filename in os.listdir(act_path):
        if filename.endswith("wav"):
            fp_activate = AudioSegment.from_wav(act_path+"/"+filename)
            activates.append(fp_activate)
    print("Number of activation phrases: ", len(activates))
    for filename in os.listdir(neg_path):
        if filename.endswith("wav"):
            fp_negative = AudioSegment.from_wav(neg_path+"/"+filename)
            negatives.append(fp_negative)
    print("Number of negative phrases: ", len(negatives))
    for filename in os.listdir(back_path):
        if filename.endswith("wav"):
            print(filename)
            fp_background = AudioSegment.from_wav(back_path+"/"+filename)
            segment_start = 1*1000
            segment_end = 11*1000
            fp_background = fp_background[segment_start:segment_end]
            fp_background = fp_background-10
            backgrounds.append(fp_background)
    print("Number of background phrases: ", len(backgrounds))
    return activates, negatives, backgrounds

Ty = 1375

def generating_training_sets(backgrounds, activates, negatives, index):
    """
    Creates a certain number of training samples with background noise overlayed 
    with random activation phrases and negative phrases.
    
    Arguments:
    num_samples -- number of training phrases we wish to generate
    background -- list of background noises
    activates -- list of activation phrases
    negatives -- list of negative phrases
    
    Returns:
    x -- the spectrogram of the training example
    y -- the label at each time step of the spectrogram
    """
    y = np.zeros((1, Ty))

    previous_segments = []
    

    random_index_background = np.random.randint(0, 4)
    
    random_background = backgrounds[random_index_background]
    print("Background track: ", random_index_background)
    num_of_activates = np.random.randint(2, 4)
    random_indices_act = np.random.randint(len(activates), size = num_of_activates)
    random_activates = [activates[j] for j in random_indices_act]
    num_of_negatives = np.random.randint(1, 4)
    random_indices_neg = np.random.randint(len(negatives), size = num_of_negatives)
    random_negatives = [negatives[j] for j in random_indices_neg]
        
    for random_activate in random_activates:
        random_background, segment_time = insert_audio_clip(random_background, random_activate, previous_segments)
        segment_start, segment_end = segment_time
        y = insert_ones(y, segment_end_ms=segment_end)
    

    for random_negative in random_negatives:
        random_background, _ = insert_audio_clip(random_background, random_negative, previous_segments)
    
    file_handle = random_background.export("/flush1/liu181/training_samples/sample_"+str(index)+ ".wav", format="wav")

    x = graph_spectrogram("/flush1/liu181/training_samples/sample_"+str(index)+ ".wav")
    np.save("/flush1/liu181/training_samples/IndividualSamples_X/sample_" + str(index)+".npy", x)
    np.save("/flush1/liu181/training_samples/IndividualSamples_Y/sample_"+ str(index)+".npy", y)

    return x, y

act_path = "/flush1/liu181/samples/Activations_New"
neg_path = "/flush1/liu181/samples/negatives_22"
back_path = "/flush1/liu181/samples/Background"
activates, negatives, backgrounds = load_samples(act_path, neg_path, back_path)

shape_x = (0, 5511, 101)
shape_y = (0, 1375, 1)

final_x = np.empty(shape_x)
final_y = np.empty(shape_y)

for i in range(0, 4000):
	x, y = generating_training_sets(backgrounds = backgrounds, activates = activates, negatives = negatives, index = i)
	x = x.swapaxes(0,1)
	x = np.expand_dims(x, axis=0)

	y = y.swapaxes(0,1)
	y = np.expand_dims(y, axis = 0)

	final_x = np.append(final_x, x, axis = 0)
	final_y = np.append(final_y, y, axis = 0)
	print('x_final shape: ', final_x.shape)
	print('y_final shape: ', final_y.shape)

	print(i)

print('x shape: ', final_x.shape)
print('y shape: ', final_y.shape)

np.save("/flush1/liu181/22/Network_Inputs/x_inputs_multi.npy", final_x)
np.save("/flush1/liu181/22/Network_Inputs/y_inputs_multi.npy", final_y)


