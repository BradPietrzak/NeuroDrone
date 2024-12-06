from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import json
import time
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch
from tensorflow.keras.models import load_model
from djitellopy import Tello
import logging

# Load environment variables
load_dotenv()


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed logs
    format='%(asctime)s %(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize Tello drone
try:
    tello = Tello()
    tello.connect()
    battery = tello.get_battery()
    logging.info(f"Connected to Tello drone. Battery level: {battery}%")
except Exception as e:
    logging.error(f"Failed to connect to Tello drone: {e}")
    tello = None  # Proceed without drone if connection fails






print("NEUROSITY_DEVICE_ID:", os.getenv("NEUROSITY_DEVICE_ID"))
print("NEUROSITY_EMAIL:", os.getenv("NEUROSITY_EMAIL"))
print("NEUROSITY_PASSWORD:", os.getenv("NEUROSITY_PASSWORD"))

all_brain_data = []

neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

def load_json_from_file(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"the file is not found")

    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"error decoding Json: {e}")
    return data

def print_flat_array(array):

    for row in array:
        if isinstance(row, list):  # Check if row is a list (for 2D)
            for item in row:
                print(item)
        else:
            print(row)

def merge_json_data(json_data):
    """
        Merges and processes raw JSON EEG data into a new format with specified constraints.

        Parameters:
            json_data (list of dict): A list of JSON objects, where each object contains EEG data
                                      under the "data" key. Each "data" key maps to a list of lists
                                      representing channels and their respective samples.

        Returns:
            list of lists: A 2D list where each sublist corresponds to a channel (8 total),
                           and contains up to 16 samples per data array, merged from the input JSON data.

        Functionality:
            - Creates a new 2D list (`new_json_data`) with 8 empty lists, one for each EEG channel.
            - Iterates through the input JSON data (`json_data`), which contains multiple datasets.
            - For each dataset:
                - Loops through the first 8 channels in the "data" field.
                - Appends up to 16 elements (samples) from each channel to the corresponding channel list in `new_json_data`.
                - Skips additional samples or channels beyond the specified limits (8 channels, 16 samples per channel).
            - Prints the progress and structure of the merged data during the process.

        Example Input:
            json_data = [
                {"data": [[1, 2, 3], [4, 5, 6], [7, 8, 9], ...]},
                {"data": [[10, 11, 12], [13, 14, 15], [16, 17, 18], ...]},
                ...
            ]

        Example Output:
            [
                [1, 2, 3, 10, 11, 12],  # Merged samples for channel 1
                [4, 5, 6, 13, 14, 15],  # Merged samples for channel 2
                [7, 8, 9, 16, 17, 18],  # Merged samples for channel 3
                ...
            ]

        Notes:
            - Assumes that each dataset contains a "data" key with a list of channel data.
            - Limits processing to the first 8 channels and first 16 samples per channel to maintain structure and size consistency.
            - Logs information to the console for debugging and progress tracking.
        """
    new_json_data = [[] for _ in range(8)]
    #print_flat_array(new_json_data)
    for data_set_obj in json_data:

        i = 0
        for data_array in data_set_obj["data"]:
            if i < 8:
                j = 0
                for element in data_array:
                    if j < 16:
                        new_json_data[i].append(element)
                    j += 1
                i += 1
            else:
                break

    return new_json_data


def save_json_to_file(json_obj, file_path):

    with open(file_path, 'w') as file:
        json.dump(json_obj, file, indent = 4)
    #print(f"Merged JSON data saved to {file_path}")

def process_eeg_data(eeg_data, fs=256, lowcut=0.02, highcut=40.0, notch_freq=60.0, quality_factor=30):
    """
    Processes EEG data by applying filters and normalization.

    Parameters:
    - eeg_data: NumPy array of raw EEG data (channels x samples).
    - fs: Sampling frequency in Hz.
    - lowcut: Low cutoff frequency for bandpass filter (Hz).
    - highcut: High cutoff frequency for bandpass filter (Hz).
    - notch_freq: Frequency to remove with notch filter (Hz).
    - quality_factor: Quality factor for notch filter.

    Returns:
    - normalized_data: NumPy array of processed EEG data (channels x samples).
    """
    num_channels = eeg_data.shape[0]
    filtered_data = np.zeros_like(eeg_data)

    # Apply filters to each channel
    for i in range(num_channels):
        channel = eeg_data[i, :]
        try:
            bandpassed_channel = bandpass_filter(channel, lowcut, highcut, fs, order=3)
            filtered_channel = notch_filter(bandpassed_channel, notch_freq, fs, quality_factor)
            filtered_data[i, :] = filtered_channel
        except ValueError as e:
            #print(f"Error filtering channel {i + 1}: {e}")
            filtered_data[i, :] = channel  # Use original data if filtering fails

    # Normalize the data
    mean = np.mean(filtered_data, axis=1, keepdims=True)
    std = np.std(filtered_data, axis=1, keepdims=True) + 1e-6  # Add small value to prevent division by zero
    normalized_data = (filtered_data - mean) / std

    return normalized_data

