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
            if Data.time_trace.shape[0]==0:
                Data.time_trace = Data.adc.acquire()
            
            else:
                time_trace = Data.adc.acquire()
                
                if time_trace.shape[0]  == Data.time_trace.shape[0]:
                    Data.time_trace = np.hstack([Data.time_trace, Data.adc.acquire()])
                    
                else: 
                    Data.time_trace = time_trace
            

            if Data.time_trace.shape[1] > Data.averages:
                for i in range(Data.time_trace.shape[1]-Data.averages):
                    Data.time_trace = np.delete(Data.time_trace, 0, 1)


            Data.avg_time_trace = np.average(Data.time_trace,1)

            
            Data.FFT()
        except Exception as e:
            if Data.error < 2:
                print("Daq card not being loaded")
                time_trace=np.array([])
                QtCore.QThread.sleep(1)
        
        
    def FFT():
        
        FFT = np.fft.fft(Data.avg_time_trace)/Data.ns
        Data.rFFT = np.abs(FFT.real[:int(Data.ns/2)])
        Data.iFFT = np.abs(FFT.imag[:int(Data.ns/2)])