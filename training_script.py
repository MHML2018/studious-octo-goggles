# Create a MLP network in Keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import *
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
import numpy as np
#6import pickle
# fix random seed for reproducibility
#numpy.random.seed(7)
# load pima indians dataset
dataset = np.loadtxt("DataSetV4/data.csv", delimiter=",")
# split into input (X) and output (Y) variables

np.random.shuffle(dataset)

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

dataset_train, dataset_test = train_test_split(dataset, test_size=0.2)

X = dataset_train[:,0:13]

meanz = np.mean(X)
maxz = np.max(X)
minz = np.min(X)
X = X-meanz
X = X/(maxz - minz)

num_classes = 6

Y = dataset_train[:,13]
Y = to_categorical(Y, num_classes)
# create model
#print(X)
#print(Y)
model = Sequential()
model.add(Dense(20, input_dim=13, activation='tanh'))
model.add(Dense(20, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(num_classes, activation='sigmoid'))
# Compile model
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])
              
earlystop = EarlyStopping(monitor='val_acc', min_delta=0.0001, patience=50, verbose=1, mode='auto')
callbacks_list = [earlystop]
			  
model.fit(X, Y, epochs=1000, batch_size=200, callbacks=callbacks_list, verbose=1, validation_split=0.2)
# evaluate the model

X_test = dataset_test[:,0:13]
X_test = X_test-meanz
X_test = X_test/(maxz - minz)
Y_test = dataset_test[:,13]
Y_test = to_categorical(Y_test, num_classes)

Y_pred=model.predict(X_test)
conf_matx = confusion_matrix(Y_test.argmax(axis=1), Y_pred.argmax(axis=1))

scores = model.evaluate(X_test, Y_test)
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

print(conf_matx)

