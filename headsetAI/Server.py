
from flask import Flask, jsonify
from flask_socketio import SocketIO
from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch
from tensorflow.keras.models import load_model
import time
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load your pre-trained model
model = load_model('eeg_cnn_lstm_model.h5')
logging.info("Model loaded successfully.")

# Initialize Neurosity SDK and login
neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

def collect_and_process_eeg_data(duration=5):
    """
    Collects EEG data for a specified duration and processes it for prediction.

    Parameters:
    - duration: Time in seconds to collect EEG data.

    Returns:
    - reshaped_data: NumPy array ready for model prediction.
    """
    all_brain_data = []

    def callback(data):
        all_brain_data.append(data)

    # Subscribe to raw brainwave data
    unsubscribe = neurosity.brainwaves_raw_unfiltered(callback)
    logging.info("Started collecting EEG data.")

    # Collect data for the specified duration
    time.sleep(duration)

    # Unsubscribe to stop data collection
    try:
        unsubscribe()
        logging.info("Stopped collecting EEG data.")
    except AttributeError as e:
        logging.error(f"Error while unsubscribing: {e}")

    if not all_brain_data:
        logging.error("No EEG data collected.")
        return None

    # Merge and process data
    merged_data = merge_json_data(all_brain_data)
    eeg_array = np.array(merged_data, dtype=np.float64)
    normalized_data = process_eeg_data(eeg_array)

    # Ensure data has the correct shape
    desired_length = 1280  # Adjust based on your model's input requirements
    current_length = normalized_data.shape[1]

    if current_length < desired_length:
        pad_width = desired_length - current_length
        normalized_data = np.pad(normalized_data, ((0, 0), (0, pad_width)), mode='constant', constant_values=0)
    elif current_length > desired_length:
        normalized_data = normalized_data[:, :desired_length]

    reshaped_data = reshape_eeg_data(normalized_data)
    return reshaped_data

def merge_json_data(json_data):
    """
    Merges raw EEG data into a 2D list with 8 channels.

    Parameters:
    - json_data: List of JSON objects containing EEG data.

    Returns:
    - merged_data: List of lists with merged EEG data per channel.
    """
    merged_data = [[] for _ in range(8)]
    for data_set in json_data:
        for i, channel_data in enumerate(data_set.get("data", [])[:8]):
            merged_data[i].extend(channel_data[:16])
    return merged_data

def process_eeg_data(eeg_data, fs=256, lowcut=0.02, highcut=40.0, notch_freq=60.0, quality_factor=30):
    """
    Processes EEG data by applying bandpass and notch filters, then normalizes it.

    Parameters:
    - eeg_data: NumPy array of raw EEG data (channels x samples).
    - fs: Sampling frequency in Hz.
    - lowcut: Low cutoff frequency for bandpass filter in Hz.
    - highcut: High cutoff frequency for bandpass filter in Hz.
    - notch_freq: Frequency to remove with notch filter in Hz.
    - quality_factor: Quality factor for notch filter.

    Returns:
    - normalized_data: NumPy array of processed EEG data.
    """
    num_channels = eeg_data.shape[0]
    filtered_data = np.zeros_like(eeg_data)

    for i in range(num_channels):
        channel = eeg_data[i, :]
        try:
            bandpassed_channel = bandpass_filter(channel, lowcut, highcut, fs)
            filtered_channel = notch_filter(bandpassed_channel, notch_freq, fs, quality_factor)
            filtered_data[i, :] = filtered_channel
        except ValueError as e:
            logging.error(f"Error filtering channel {i + 1}: {e}")
            filtered_data[i, :] = channel  # Use original data if filtering fails

    # Normalize the data
    mean = np.mean(filtered_data, axis=1, keepdims=True)
    std = np.std(filtered_data, axis=1, keepdims=True) + 1e-6  # Prevent division by zero
    normalized_data = (filtered_data - mean) / std

    return normalized_data

def bandpass_filter(data, lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def notch_filter(data, freq, fs, quality_factor=30):
    nyq = 0.5 * fs
    w0 = freq / nyq
    b, a = iirnotch(w0, quality_factor)
    y = filtfilt(b, a, data)
    return y

def reshape_eeg_data(normalized_data):
    """
    Reshapes normalized EEG data to (samples, time_steps, features) format.

    Parameters:
    - normalized_data: NumPy array of normalized EEG data.

    Returns:
    - reshaped_data: NumPy array ready for model prediction.
    """
    num_channels, num_samples = normalized_data.shape
    reshaped_data = normalized_data.reshape(1, num_channels, num_samples).transpose(0, 2, 1)
    return reshaped_data

@app.route('/predict', methods=['GET'])
def predict():
    reshaped_data = collect_and_process_eeg_data()

    if reshaped_data is None:
        return jsonify({'error': 'No EEG data collected'}), 500

    # Make predictions
    predictions = model.predict(reshaped_data)
    prob_class_0 = predictions[0][0]
    prob_class_1 = predictions[0][1]

    # Determine predicted class based on threshold
    confidence_threshold = 0.55
    if prob_class_1 >= confidence_threshold:
        predicted_class = 1
    else:
        predicted_class = 0

    logging.info(f"Predicted Class: {predicted_class}")
    logging.info(f"Probability of Class 0: {prob_class_0}")
    logging.info(f"Probability of Class 1: {prob_class_1}")

    # Return prediction as JSON
    return jsonify({
        'predicted_class': int(predicted_class),
        'probability_class_0': float(prob_class_0),
        'probability_class_1': float(prob_class_1)
    })

if __name__ == '__main__':
    # Start the Flask server
    socketio.run(app, host='0.0.0.0', port=5000)
