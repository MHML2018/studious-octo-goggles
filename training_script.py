# Create a MLP network in Keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import *
from keras.utils import to_categorical
import numpy as np
#6import pickle
# fix random seed for reproducibility
#numpy.random.seed(7)
# load pima indians dataset
dataset = np.loadtxt("DataSetV2/data.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:13]
meanz = np.mean(X)
maxz = np.max(X)
minz = np.min(X)
X = X-meanz
X = X/(maxz - minz)

num_classes = 5

Y = dataset[:,13]
Y = to_categorical(Y, num_classes)
# create model
#print(X)
#print(Y)
model = Sequential()
model.add(Dense(18, input_dim=13, activation='tanh'))
model.add(Dense(20, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(num_classes, activation='sigmoid'))
# Compile model
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])
			  
model.fit(X, Y, epochs=200, batch_size=100, verbose=1)
# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# serialize model to JSON
model_json = model.to_json()
with open("model.nn", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
 
print("Norm-Parms - mean, max, min")
print(meanz)
print(maxz)
print(minz)
