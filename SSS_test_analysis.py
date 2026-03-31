# -*- coding: utf-8 -*-
"""
SPEECH SYNCHRONY ANALYSIS

Analysis of the Speech Synchrony Test as described in Lizcano et al. 2022.
The script perfoms the following steps:
    (1) Extracts the envelope of the produced speech signal and filters it around the stimulus syllabic rate.
    (2) Computes the PLVs between the produced and perceived filtered envelopes, in windows of 5 secs length, with an overlap of 2 secs
    (3) Averages the PLVs within each audio file (i.e. run1 and run2)
    (4) Control for consistency between runs
    (5) Gives the probability of the participant of being a high or low synchronizer.

Original
@author: Cecilia Mares 2021 ceciliap.maresr@gmail.com

Adapted
@author: Carlos Magallanes-Aranda 2026 cmagallanx@gmail.com

"""

import funcs

def analyze(filename):
    
    #############################################################################################################
    # STEP 1: Loads the stimulus and both Runs of the subject's responses (signals)
    #############################################################################################################
    #fs, y   = funcs.read_WAV('stimulus_ExpAcc.wav')
    fs_h, h = funcs.read_WAV(filename)

    # Demeans and takes the envelope of the stimulus and of the spoken syllables
    #y_env  = funcs.gets_envelope(y)
    h_env = funcs.gets_envelope(h)

    # Applies a bandpass filter to the envelopes
    bp_freqs = [3.3, 5.7] # cut frequencies
    #y_env_filt  = funcs.filt_bandpass(y_env,  fs,    bp_freqs)
    h_env_filt = funcs.filt_bandpass(h_env, fs_h, bp_freqs)

    # Resamples the filtered envelopes
    fs_new = 100 # new sample frequency
    #y_env_filt_resamp  = funcs.resample(y_env_filt, fs, fs_new)
    h_env_filt_resamp = funcs.resample(h_env_filt, fs_h, fs_new)

    # Estimates the spectrum of the envelopes for visualization purposes.
    # xf1, yf1 = funcs.freqSpect(h_env_filt_resamp, fs_new)

    #############################################################################################################
    # STEP 2 & 3: Computes the PLV between the produced and perceived filtered envelopes
    #############################################################################################################
    #theta_y  = funcs.angles(y_env_filt_resamp)
    theta_y = funcs.np.load("theta_y.npy")
    theta_h = funcs.angles(h_env_filt_resamp)

    T = 5 # Size of window
    shift = 2 # Size of overlap

    plv_mean, plv, time = funcs.PLVevol(theta_y, theta_h, T, shift, fs_new)
    plv_mean = round(plv_mean, 2)

    return(str(plv_mean))

