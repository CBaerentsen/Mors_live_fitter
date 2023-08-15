# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 11:17:06 2021

@author: chris
"""
# from pyspectrumdaq.m2i4931 import Card
import numpy as np
from PyQt5 import QtCore
import time
from scipy import signal
from pyspectrumdaq import Card

class DataCollector(QtCore.QRunnable):
    def __init__(self):
        super(DataCollector, self).__init__()
        
    def run(self):
        Data.acquire()
            

class Data(object):
    
    time_trace=np.array([])
    avg_time_trace=[]
    rFFT = []
    iFFT = []
    channel = 1
    time = 50*1e-3
    averages = 1
    samplerate = 30*1e6
    adc=[]
    error=0
    freq = []
    ns = int(time*samplerate)
    # It is highly recommended to use context management ("with" statement) to make sure
    # proper closing of the card

             

                # a now contains the data as a float64 NumPy array, shaped as [n_samples, n_channels]
                
    def start_acquire():

        try:
            Data.adc = Card()
            
            Data.ns = int(Data.time*Data.samplerate)
            Data.adc.set_acquisition(channels=[Data.channel], 
                                terminations=["50"], 
                                fullranges=[2],
                                pretrig_ratio=0, 
                                nsamples=Data.ns,
                                samplerate=Data.samplerate)         
            
            Data.adc.set_trigger(mode="ext")
            # print("2")
            time_trace = Data.adc.acquire()
            Data.ns = int(time_trace.shape[0])
            
            Data.freq = np.fft.fftfreq(Data.ns, d=1/Data.samplerate)[:int(Data.ns/2)]
            
            # print(2)
            
        except:
            if Data.error==0:
                print("There is no connection to the Daq card")
                Data.error = 1
    
    def acquire():
            
        try:
            data = Data.adc.acquire()
            if Data.time_trace.shape[0]==0:
                Data.time_trace = np.zeros([Data.averages+1,data.shape[0]])
                # print("2")
                Data.time_trace[0,:] = data[:,0]
                Data.counter = 1
            
            else:
                if data.shape[0]  == Data.time_trace.shape[1]:
                    Data.time_trace[Data.counter,:] = data[:,0]
                    # print("test1")
                    if Data.counter < Data.averages and Data.averages+1 == Data.time_trace.shape[0]:
                        Data.counter += 1
                    
                    elif Data.averages+1 != Data.time_trace.shape[0]:
                        if Data.averages+1 > Data.time_trace.shape[0]:
                            empty = np.zeros([Data.averages+1,data.shape[0]])
                            empty[:Data.time_trace.shape[0],:]=Data.time_trace
                            Data.time_trace = empty
                        else:
                            empty = np.zeros([Data.averages+1,data.shape[0]])
                            empty[:,:]=Data.time_trace[:empty.shape[0],:]
                            Data.time_trace = empty
                            if Data.counter > Data.averages:
                                Data.counter = Data.averages
                    
                    else:
                        Data.time_trace[:-1,:] = Data.time_trace[1:,:]
                        Data.counter = Data.averages
                        
                else: 
                    Data.time_trace=np.array([])
            
            
            Data.total_averages = Data.counter

                


            Data.avg_time_trace = np.average(Data.time_trace[:Data.counter,:],axis=0)
            # print(Data.avg_time_trace)
            
            Data.FFT()
        except Exception as e:
            if Data.error < 2:
                print("Daq card not being loaded")
                Data.time_trace=np.array([])
                QtCore.QThread.sleep(1)
        
        
    def FFT():
        
        FFT = np.fft.fft(Data.avg_time_trace)/Data.ns
        Data.PSD = np.abs(FFT[:int(Data.ns/2)])**2
        Data.abs = np.abs(FFT[:int(Data.ns/2)])
        Data.angle = np.angle(FFT[:int(Data.ns/2)])
        Data.imag = np.abs(np.real(FFT[:int(Data.ns/2)]))