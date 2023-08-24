# Mors_live_fitter

Presents a graphical interface for live analyzing the pumping polarization of a magneto-optical resonance signal, where the signal is digitalized using Spectrum M2 digitizer card.
![MORS_D2_as_pump_D1_as_repump](https://github.com/CBaerentsen/Mors_live_fitter/assets/72730865/c159aef2-96d9-4429-b619-b592cf1143c4)

Run "main_window.py" to start the program. It is important to send triggering pulses to the DAQ card in order to receive data as it is programmed:

""

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

""
    
