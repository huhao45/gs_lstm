# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:28:52 2020

@author: 59654
"""
import data_read_n
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout
from keras.optimizers import SGD
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn import metrics
# from sklearn.preprocessing import MinMaxScaler
def plot_predictons(test,result):
    plt.plot(test,color = 'red',label = 'True_data')
    plt.plot(result,color = 'blue',label = 'Predict_data')
    plt.title('gsdsklyc')
    plt.xlabel('Time')
    plt.ylabel('value')
    plt.legend()
    plt.show()

def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


data = data_read_n.getdata()
data = data[['count1','month','day','最高气温','time_min']]
data = data[data['month']<8]
data_len = len(data)

# 手动归一化
MAX_Y = data['count1'].max()
MIN_Y = data['count1'].min()
data['count1'] = (data['count1']- MIN_Y)/(MAX_Y- MIN_Y)
data = data.reset_index()
train_set = data[~(data['day']==28) & (data['month']==7)]
test_set = data[(data['day']==28) & (data['month']==7)]
# 转numpy
train_set_scaled =train_set.values
test_set_scaled =test_set.values
train_len = len(train_set_scaled)
PREDICT_TIME = 12
# train_set = normalization(train_set['count1'])
# test_set = normalization(test_set['count1'])
# 归一化
# sc = MinMaxScaler(feature_range=[0,1])
# train_set_scaled = sc.fit_transform(train_set)

# plot_predictons(train_set['time_h'], train_set['count1'])
# train_set.plot(figsize = (16,4),legend=True)
# test_set.plot(figsize = (16,4),legend=True)

X_train = []
Y_train = []
for i in range(PREDICT_TIME,train_len):
    X_train.append(train_set_scaled[i-PREDICT_TIME:i,1])
    Y_train.append(train_set_scaled[i,1])
    
X_train,Y_train = np.array(X_train),np.array(Y_train)
X_train = np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1))
X_train = X_train.astype('float64')
model = Sequential()
# first layer
model.add(LSTM(64,return_sequences = True,input_shape=(X_train.shape[1],1)))
model.add(Dropout(0.2))
# second layer
model.add(LSTM(64,return_sequences = True))
model.add(Dropout(0.2))
# third layer
model.add(LSTM(64))
model.add(Dropout(0.2))

model.add(Dense(units=1))
sgd = SGD(lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(optimizer = sgd,loss = 'mse')
model.fit(X_train,Y_train,epochs=200,batch_size = 32)

data_total = pd.concat((train_set,test_set),axis = 0)
inputs = data_total[len(data_total)-len(test_set)-PREDICT_TIME:]
inputs = inputs['count1'].values
inputs = inputs.reshape(-1,1)
input_len = len(inputs)
# inputs = sc.fit_transform(inputs)


X_test = []
for i in range(PREDICT_TIME,input_len):
    X_test.append(inputs[i-PREDICT_TIME:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
predict_test = model.predict(X_test)
# predict_result = sc.inverse_transform(predict_test)
# test_set_scaled = sc.fit_transform(test_set)
test_set_scaled = test_set_scaled[:,1]
true_y = MIN_Y+ test_set_scaled * (MAX_Y - MIN_Y)
predict_y = MIN_Y+ predict_test * (MAX_Y - MIN_Y)
# plot_predictons(test_set_scaled,predict_test)
plot_predictons(true_y,predict_y)
print("accuracy_score:",accuracy_score(true_y, predict_y))


