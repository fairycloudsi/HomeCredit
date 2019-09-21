#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 20:41:59 2018

@author: fairy
"""

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout, BatchNormalization
from keras.layers.advanced_activations import PReLU
from keras.optimizers import Adam
from sklearn.model_selection import KFold

import gc
import os

from sklearn.metrics import roc_auc_score
from keras.callbacks import Callback

class roc_callback(Callback):
    def __init__(self,training_data,validation_data):
        self.x = training_data[0]
        self.y = training_data[1]
        self.x_val = validation_data[0]
        self.y_val = validation_data[1]


    def on_train_begin(self, logs={}):
        return

    def on_train_end(self, logs={}):
        return

    def on_epoch_begin(self, epoch, logs={}):
        return

    def on_epoch_end(self, epoch, logs={}):
        y_pred = self.model.predict(self.x)
        roc = roc_auc_score(self.y, y_pred)
        y_pred_val = self.model.predict(self.x_val)
        roc_val = roc_auc_score(self.y_val, y_pred_val)
        print('\rroc-auc: %s - roc-auc_val: %s' % (str(round(roc,4)),str(round(roc_val,4))),end=100*' '+'\n')
        return

    def on_batch_begin(self, batch, logs={}):
        return

    def on_batch_end(self, batch, logs={}):
        return

def f10_dnn(X_train, Y_train, nn_num_folds=10):
    
    folds = KFold(n_splits=nn_num_folds, shuffle=True, random_state=42)

    for n_fold, (nn_trn_idx, nn_val_idx) in enumerate(folds.split(X_train)):
        nn_trn_x, nn_trn_y = X_train.iloc[nn_trn_idx,:], Y_train[nn_trn_idx]
        nn_val_x, nn_val_y = X_train.iloc[nn_val_idx,:], Y_train[nn_val_idx]

        print( 'Setting up neural network...' )
        nn = Sequential()
        nn.add(Dense(units = 400 , kernel_initializer = 'normal', input_dim = 718))
        nn.add(PReLU())
        nn.add(Dropout(.3))
        nn.add(Dense(units = 160 , kernel_initializer = 'normal'))
        nn.add(PReLU())
        nn.add(BatchNormalization())
        nn.add(Dropout(.3))
        nn.add(Dense(units = 64 , kernel_initializer = 'normal'))
        nn.add(PReLU())
        nn.add(BatchNormalization())
        nn.add(Dropout(.3))
        nn.add(Dense(units = 26, kernel_initializer = 'normal'))
        nn.add(PReLU())
        nn.add(BatchNormalization())
        nn.add(Dropout(.3))
        nn.add(Dense(units = 12, kernel_initializer = 'normal'))
        nn.add(PReLU())
        nn.add(BatchNormalization())
        nn.add(Dropout(.3))
        nn.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
        nn.compile(loss='binary_crossentropy', optimizer='adam')

        print( 'Fitting neural network...' )
        nn.fit(nn_trn_x, nn_trn_y, validation_data = (nn_val_x, nn_val_y), epochs=10, verbose=2,
              callbacks=[roc_callback(training_data=(nn_trn_x, nn_trn_y),validation_data=(nn_val_x, nn_val_y))])
        
        #print( 'Predicting...' )
        #sub_preds += nn.predict(X_test).flatten().clip(0,1) / folds.n_splits
    
        gc.collect()
        
        return nn