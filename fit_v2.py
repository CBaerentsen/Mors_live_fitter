# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 13:42:28 2021

@author: chris
"""
from lmfit import Model, minimize
import numpy as np
from PyQt5 import QtCore
import time

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
    r=0
    n=0
    phi=0
    timer=0.01
    
    def C(n):
        result=[8,14,18,20,20,18,14,8]
        return result[n]
    
    def lorentzian(x,x0,G,d,n):
        return np.array(G/(d*n+x0-x-1j*G/2))
    
    def lorentzian2(x,x0,G,d,n):
        omega = (d*n+x0)
        return np.array(2*G*x0/(omega**2-x**2-1j*x*G+(G/2)**2))
    
    def phase(phi):
        return np.exp(-1j*phi)
    
    def population(r,n):
        return r**n-r**(n+1)
    
    def morsR(x,x0,r,phi,A,G,d,n,B):
        model=np.zeros(len(x))
        for i in range(n):
            model = model + A*Fit.C(i)*Fit.population(r,i)*Fit.phase(phi)*Fit.lorentzian(x,x0,G,d,i)
        
        model=np.real(model)
        model+=B
        
        return model
    
    def morsI(x,x0,r,phi,A,G,d,n,B):
        model=np.zeros(len(x))
        for i in range(n):
            model = model + A*Fit.C(i)*Fit.population(r,i)*Fit.phase(phi)*Fit.lorentzian(x,x0,G,d,i)
        
        model=np.Imag(model)
        model+=B
        
        return model
    
    
    def fitter():
        start = time.time()
        f_start = Fit.center-Fit.span
        f_end = Fit.center+Fit.span
        data_fit = Fit.data[(Fit.f>=f_start) & (Fit.f<=f_end)]
        f_fit = Fit.f[(Fit.f>=f_start) & (Fit.f<=f_end)]
        Fit.f_fit = f_fit
        scaling= np.average(data_fit)
        data_fit=data_fit/scaling
        
        w0 = f_fit[np.argmax(data_fit)]
        d=2*w0**2/9.19e6
        
        model = Model(Fit.morsR)
        model.set_param_hint('A', value=Fit.A,min=0)
        model.set_param_hint('phi', value=Fit.phi*np.pi,vary=True,min=-4*np.pi,max=4*np.pi)
        model.set_param_hint('dphi', value=0,vary=True)
        model.set_param_hint('x0', value=w0)
        model.set_param_hint('d', value=d, vary=True)
        model.set_param_hint('G', value=Fit.g, min=0)
        model.set_param_hint('r', value=Fit.r,min=0,max=1)
        model.set_param_hint('B', value=1,vary=True)
        model.set_param_hint('n', value=int(Fit.n),vary=False)


        sigma=np.sqrt(data_fit)
        weights=1/sigma**2
        
        # weights = 1/np.log(data_fit)
        
        # weights=np.ones(len(psd_new))
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
    
