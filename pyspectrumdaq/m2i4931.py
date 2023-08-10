# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division


import sys
import numpy as np
import numba
from enum import Enum

import time

# import spectrum driver functions
import pyspectrumdaq.Spectrum_M2i4931_pydriver.pyspcm as sp
    
class CardError(Exception):
    """ Base class for card errors """
    
class CardInaccessibleError(CardError):
    pass

class CardIncompatibleError(CardError):
    pass

# Function for card name translation
def szTypeToName (lCardType):
    sName = ''
    lVersion = (lCardType & sp.TYP_VERSIONMASK)
    if (lCardType & sp.TYP_SERIESMASK) == sp.TYP_M2ISERIES:
        sName = 'M2i.%04x'%lVersion
    elif (lCardType & sp.TYP_SERIESMASK) == sp.TYP_M2IEXPSERIES:
        sName = 'M2i.%04x-Exp'%lVersion
    elif (lCardType & sp.TYP_SERIESMASK) == sp.TYP_M3ISERIES:
        sName = 'M3i.%04x'%lVersion
    elif (lCardType & sp.TYP_SERIESMASK) == sp.TYP_M3IEXPSERIES:
        sName = 'M3i.%04x-Exp'%lVersion
    elif (lCardType & sp.TYP_SERIESMASK) == sp.TYP_M4IEXPSERIES:
        sName = 'M4i.%04x-x8'%lVersion
    elif (lCardType & sp.TYP_SERIESMASK) == sp.TYP_M4XEXPSERIES:
        sName = 'M4x.%04x-x4'%lVersion
    else:
        sName = 'unknown type'
    return sName

def chan_from_num(chan_n):
    return getattr(sp, "CHANNEL{0:d}".format(int(chan_n)))
    
@numba.jit(nopython=True, parallel=True)            
def _convert(out, x, convs):
    """ Convert a int16 2D numpy array (N, ch) into a 2D float64 array with 
    some conversion factors. Uses preallocated arrays
    """
    for ch in numba.prange(out.shape[1]):
        for n in numba.prange(out.shape[0]):
            out[n, ch] = x[n, ch] * convs[ch]

