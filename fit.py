# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 13:42:28 2021

@author: chris
"""
from lmfit import Model, minimize
import numpy as np
from PyQt5 import QtCore
import time
from data import Data, DataCollector

class FitCollector(QtCore.QRunnable):
    def __init__(self):
        super(FitCollector, self).__init__()
        
    def run(self):
        try:

            Fit.fitter()
        except Exception as e:
            print(e)



class Fit(object):
    result = []
    f_fit=[]
    scaling=0
    data=[]
    f=[]
    center=1000
    span=20
    A=0
    g=0
    data_imag = []
    r=0
    n=0
    B=0
    phi=0
    imag=False
    timer=0.01
    
    def C(n):
        result=[8,14,18,20,20,18,14,8]
        return result[n]
    
    def lorentzian(x,x0,G,d,n):
        return np.array(G/(d*n+x0-x-1j*G/2))
    
    def lorentzian2(x,x0,G,d,n):
        omega = (d*n+x0)
        return np.array(2*G*x0/(omega**2-x**2-1j*x*G+(G/2)**2))
    
    def phase(phi,i):
        if i==0:
            return np.exp(-1j*phi)
        else:
            return 1
    
    def population(r,n):
        return r**n-r**(n+1)
    
    
    def morsABS(x,x0,phi,A,d,n,B,G_0,G_1,G_2,G_3,G_4,G_5,G_6,G_7,A_0,A_1,A_2,A_3,A_4,A_5,A_6,A_7):
      
      model=np.zeros(len(x))
      for i in range(n):
          model = model + eval("A_%d"%i)*Fit.C(i)*Fit.phase(phi,i)*Fit.lorentzian(x,x0,eval("G_%d"%i),d,i)
          
      model=np.abs(model)
      model+=B
      
      return np.log10(model)
    
    def morsAngle(x,x0,phi,A,d,n,B,G_0,G_1,G_2,G_3,G_4,G_5,G_6,G_7,A_0,A_1,A_2,A_3,A_4,A_5,A_6,A_7,Angle):
      
      model=np.zeros(len(x))
      for i in range(n):
          model = model + eval("A_%d"%i)*Fit.C(i)*Fit.phase(phi,i)*Fit.lorentzian(x,x0,eval("G_%d"%i),d,i)
          
      model=np.angle(model*np.exp(-1j*Angle))
      
      return model
  
    def mors_ABS_Angle(x,x0,phi,A,d,n,B,G_0,G_1,G_2,G_3,G_4,G_5,G_6,G_7,A_0,A_1,A_2,A_3,A_4,A_5,A_6,A_7,Angle):
        x = np.array_split(x,2)
        R = Fit.morsABS(x[0],x0,phi,A,d,n,B,G_0,G_1,G_2,G_3,G_4,G_5,G_6,G_7,A_0,A_1,A_2,A_3,A_4,A_5,A_6,A_7)
        I = Fit.morsAngle(x[1],x0,phi,A,d,n,B,G_0,G_1,G_2,G_3,G_4,G_5,G_6,G_7,A_0,A_1,A_2,A_3,A_4,A_5,A_6,A_7,Angle)
        return np.hstack([R,I])
    
    def morsPSDthermal(x,x0,r,phi,A,d,n,B,G_0,G_1,G_2,G_3,G_4,G_5,A_0,A_1,A_2,A_3):
        
        model=np.zeros(len(x))
        for i in range(n):
            model = model + A*Fit.C(i)*Fit.population(r,i)*Fit.phase(phi,i)*Fit.lorentzian(x,x0,eval("G_%d"%i),d,i)
            
        model=np.abs(model)**2
        model+=B
        
        return np.log10(model)
    
    #A_0,A_1,A_2,A_3,A_4,A_5
    def morsPSD(x,x0,phi,A,d,n,B,G_0,G_1,G_2,G_3,G_4,G_5,G_6,G_7,A_0,A_1,A_2,A_3,A_4,A_5,A_6,A_7):
      
      model=np.zeros(len(x))
      for i in range(n):
          model = model + eval("A_%d"%i)*Fit.C(i)*Fit.phase(phi,i)*Fit.lorentzian(x,x0,eval("G_%d"%i),d,i)
          
      model=np.abs(model)**2
      model+=B
      
      return np.log10(model)
    
    def fitter():
        start = time.time()
        f_start = Fit.center-Fit.span
        f_end = Fit.center+Fit.span
        data_fit = Fit.data[(Fit.f>=f_start) & (Fit.f<=f_end)]
        f_fit = Fit.f[(Fit.f>=f_start) & (Fit.f<=f_end)]
        Fit.f_fit = f_fit
        
        scaling = np.average(data_fit[:100]+data_fit[-100:])/2
        data_fit=np.log10(data_fit/scaling)
        w0 = f_fit[np.argmax(data_fit)]
        d=2*w0**2/9.19e6
        if Fit.imag == True:
            data_fit_imag = Fit.data_imag[(Fit.f>=f_start) & (Fit.f<=f_end)]
            data_fit = np.hstack([data_fit,data_fit_imag])
            f_fit = np.hstack([f_fit,f_fit])

        
        

        if Fit.imag == False:
            model = Model(Fit.morsPSD)
        else:
            model = Model(Fit.mors_ABS_Angle)
            model.set_param_hint('Angle', value=0)
        model.set_param_hint('A', value=Fit.A,min=0)
        # for i in range(int(0)):
        #     A=Fit.A*Fit.population(Fit.r,i)
        #     model.set_param_hint('A_%d'%i, value=A, min=0)
            
        model.set_param_hint('phi', value=Fit.phi*np.pi,vary=True,min=-4*np.pi,max=4*np.pi)
        model.set_param_hint('dphi', value=0,vary=True)
        model.set_param_hint('x0', value=w0)
        model.set_param_hint('d', value=d, vary=True,min=d*0.5,max=d*1.5)
        for i in range(int(Fit.n)):
            if i<3:
                model.set_param_hint('G_%d'%i, value=Fit.g, min=0)
                
        for i in range(int(Fit.n)):
            model.set_param_hint('A_%d'%i, value=Fit.A*Fit.population(Fit.r,i)/Fit.population(Fit.r,0)*(i+1)**2, min=0)
        # model.set_param_hint('r', value=Fit.r,min=0,max=1)
        model.set_param_hint('B', value=Fit.B,vary=True,min=0)
        model.set_param_hint('n', value=int(Fit.n),vary=False)

        
        # sigma=np.sqrt(data_fit)
        # sigma = np.log(data_fit)
        # weights=1/sigma**1
        
        # weights = 1/np.log(data_fit)
        
        weights=np.ones(len(data_fit))
        Fit.result = model.fit(data_fit, x=f_fit,weights=weights)
        Fit.scaling = scaling
        end = time.time()
        Fit.timer=end-start+0.01
        
    def spinpol(r):
        F=4;
        S44=1./(1+r+r**2+r**3+r**4+r**5+r**6+r**7+r**8);
        m=np.linspace(4,-4,num=9)
        p=sum(m*r**(4-m))*S44/F
        return p
    
    def spinpol3peak(n=0,A_0=0,A_1=0,A_2=0,A_3=0,A_4=0,A_5=0,A_6=0):
    
        norm = 0
        vec = np.arange(int(n))
        S=np.zeros(int(n))
        
        for i in range(int(n)):
            S[i] = eval("A_%d"%i)
            norm += eval("A_%d"%i)*(i+1)
        
        sig = []
        for i in range(int(n)):
            sig.append(np.sum(S[i:])*(4-i))
            
        p = 1/4 * np.sum(sig)/norm
            
        return p
