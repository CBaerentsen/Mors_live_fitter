# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 11:17:06 2021

@author: chris
"""
# from pyspectrumdaq.m2i4931 import Card
import numpy as np
from PyQt5 import QtCore
import time

# from pyspectrumdaq import Card

class DataCollector(QtCore.QRunnable):
    def __init__(self):
        super(DataCollector, self).__init__()
        
    def run(self):
        while True:
            begin = time.time()
            Data.acquire()
            timer = (time.time()-begin)*1e3
            if timer<10:
                QtCore.QThread.msleep(int(10-timer))


class Data(object):
    
    time_trace=[]
    avg_time_trace=[]
    rFFT = []
    iFFT = []
    channel = 1
    time = 50*1e-3
    averages = 1
    samplerate = 30*1e6
    adc=[]
    error=0
    
    # It is highly recommended to use context management ("with" statement) to make sure
    # proper closing of the card

             

                # a now contains the data as a float64 NumPy array, shaped as [n_samples, n_channels]
                
    def start_acquire():
        try:
            with Card() as adc:
                adc.acquisition_set(channels=Data.channel, 
                                    terminations=["50"], 
                                    fullranges=[2],
                                    pretrig_ratio=0, 
                                    Ns=int(Data.time*Data.samplerate),
                                    samplerate=Data.samplerate)             
                adc.trigger_set(mode="pos")
        except:
            if Data.error==0:
                print("There is no connection to the Daq card")
                Data.error = 1
        
    def acquire():
        Data.time=1
        if Data.adc == []:
            Data.start_acquire()
            
        try:
            Data.time_trace = np.vstack([Data.time_trace,Data.adc.acquire()])
            
            if Data.time_trace.shape[0] < Data.averages:
                Data.time_trace = np.delete(Data.time_trace, 0, 0)
        
            Data.avg_time_trace = np.average(Data.time_trace,1)
            
            Data.FFT()
        except:
            if Data.error < 2:
                print("Daq card not being loaded")
                Data.error = 2
        
        
    def FFT():
        FFT = np.fft.fft(Data.avg_time_trace)
        Data.rFFT = FFT.real
        Data.iFFT = FFT.imag