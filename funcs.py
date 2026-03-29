# -*- coding: utf-8 -*-
"""

SPEECH SYNCHRONY ANALYSIS FUNCTIONS

Analysis of the Speech Synchrony Test as described in Lizcano et al. 2022.
The description of each function is explained below.

Original
@author: Cecilia Mares 2021 ceciliap.maresr@gmail.com

Adapted
@author: Carlos Magallanes-Aranda 2026 cmagallanx@gmail.com

"""

import numpy as np
from scipy import signal
from scipy.signal import hilbert
from scipy.fft import fft, fftfreq
import scipy.io.wavfile as wavfile
from scipy.stats import norm

def read_WAV(file_name):
    '''
    

    Parameters
    ----------
    file_name : Name of WAV file

    Returns
    -------
    fs : Sample frequency of WAV file.
    y : Array with data in WAV file.

    '''
    fs, y = wavfile.read(file_name)  
    return fs, y

def gets_envelope(y):
    '''
    

    Parameters
    ----------
    y : Signal.

    Returns
    -------
    envelope : Envelope of signal.

    '''
    envelope = np.abs(hilbert(y))
    envelope = envelope - np.mean(envelope)
    return envelope

def filt_bandpass(y,fs_ent,bp_freqs):
    '''
    

    Parameters
    ----------
    y : Signal.
    fs_ent : Sample frequency of signal.
    bp_freqs : cut frequencies of bandpass filter.

    Returns
    -------
    y_filt : signal filtered.

    '''
    sos = signal.butter(5, bp_freqs, btype='bandpass', analog=False, output='sos',fs=fs_ent)
    y_filt = signal.sosfilt(sos, y)
    return y_filt

def resample(y, fs_old, fs_new):
    '''
    

    Parameters
    ----------
    y : Signal.
    fs_old : Old sample frequency.
    fs_new : New sample frequency.

    Returns
    -------
    y_resampled : Signal resampled.

    '''
    y_resampled = y[::int(fs_old/fs_new)]
    return y_resampled

def freqSpect(y, fs):
    '''
    

    Parameters
    ----------
    y : Signal.
    fs : Sample frequency of signal.

    Returns
    -------
    xf : Vector of frequencies.
    yf : Power of signal.

    '''
    y = y - np.mean(y)
    N = len(y)
    Ts = 1.0 / fs
    
    yf = fft(y)
    xf = fftfreq(N, Ts)[:N//2]
    
    index10 = np.where(xf <= 10)
    xf = xf[index10]
    yf = yf[index10]
    
    yf = np.power(np.abs(yf),2)
    yf = yf / max(yf)
    
    return xf, yf

def angles(y):
    '''
    

    Parameters
    ----------
    y : Signal.

    Returns
    -------
    theta : Angles' vector.

    '''
    yy = hilbert(y)
    theta = np.unwrap(np.angle(yy))
    return theta

def PLVevol(theta_stim, theta_sign, T, shift, fs):
    '''

    Parameters
    ----------
    theta_stim : Angles' vector of the stimulus.
    theta_sign : Angles' vector of the signal.
    T : Size of window.
    shift : Size of overlap.
    fs : Sample frequency.

    Returns
    -------
    plv : Phase Locking Value between stimulus and signal.
    time : Timing vector.

    '''
    tmp = min(len(theta_stim), len(theta_sign))
    phase_diff = theta_stim[0:tmp] - theta_sign[0:tmp]
    duration = tmp / fs
    
    nT = round(fs*T)
    nshift = round(fs*shift)
    n_ant = 0
    i = 0
    
    time = np.empty(int(duration * fs / nshift))
    plv = np.empty(int(duration * fs / nshift))

    
    while (n_ant + nT) <= len(phase_diff):
        plv[i] = np.abs(np.sum(np.exp(1j*phase_diff[n_ant : n_ant + nT])))/ nT
        time[i] = 0.5 * (n_ant + n_ant + nT) / fs
        n_ant += nshift
        i += 1

    if (n_ant + nT) > len(phase_diff):
        plv[i] = np.abs(np.sum(np.exp(1j*phase_diff[n_ant:]))) / (len(phase_diff) - n_ant)
        time[i] = 0.3 * (len(phase_diff) + n_ant) / fs
       
    plv_mean = np.mean(plv)

    return plv_mean, plv, time
 