def bandpass_filter(data, lowcut, highcut, fs, order=3):
    """
    Applies a Butterworth bandpass filter to the data.

    Parameters:
    - data: 1D NumPy array of the signal.
    - lowcut: Low cutoff frequency (Hz).
    - highcut: High cutoff frequency (Hz).
    - fs: Sampling frequency (Hz).
    - order: Order of the filter.

    Returns:
    - Filtered signal.
    """
    nyq = 0.5 * fs  # Nyquist Frequency
    low = lowcut / nyq
    high = highcut / nyq
    # Create the Butterworth bandpass filter coefficients
    b, a = butter(order, [low, high], btype='band')
    # Apply the filter using filtfilt for zero-phase filtering
    y = filtfilt(b, a, data)
    return y

def notch_filter(data, freq, fs, quality_factor=30):
    """
    Applies a notch filter to remove a specific frequency.

    Parameters:
    - data: 1D NumPy array of the signal.
    - freq: Frequency to remove (Hz).
    - fs: Sampling frequency (Hz).
    - quality_factor: Controls the width of the notch.

    Returns:
    - Filtered signal.
    """
    nyq = 0.5 * fs
    w0 = freq / nyq
    # Create notch filter coefficients
    b, a = iirnotch(w0, quality_factor)
    # Apply the filter using filtfilt for zero-phase filtering
    y = filtfilt(b, a, data)
    return y

def reshape_eeg_data(normalized_json_data):
    """
    Reshapes the normalized EEG data to (samples, time_steps, features) format.

    Parameters:
    - normalized_data: NumPy array of normalized EEG data (channels x samples).

    Returns:
    - reshaped_data: NumPy array of reshaped EEG data (1 x samples x channels).
    """
    num_channels, num_samples = normalized_json_data.shape
    reshaped_json_data = normalized_json_data.reshape(1, num_channels, num_samples).transpose(0, 2, 1)  # Shape: (1, num_samples, num_channels)
    return reshaped_json_data


model = load_model('eeg_cnn_lstm_model.h5')
print("Model loaded successfully.")
while(1):
    all_brain_data = []  # Clear data for the current segment

    def callback(data):
        #print("data", data)

        all_brain_data.append(data)

    # Subscribe to raw brainwave data
    unsubscribe = neurosity.brainwaves_raw_unfiltered(callback)

    # Collect data for 5 seconds
    time.sleep(5)

    # Stop collecting data
    try:
        unsubscribe()
        print("Unsubscribed successfully.")
    except AttributeError as e:
        print(f"Error while unsubscribing: {e}")

    # Save data to the specified path with the naming convention
    file_path = f"C:\\Users\\bradp\\PycharmProjects\\relearning python\\BrainDroneInterface\\brainData\\live_data.json"

    save_json_to_file(all_brain_data, file_path)

    json_data = load_json_from_file(file_path)

    json_data = merge_json_data(json_data)

    eeg_array = np.array(json_data, dtype=np.float64)
    #print(eeg_array)
    normalized_data = process_eeg_data(eeg_array)

    desired_length = 1280  # Adjust as needed
    current_length = normalized_data.shape[1]
    print(current_length)

    if current_length < desired_length:
        pad_width = desired_length - current_length
        normalized_data = np.pad(normalized_data, ((0, 0), (0, pad_width)), mode='constant', constant_values=0)
    elif current_length > desired_length:
        normalized_data = normalized_data[:, :desired_length]

    reshaped_json_data = reshape_eeg_data(normalized_data)
    # Set your confidence threshold
    # Set your confidence threshold
    confidence_threshold = 0.55

    # Make predictions
    predictions = model.predict(reshaped_json_data)  # Shape: (1, num_classes)

    # Extract probabilities
    prob_class_0 = predictions[0][0]
    prob_class_1 = predictions[0][1]

    # Determine the predicted class based on the threshold
    if prob_class_1 >= confidence_threshold:
        predicted_class = 1
    else:
        predicted_class = 0  # Default to class 0

    # Output the result
    print(f"Predicted Class: {predicted_class}")
    print(f"Probability of Class 1: {prob_class_1}")
    print(f"Probability of Class 0: {prob_class_0}")
    print(f"EEG array shape: {eeg_array.shape}")

    # Trigger flip command if prediction is 1
    if predicted_class == 1 and tello:
        try:
            logging.info("Predicted Class: 1. Sending flip command to drone.")
            tello.takeoff()
            logging.info("Drone flip command executed.")

            logging.info("Sending land command to drone.")
            tello.land()
            logging.info("Drone has landed.")

            break  # Exit the loop after landing
        except Exception as e:
            logging.error(f"Failed to execute flip or land command: {e}")
