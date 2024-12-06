import json
import numpy as np
import mne
import matplotlib.pyplot as plt

# Load JSON file
file_path = r"C:\Users\bradp\PycharmProjects\relearning python\BrainDroneInterface\brainData\merged_data_UP.json"
with open(file_path, 'r') as file:
    data = json.load(file)

# Convert data to numpy arrays of floats
data = [np.array(channel, dtype=float) for channel in data]

# Ensure equal lengths by padding shorter channels
max_len = max(len(channel) for channel in data)
data_padded = [np.pad(channel, (0, max_len - len(channel)), mode='constant') for channel in data]
eeg_data = np.vstack(data_padded)

# Metadata
sampling_frequency = 256  # in Hz
channel_names = ["CP3", "C3", "F5", "PO3", "PO4", "F6", "C4", "CP4"][:eeg_data.shape[0]]
channel_types = ['eeg'] * len(channel_names)

# Create MNE Info object
info = mne.create_info(ch_names=channel_names, sfreq=sampling_frequency, ch_types=channel_types)

# Create Raw object
raw = mne.io.RawArray(eeg_data, info)

# Set the montage (standard 10-20 system)
montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage)

raw.filter(l_freq=0.02, h_freq=40.0)
raw.notch_filter(freqs=60.0)
# Plot the EEG data (all channels)
raw.plot(n_channels=len(channel_names), duration=5, start=0, scalings='auto', title='EEG Channels', show=True, block=True)

# Plot the F5 channel separately
raw.plot(picks=['F5'], duration=5, start=0, scalings='auto', title='F5 Channel', show=True, block=True)

# Define the time vector for plotting
times = np.arange(eeg_data.shape[1]) / sampling_frequency


plt.figure(figsize=(15, 6))
for i, channel_data in enumerate(eeg_data):
    plt.plot(times, channel_data, label=channel_names[i], alpha=0.8)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('EEG Channels Overlaid')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()