class Card(object):
    def _get32(self, param, uint=False):
        if not uint:
            destination = sp.int32(0)
        else:
            destination = sp.int32(0)
        sp.spcm_dwGetParam_i32(self._hCard, param, sp.byref(destination))
        return destination
    
    def _set32(self, param, val, uint=False):
        val = int(val)
        if not uint:
            return sp.spcm_dwSetParam_i32(self._hCard, param, sp.int32(val))
        else:
            return sp.spcm_dwSetParam_i32(self._hCard, param, sp.uint32(val))
    
    def _set64(self, param, val, uint=False):
        val = int(val)
        if not uint:
            return sp.spcm_dwSetParam_i64(self._hCard, param, sp.int64(val))
        else:
            return sp.spcm_dwSetParam_i64(self._hCard, param, sp.uint64(val))
    
    # Connect to DAQ card
    def __init__(self):
        # Open card
        self._hCard = sp.spcm_hOpen("/dev/spcm0")
        if self._hCard == None:
            msg = "Card not found or not accessible. Try closing other software that might be using it"
            raise CardInaccessibleError(msg)

        # read type, function and sn and check for A/D card
        lCardType = self._get32(sp.SPC_PCITYP)
        lSerialNumber = self._get32(sp.SPC_PCISERIALNO)
        lFncType = self._get32(sp.SPC_FNCTYPE)

        sCardName = szTypeToName(lCardType.value)
        if lFncType.value == sp.SPCM_TYPE_AI:
            print("Found: {0} sn {1:05d}".format(sCardName,lSerialNumber.value))
        else:
            msg = "Card is inaccessible (try closing other apps) or not supported"
            raise CardIncompatibleError(msg)

        # Reset the card to prevent undefined behaviour
        self.reset()
        
        # Create a set of conversions: factors for converting between ADC 
        # values and voltages (for all enabled channels)
        self._conversions = np.zeros(4)

    # Close connection to DAQ card
    def close(self):
        sp.spcm_vClose(self._hCard)

    # Reset the card to default settings
    def reset(self):
        sp.spcm_dwSetParam_i32(self._hCard, sp.SPC_M2CMD, sp.M2CMD_CARD_RESET)
        
    def __enter__(self):
        self.reset()
        return self
    
    def __exit__(self, *a):
        self.close()
        
    """
    Initialize channels.
    ch_nums is a list of channel numbers to initialize
    terminations is a list of terminations to use with these channels
    fullranges is a list of ranges for these channels
    The three lists have to have the same length
    """
    def ch_init(self, ch_nums=[1], terminations=["1M"], 
                fullranges=[10]):
        
        # Check that the channel numbers are correct
        if not all([(ch_n in range(4)) for ch_n in ch_nums]):    
            raise ValueError("Some channel numbers are invalid")
            
        # Enable these channels by creating a CHENABLE mask and applying it
        chan_mask = 0
        
        for ch_n in ch_nums:
            chan_mask |= getattr(sp, "CHANNEL{0:d}".format(int(ch_n)))
            
        self._set32(sp.SPC_CHENABLE, chan_mask)
        
        for ch_n, termination, fullrange in zip(ch_nums, terminations, 
                                                fullranges):
            ch_n = int(ch_n)
            fullrange = int(fullrange * 1000)
            
            if fullrange in [200,500,1000,2000,5000,10000]:
                range_param = getattr(sp, "SPC_AMP{0:d}".format(int(ch_n)))
                self._set32(range_param, fullrange); 
                
                
                maxadc = self._get32(sp.SPC_MIINST_MAXADCVALUE)
                self._maxadc = maxadc.value
                
                conversion = float(fullrange)/1000 / self._maxadc
                self._conversions[ch_n] = conversion
            else:
                raise ValueError("The specified voltage range is invalid")
            
            if termination == "1M":
                term_val = 0
            elif termination == "50":
                term_val = 1
            else:
                raise ValueError("The specified termination is invalid")
                
            term_param = getattr(sp, "SPC_50OHM{0:d}".format(int(ch_n)))
            self._set32(term_param, term_val)
            
            #print(f"Channel {ch_n} set up")

    '''
    Specify number of samples (per channel).
    Samplerate in Hz.
    Timeout in ms.
    Specify channel number as e.g. 0, 1, 2 or 3.
    Fullrange is in V has to be equal to one of {0.2, 0.5, 1, 2, 5, 10}.
    Termination is equal to 1 for 50 Ohm and 0 for 1 MOhm
    '''            
    # Initializes acquisition settings
    def acquisition_set(self, channels=[1], Ns=300e3, samplerate=30e6, 
                        timeout=10, fullranges=[10], 
                        terminations=["1M"], pretrig_ratio=0):
        
        if len(channels) not in [1, 2, 4]:
            raise ValueError("Number of activated channels should be 1, 2 or 4 only")
            
        timeout *= 1e3 # Convert to ms
        self.Ns = int(Ns)
        if self.Ns % 4 != 0:
            raise ValueError("Number of samples should be divisible by 4")
        self.samplerate = int(samplerate)
        
        #self.N_acq_channels = len(channels)
        
        # Sort all the arrays
        sort_idx = np.argsort(channels)
        self._acq_channels = np.array(channels)[sort_idx]
        terminations = np.array(terminations)[sort_idx]
        fullranges = np.array(fullranges)[sort_idx]
        
        if Ns / samplerate >= timeout:
            raise ValueError("Timeout is shorter than acquisition time")
        
        # Settings for the DMA buffer
        # Buffer size in bytes. Enough memory samples with 2 bytes each
        self._qwBufferSize = sp.uint64(self.Ns * 2 * len(self._acq_channels)); 
        
        # Driver should notify program after all data has been transfered
        self._lNotifySize = sp.int32(0); 

        # Set number of samples per channel
        self._set32(sp.SPC_MEMSIZE, self.Ns)
        
        # Setting the posttrigger value which has to be a multiple of 4
        pretrig = np.clip(((self.Ns * pretrig_ratio) // 4) * 4, 4, self.Ns - 4)
        self._set32(sp.SPC_POSTTRIGGER, self.Ns - int(pretrig))
        
        # Single trigger, standard mode
        self._set32(sp.SPC_CARDMODE, sp.SPC_REC_STD_SINGLE)
        
        # Set timeout value
        self._set32(sp.SPC_TIMEOUT, int(timeout))
        
        # Set internal clock
        #sp.spcm_dwSetParam_i32 (self._hCard, sp.SPC_CLOCKMODE,      sp.SPC_CM_INTPLL)         # clock mode internal PLL
        
        # Set external reference lock with 10 MHz frequency
        self._set32(sp.SPC_CLOCKMODE, sp.SPC_CM_EXTREFCLOCK)
        self._set32(sp.SPC_REFERENCECLOCK, 10000000)
        
        # Set the sampling rate
        self._set64(sp.SPC_SAMPLERATE, self.samplerate)
        

        # Choose channel
        self.ch_init(self._acq_channels, terminations, fullranges)

        # define the data buffer
        # we try to use continuous memory if available and big enough
        self._pvBuffer = sp.c_void_p()
        self._qwContBufLen = sp.uint64(0)
        sp.spcm_dwGetContBuf_i64 (self._hCard, 
                                  sp.SPCM_BUF_DATA, 
                                  sp.byref(self._pvBuffer), 
                                  sp.byref(self._qwContBufLen))
        #sys.stdout.write ("ContBuf length: {0:d}\n".format(self._qwContBufLen.value))
        if self._qwContBufLen.value >= self._qwBufferSize.value:
            sys.stdout.write("Using continuous buffer\n")
        else:
            self._pvBuffer = sp.create_string_buffer(self._qwBufferSize.value)

        sp.spcm_dwDefTransfer_i64 (self._hCard, sp.SPCM_BUF_DATA, 
                                   sp.SPCM_DIR_CARDTOPC, self._lNotifySize, 
                                   self._pvBuffer, sp.uint64(0), 
                                   self._qwBufferSize)

    def trigger_set(self, mode="soft", channel=0, edge="pos", level=0):
        """
        Set triggering mode. Can be either "software", i.e. immediate free-run,
        or on a rising or falling edge of one of the channels
        """
        if mode == "soft":
            # Trigger set to software
            self._set32(sp.SPC_TRIG_ORMASK, sp.SPC_TMASK_SOFTWARE)
            self._set32(sp.SPC_TRIG_ANDMASK, 0)
            return
            
        elif mode == "chan":
            # The division by 4 is necessary because the trigger has 14-bit 
            # resolution as compared to overall 16-bit resolution of the card
            trigvalue = int(level/self._conversions[channel]/4)
            
            # Check that the trigger level is within specified levels
            if abs(trigvalue) >= self._maxadc/4:
                raise ValueError("The specified trigger level is outside allowed values")
            
            # Disable all other triggering
            self._set32(sp.SPC_TRIG_ORMASK, 0)
            self._set32(sp.SPC_TRIG_ANDMASK, 0)
            self._set32(sp.SPC_TRIG_CH_ORMASK1, 0)
            self._set32(sp.SPC_TRIG_CH_ANDMASK1, 0)
            
            # Enable the required trigger
            maskname = "SPC_TMASK0_CH{0:d}".format(int(channel))
            chmask = getattr(sp, maskname)
            self._set32(sp.SPC_TRIG_CH_ORMASK0, chmask)
            
            # Mode is set to the required one
            modereg_name = "SPC_TRIG_CH{0:d}_MODE".format(int(channel))
            modereg = getattr(sp, modereg_name)
            if edge == "pos":
                pass
                self._set32(modereg, sp.SPC_TM_POS)
            elif edge == "neg":
                pass
                self._set32(modereg, sp.SPC_TM_NEG)
            else:
                raise ValueError("Incorrect edge specification")
                
            # Finally, set the trigger level
            levelreg_name = "SPC_TRIG_CH{0:d}_LEVEL0".format(int(channel))
            levelreg = getattr(sp, levelreg_name)
            self._set32(levelreg, trigvalue)

    '''
    Acquire time trace without time axis
    '''
    def acquire(self, convert=True):
        # Setup memory transfer parameters
        sp.spcm_dwDefTransfer_i64 (self._hCard, sp.SPCM_BUF_DATA, 
                                   sp.SPCM_DIR_CARDTOPC, 
                                   self._lNotifySize, self._pvBuffer, 
                                   sp.uint64(0), self._qwBufferSize)
        
        # Start card, enable trigger and wait until the acquisition has finished
        start_cmd = sp.M2CMD_CARD_START | sp.M2CMD_CARD_ENABLETRIGGER |\
        sp.M2CMD_CARD_WAITREADY | sp.M2CMD_DATA_STARTDMA | \
        sp.M2CMD_DATA_WAITDMA
        dwError = self._set32(sp.SPC_M2CMD, start_cmd)
        
        
        # check for error
        szErrorTextBuffer = sp.create_string_buffer(sp.ERRORTEXTLEN)
        if dwError != sp.ERR_OK:
            sp.spcm_dwGetErrorInfo_i32 (self._hCard, None, None, 
                                        szErrorTextBuffer)
            print("{0}\n".format(szErrorTextBuffer.value))
            self.close()
            exit()

        # Wait until acquisition has finished, then return data
        # Cast data pointer to pointer to 16bit integers
        pnData = sp.cast(self._pvBuffer, sp.ptr16) 
        
        # Convert the array of data into a numpy array
        # The array is already properly ordered, so we can already
        # give it the right shape
        Nch = len(self._acq_channels)
        data = np.ctypeslib.as_array(pnData, shape=(self.Ns, Nch))
        
        # Conversion factors for active channels
        conv_out = [self._conversions[ch_n] for ch_n in self._acq_channels]
        
        if convert:
            out = np.zeros((self.Ns, Nch), dtype=np.float64)
#            for i, ch_n in enumerate(self._acq_channels):
#                out[:,i] = out[:,i]*self._conversions[ch_n]
            return out
            
        # Return a copy of the array to prevent it from being
        # overwritten by DMA
        if not convert:
            return (conv_out, data.copy())
        else:
            _convert(out, data, conv_out)
            return out

if __name__ == '__main__':
    with Card() as adc:
        adc.acquisition_set(channels=[0, 1, 2, 3], 
                            terminations=["1M", "1M", "50", "1M"], 
                            fullranges=[2, 2, 2, 2],
                            pretrig_ratio=0, 
                            Ns=10**6,
                            samplerate=10**6)             
        adc.trigger_set(mode="soft")
        
        a = adc.acquire()
        print(a[0])
