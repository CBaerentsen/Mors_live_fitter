# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:01:26 2019

@author: chris
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from main_window_ui import Ui_MainWindow
import numpy as np
from pyqtgraph import PlotWidget
from pyqtgraph import mkQApp
import pyqtgraph as pg
from fit_v2 import Fit, FitCollector
from data_v2 import Data, DataCollector



class MainWindow(QtWidgets.QMainWindow):    
    
    def __init__(self):
        # Create the main window
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #initial parameters
        self.UPDATE=0 #Sets whether new data should be loaded
        self.data=0 #Sets whether the data has been loaded
        self.threadpool = QtCore.QThreadPool()  
        self.threadpool.setMaxThreadCount(1)
        self.fitpool = QtCore.QThreadPool()  
        self.fitpool.setMaxThreadCount(1)
        
        #Pushbuttons
        self.ui.pushButton_stop.clicked.connect(self.STOP)
        self.ui.pushButton_start.clicked.connect(self.START)
        self.ui.pushButton_save.clicked.connect(self.SAVE)
        
        #Data collecting
        self.daq_updating()
        self.averaging()
        self.ui.Averages.valueChanged.connect(self.averaging)
        self.ui.SamplingRate.valueChanged.connect(self.daq_updating)
        self.ui.SamplingTime.valueChanged.connect(self.daq_updating)
        self.ui.Channel.valueChanged.connect(self.daq_updating)
        Data.start_acquire()

        
        self.ui.Updating_speed.valueChanged.connect(self.UpdatingSpeed)
        
        
        self.update = QtCore.QTimer()
        self.update.setInterval(int(self.ui.Updating_speed.value()*1e3))
        self.update.timeout.connect(self.Updating)
        self.update.start()
        
        self.update_data = QtCore.QTimer()
        self.update_data.setInterval(int(5))
        self.update_data.timeout.connect(self.data_runner)
        self.update_data.start()
        
        self.plot_data()

        
        
        #testing the fitting cababilities
        # self.x,self.y=testdata()
        
    def daq_updating(self):
        Data.samplerate = self.ui.SamplingRate.value()*1e6
        Data.time = self.ui.SamplingTime.value()*1e-3
        Data.channel = self.ui.Channel.value()
        Data.time_trace=np.array([])
        try:
            
            ns = int(Data.time*Data.samplerate)
            
            Data.adc.set_acquisition(channels=[Data.channel], 
                                terminations=["50"], 
                                fullranges=[2],
                                pretrig_ratio=0, 
                                nsamples=ns,
                                samplerate=Data.samplerate)
            
            
            Data.adc.set_trigger(mode="ext")
            time_trace = Data.adc.acquire()
            Data.ns = int(time_trace.shape[0])
            
            if Data.ns > 0:
                Data.freq = np.fft.fftfreq(Data.ns, d=1/Data.samplerate)[:int(Data.ns/2)]
            
        except:
            pass
        
    def averaging(self):
        Data.averages = self.ui.Averages.value()
    
    def Cap_updating(self,timer):
        self.ui.Updating_speed.setMinimum(timer) 
        
            
        
    def UpdatingSpeed(self,value):
        timer=int(value*1e3)
        self.update.setInterval(timer)
    
    def STOP(self):
        self.UPDATE=0
        self.data=0
        
    def START(self):
        self.UPDATE=1
    
    def data_runner(self):
        go_to_work = DataCollector()
        self.threadpool.start(go_to_work)
    
    def SAVE(self):
        if self.ui.Save_png.isChecked()==True:
            print("save_png")
        if self.ui.Save_fit.isChecked()==True:
            print("save_fit")
    
    
    def plot_data(self):
        self.ui.graphicsView.setDownsampling(auto=True)
