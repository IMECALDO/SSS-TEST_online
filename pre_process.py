import funcs

fs, y   = funcs.read_WAV('stimulus_ExpAcc.wav')

y_env  = funcs.gets_envelope(y)

bp_freqs = [3.3, 5.7] # cut frequencies

y_env_filt  = funcs.filt_bandpass(y_env,  fs,    bp_freqs)

fs_new = 100 # new sample frequency

y_env_filt_resamp  = funcs.resample(y_env_filt, fs, fs_new)

theta_y  = funcs.angles(y_env_filt_resamp)

theta_y = funcs.np.array(theta_y)

funcs.np.save("theta_y.npy", theta_y)

theta_y = funcs.np.load("theta_y.npy")

