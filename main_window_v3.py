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
from fit_v3 import Fit, FitCollector
from data_v3 import Data, DataCollector
import h5py
from datetime import datetime

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
        self.update_data.setInterval(0)
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
            
            Data.ns = int(Data.time*Data.samplerate)
            
            Data.adc.set_acquisition(channels=[Data.channel], 
                                terminations=["50"], 
                                fullranges=[2],
                                pretrig_ratio=0, 
                                nsamples=Data.ns,
                                samplerate=Data.samplerate)
            
            
            Data.adc.set_trigger(mode="ext")
            Data.adc.acquire()
            time_trace = Data.adc.acquire()
            Data.ns = int(time_trace.shape[0])
            
            if Data.ns > 0:
                Data.freq = np.fft.fftfreq(Data.ns, d=1/Data.samplerate)[:int(Data.ns/2)]
            
        except:
            pass
        
    def averaging(self):
        Data.averages = self.ui.Averages.value()
        
        
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
        # file = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        file = str(QtWidgets.QFileDialog.getSaveFileName(self, "Select Directory")[0])
        print(file)
        if self.ui.Save_png.isChecked()==True:
            print("save_png")
            app = QtWidgets.QApplication(sys.argv)
            QtGui.QScreen.grabWindow(app.primaryScreen(),
            QtWidgets.QApplication.desktop().winId()).save(file+".png", 'png')
               
            # Saves the data in an HDF5 file in the current directory 
            file_name = file + str(datetime.now()).replace(':', '-') + " demod.h5"
            with h5py.File(file_name, "w") as f:
                f["ydata"] = np.array(self.y)
                f["ydata"].attrs["xmin"] = 0
                f["ydata"].attrs["samplerate"] = Data.samplerate
                f["ydata"].attrs["number of samples"] = Data.ns
                f["xdata"] = np.array(self.x)

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
        # self.ui.graphicsView.plotItem.vb.setLimits(xMin=1, xMax=1e8, yMin=0, yMax=1e8)

        self.plot = self.ui.graphicsView.plot(pen=pg.mkPen('b', width=1))
        self.fit = self.ui.graphicsView.plot(pen=pg.mkPen(color=(0, 0, 0), width=3))
        self.guess = self.ui.graphicsView.plot(pen=pg.mkPen(color=(0, 100, 0), width=3))
        
        
        #scope
        self.ui.graphicsViewScope.setDownsampling(auto=True)
        # self.plotItem.removeItem(d["line"])
        self.ui.graphicsViewScope.setLabel("left", "", units="")
        self.ui.graphicsViewScope.setLabel("bottom", "", units="")
        self.ui.graphicsViewScope.showAxis("right")
        self.ui.graphicsViewScope.showAxis("top")
        self.ui.graphicsViewScope.getAxis("top").setStyle(showValues=False)
        self.ui.graphicsViewScope.getAxis("right").setStyle(showValues=False)
        self.ui.graphicsViewScope.setClipToView(True)

        self.ui.graphicsViewScope.plotItem.showGrid(True, True)

        self.scope = self.ui.graphicsViewScope.plot(pen=pg.mkPen('b', width=1))
        self.scope_fit = self.ui.graphicsViewScope.plot(pen=pg.mkPen(color=(0, 0, 0), width=3))
        self.scope_guess = self.ui.graphicsViewScope.plot(pen=pg.mkPen(color=(0, 100, 0), width=3))
    
    def Updating(self):
        
        if self.UPDATE==1:
            self.data=1
            if self.ui.Show_R_I.isChecked()==False:
                self.x=Data.freq
                # print(self.x.shape)
                self.y=Data.PSD
                
                # print(self.y)
                try:
                    self.plot.setData(self.x,self.y)
                except:
                    Data.ns = int(self.y.shape[0])*2
                    if Data.ns > 0:
                        
                        Data.freq = np.fft.fftfreq(Data.ns, d=1/Data.samplerate)[:int(Data.ns/2)]
                else:
                    pass
                
                #scope
                
                    if self.ui.Show_scope.isChecked()==True:
                        self.y_scope = Data.avg_time_trace
                        try:
                            self.scope.setData(self.x_scope,self.y_scope)
                        except:
                            self.x_scope = np.linspace(0,Data.time,Data.ns)
                        else:
                            pass
            # Plotting real and imaginary part
            else:
                self.x=Data.freq
                self.x_scope=Data.freq
                # print(self.x.shape)
                self.y = Data.abs
                self.y_scope = Data.angle
                
                # print(self.y)
                try:
                    self.plot.setData(self.x,self.y)
                    self.scope.setData(self.x_scope,self.y_scope)
                except:
                    Data.ns = int(self.y.shape[0])*2
                    if Data.ns > 0:
                        
                        Data.freq = np.fft.fftfreq(Data.ns, d=1/Data.samplerate)[:int(Data.ns/2)]
                else:
                    pass
            
            
            averages = Data.total_averages
            if averages > 1:
                self.ui.Fit_8.setText("Averages:  " + "%d" %averages)
                pass
            else: 
                self.ui.Fit_8.setText("Averages:")
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
    
    

    def Start_fit(self):
        #fitting
        go_to_work = FitCollector()
        self.fitpool.start(go_to_work)
        

        #plotting fit
        if self.ui.Show_fit.isChecked()==True and Fit.scaling != 0:
            # print(Fit.scaling)
            result = Fit.result
            scaling = Fit.scaling
            f = Fit.f_fit*1e3
            if self.ui.Show_R_I.isChecked()==True:
                bestfit=np.array_split(10**(result.best_fit)*scaling,2)[0]
                bestfit_scope = np.array_split(result.best_fit,2)[1]
                try:
                    self.scope_fit.setData(f,bestfit_scope)
                except:
                    pass
                    
            else:
                bestfit=10**(result.best_fit)*scaling
            try:
                self.fit.setData(f,bestfit)
            except:
                pass
            # A.setLogMode(False, True)
            params = result.params
            
            #Showing the polarization
            # pol = Fit.spinpol(params['r'])*100
            A=[]
            
            func = "Fit.spinpol3peak(Fit.n"
            for i in range(int(Fit.n)):
                  A.append(params["A_%d"%i])
                  func += ",A[%d]"%i
            
            pol = eval(func + ")*100")
            self.ui.Polarization.setPlainText("Polarization:\n" + "%0.2f" %pol + "%")
            
            # self.ui.r_fit.setPlainText("%0.2f" %params['r'])
            
            phi = params['phi']/np.pi
            self.ui.phi_fit.setPlainText("%0.2f" %phi + " pi")
            
            self.ui.A_fit.setPlainText("%0.2f, " %params['A_0'] + "%0.2f" %params['A_1'])
            
            Gamma=params['G_0']*1e3
            Gamma1=params['G_1']*1e3
            self.ui.Gamma_fit.setPlainText("%0.0f, " %Gamma + "%0.0f Hz" %Gamma1)
            
            B=params['B']
            self.ui.B_fit.setPlainText("%0.2f" %B)
        
    def Start_guess(self):
        if self.ui.Show_fit.isChecked()==True and Fit.scaling != 0:
            result = Fit.result
            scaling = Fit.scaling
            f = Fit.f_fit*1e3
            if self.ui.Show_R_I.isChecked()==True:
                initfit=np.array_split(10**(result.init_fit)*scaling,2)[0]
            else:
                initfit=10**(result.init_fit)*scaling
            try:
                self.guess.setData(f,initfit)
            except:
                pass
    
    def load(self):
        
        Fit.data = self.y
        if self.ui.Show_R_I.isChecked() == True:
            Fit.data=Data.abs
        Fit.data_imag=Data.angle
        Fit.imag = self.ui.Show_R_I.isChecked()
        Fit.f=self.x/1e3
        Fit.center=self.ui.Center_freq.value()
        Fit.span=self.ui.Span_freq.value()
        Fit.A=self.ui.A_scroll.value()
        Fit.g=self.ui.Gamma_scroll.value()*1e-3
        Fit.r=self.ui.r_scroll.value()
        Fit.n=self.ui.n_scroll.value();
        Fit.phi=self.ui.phi_scroll.value()
        Fit.B=self.ui.B_scroll.value()


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
 