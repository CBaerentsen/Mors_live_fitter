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
import pyqtgraph as pg
from fit import Fit, FitCollector
from data import Data, DataCollector



pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
l = pg.GraphicsLayout()
l.layout.setContentsMargins(0, 0, 0, 0)



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
        self.data_runner()
        
        # Spinbuttons 
        self.ui.End_freq.valueChanged.connect(self.fit_boundaries_End)
        self.ui.Start_freq.valueChanged.connect(self.fit_boundaries_Start)

        
        self.ui.Updating_speed.valueChanged.connect(self.UpdatingSpeed)
        
        
        self.update = QtCore.QTimer()
        self.update.setInterval(int(self.ui.Updating_speed.value()*1e3))
        self.update.timeout.connect(self.Updating)
        self.update.start()
        
        

        
        
        #testing the fitting cababilities
        # self.x,self.y=testdata()
        
    def daq_updating(self):
        Data.samplerate = self.ui.SamplingRate.value()
        Data.time = self.ui.SamplingTime.value()
        Data.channel = self.ui.Channel.value()
        Data.adc = []
        Data.error = 0
        
    def averaging(self):
        Data.averages = self.ui.Averages.value()
    
    def Cap_updating(self,timer):
        self.ui.Updating_speed.setMinimum(timer) 
        
    def fit_boundaries_End(self):
        if self.ui.End_freq.value()<self.ui.Start_freq.value():
            self.ui.Start_freq.setValue(self.ui.End_freq.value())

    def fit_boundaries_Start(self):
        if self.ui.End_freq.value()<self.ui.Start_freq.value():
            self.ui.End_freq.setValue(self.ui.Start_freq.value())
            
        
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
    
    def Updating(self):
        self.ui.graphicsView.clear()
        if self.UPDATE==1:
            self.data=1
            self.x=np.linspace(0,6,1000)
            self.y=np.random.rand(1000)
            self.ui.graphicsView.plot(self.x,self.y,pen=pg.mkPen('b', width=1))
            
        if self.data==1:
            #Loading fit guess
            self.load()
            
            # Showing the fit
            if self.ui.Show_fit.isChecked()==True:
                self.Start_fit()
            
            #showing the initial guess
            if self.ui.Show_guess.isChecked()==True:
                self.Start_guess()
            
            timer = Fit.timer
            self.ui.Fit_speed.setPlainText("%0.2f" %timer + "s")
            if self.ui.speed_limit.isChecked()==True:
                self.Cap_updating(timer)
            else:
                self.Cap_updating(0.01)
    
    

    def Start_fit(self):
        #fitting
        go_to_work = FitCollector()
        self.threadpool.start(go_to_work)
        

        #plotting fit
        if Fit.scaling != 0:
            result = Fit.result
            scaling = Fit.scaling
            f = Fit.f_fit
            bestfit=result.best_fit*scaling
            self.ui.graphicsView.plot(f,bestfit,pen=pg.mkPen(color=(0, 0, 0), width=3))
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
            f = Fit.f
            
            initfit=result.init_fit*scaling
            self.ui.graphicsView.plot(f,initfit,pen=pg.mkPen(color=(0, 100, 0), width=3))
    
    def load(self):
        Fit.data=self.y
        Fit.f=self.x
        Fit.start=self.ui.Start_freq.value()
        Fit.end=self.ui.End_freq.value()
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
    app.lastWindowClosed.connect(app.exit)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
 