import numpy as np
import random
import sys
import io
import os
import glob
import pickle

from keras.callbacks import ModelCheckpoint
from keras.models import Model, load_model, Sequential
from keras.layers import Dense, Activation, Dropout, Input, Masking, TimeDistributed, LSTM, Conv1D
from keras.layers import GRU, Bidirectional, BatchNormalization, Reshape
from keras.optimizers import Adam
import keras

import tensorflow as tf
if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please install GPU version of TF")

training_history = []

model = load_model("og.h5")

opt = Adam(lr = 0.0001, beta_1 = 0.9, beta_2 = 0.999, decay = 0.01)
model.compile(loss = 'binary_crossentropy', optimizer = opt, metrics = ['accuracy'])
X = np.load("/flush1/liu181/Batch_Inputs/x_inputs_batch.npy")
Y = np.load("/flush1/liu181/Batch_Inputs/y_inputs_batch.npy")
'''
earlystopping = keras.callbacks.EarlyStopping(monitor = 'val_acc', min_delta = 0, patience = 0, verbose = 0, 
											mode = 'auto', baseline = None, restore_best_weights = False)
'''
history = model.fit(X, Y, validation_split = 0.1, shuffle = True, batch_size = 10, epochs = 10)
training_history.append(history.history)

with open('training_history', 'wb') as f:
	pickle.dump(training_history, f)


model.save("twd_model.h5")

