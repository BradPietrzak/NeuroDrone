from typing import Any

import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist: float | Any = 0.5 * fs
    low: float | Any = lowcut / nyquist
    high: float | Any = highcut / nyquist
    # Design Butterworth filter
    b, a = butter(order, [low, high], btype='band')

    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    # Apply zero-phase filter
    y = filtfilt(b, a, data)
    return y

#Simulated EEG data
fs = 256  # Sampling frequency in Hz
t = np.linspace(0, 1.0, fs)
raw_eeg_data = np.sin(2 * np.pi * 10 * t)  # 10 Hz sine wave (alpha band)

#Add noise
noise = 0.5 * np.random.randn(len(t))
raw_eeg_data += noise

#Filter parameters
lowcut = 8.0   # Lower frequency for alpha band
highcut = 12.0  # Upper frequency for alpha band

#Apply band-pass filter
filtered_data = bandpass_filter(raw_eeg_data, lowcut, highcut, fs, order=4)

#Plotting
plt.figure(figsize=(12, 6))
plt.subplot(2,1,1)
plt.plot(t, raw_eeg_data)
plt.title('Raw EEG Data with Noise')
plt.subplot(2,1,2)
plt.plot(t, filtered_data, color='orange')
plt.title('Filtered EEG Data (Alpha Band)')
plt.tight_layout()
plt.show()