# self.plotItem.removeItem(d["line"])
        self.ui.graphicsView.setLabel("left", "", units="")
        self.ui.graphicsView.setLabel("bottom", "Frequency", units="Hz")
        self.ui.graphicsView.showAxis("right")
        self.ui.graphicsView.showAxis("top")
        self.ui.graphicsView.getAxis("top").setStyle(showValues=False)
        self.ui.graphicsView.getAxis("right").setStyle(showValues=False)
        self.ui.graphicsView.setClipToView(True)

        self.ui.graphicsView.plotItem.setLogMode(False, True)  # Log y.
        self.ui.graphicsView.plotItem.showGrid(True, True)

        self.plot = self.ui.graphicsView.plot(pen=pg.mkPen('b', width=1))
        self.fit = self.ui.graphicsView.plot(pen=pg.mkPen(color=(0, 0, 0), width=3))
        self.guess = self.ui.graphicsView.plot(pen=pg.mkPen(color=(0, 100, 0), width=3))
    
    def Updating(self):
        
        if self.UPDATE==1:
            self.data=1
            self.x=Data.freq
            # print(self.x.shape)
            self.y=Data.rFFT
            # print(self.y)
            try:
                self.plot.setData(self.x,self.y)
            except:
                Data.ns = int(self.y.shape[0])*2
                if Data.ns > 0:
                    
                    Data.freq = np.fft.fftfreq(Data.ns, d=1/Data.samplerate)[:int(Data.ns/2)]
            else:
                pass
            
            averages = Data.averages
            if averages > 1:
                # self.ui.Fit_8.setPlainText("Averages:  " + "%d" %averages)
                pass
            else: 
                # self.ui.Fit_8.setPlainText("Averages:")
                pass
            
        if self.data==1:
            #Loading fit guess
            self.load()
            
            # Showing the fit
            # print(self.ui.Show_fit.isChecked())
            if self.ui.Show_fit.isChecked()==True:
                self.Start_fit()
            else:
                self.fit.setData([0,1],[0,0])
                pass
            
            #showing the initial guess
            if self.ui.Show_guess.isChecked()==True:
                self.Start_guess()
            else:
                self.guess.setData([0,1],[0,0])
                pass
            
            timer = Fit.timer
            self.ui.Fit_speed.setPlainText("%0.2f" %timer + "s")
            if self.ui.speed_limit.isChecked()==True:
                self.Cap_updating(timer)
            else:
                self.Cap_updating(0.01)
    
    

    def Start_fit(self):
        #fitting
        go_to_work = FitCollector()
        self.fitpool.start(go_to_work)
        

        #plotting fit
        if Fit.scaling != 0:
            # print(Fit.scaling)
            result = Fit.result
            scaling = Fit.scaling
            f = Fit.f_fit*1e3
            bestfit=result.best_fit*scaling
            
            try:
                self.fit.setData(f,bestfit)
            except:
                pass
            # A.setLogMode(False, True)
            params = result.params
            
            #Showing the polarization
            pol = Fit.spinpol(params['r'])*100
            self.ui.Polarization.setPlainText("Polarization:\n" + "%0.2f" %pol + "%")
            
            self.ui.r_fit.setPlainText("%0.2f" %params['r'])
            
            phi = params['phi']/np.pi
            self.ui.phi_fit.setPlainText("%0.2f" %phi + " pi")
            
            self.ui.A_fit.setPlainText("%0.2f" %params['A'])
            
            Gamma=params['G']*1e3
            self.ui.Gamma_fit.setPlainText("%0.0f" %Gamma + " Hz")
        
    def Start_guess(self):
        if Fit.scaling != 0:
            result = Fit.result
            scaling = Fit.scaling
            f = Fit.f_fit*1e3
            
            initfit=result.init_fit*scaling
            try:
                self.guess.setData(f,initfit)
            except:
                pass
    
    def load(self):
        Fit.data=self.y
        Fit.f=self.x/1e3
        Fit.center=self.ui.Center_freq.value()
        Fit.span=self.ui.Span_freq.value()
        Fit.A=self.ui.A_scroll.value()
        Fit.g=self.ui.Gamma_scroll.value()
        Fit.r=self.ui.r_scroll.value()
        Fit.n=self.ui.n_scroll.value();
        Fit.phi=self.ui.phi_scroll.value()


def testdata():
    global f, psd_EN, psd_SN_TH, psd_SN_G, psd_TH, psd_G, path
    f_step=1.826087*10
    def loaddata(f_step,file,path):
        global f, psd
        
        fi=open(path+file,'rb')
        L=np.fromfile(fi,'<i4',count=1)[0]
        psd=np.fromfile(fi,'<f8',count=L)
        fi.close()
        f=np.arange(len(psd))*f_step*1E-3
        return
    path=r'Z:\membrane\atom-membrane\data\2021\09\24\atomic_pol' + "\\"

    loaddata(f_step,"mors30.bin",path)
    return f, psd


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    l = pg.GraphicsLayout()
    l.layout.setContentsMargins(0, 0, 0, 0)
    
    app.lastWindowClosed.connect(app.exit)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
 