"""
This script collects raw unfiltered brainwave data from a Neurosity device.

It logs in to the Neurosity SDK using credentials from a .env file, subscribes
to brainwave data, and saves it to a JSON file (`eeg_data_test.json`) for further analysis.
"""

from datetime import time as datetime_time  # Alias to avoid conflict with the time module
import time  # Import the standard time module for sleep
import json
from neurosity import NeurositySDK
from dotenv import load_dotenv
import os

load_dotenv()

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

def callback(data):
    """
    Callback function to handle incoming brainwave data.

    Args:
        data (dict): A dictionary containing raw unfiltered brainwave data.

    This function appends the received data to the global `all_brain_data` list,
    then writes the entire dataset to a JSON file (`eeg_data_test.json`).
    """
        print("data", data)

        all_brain_data.append(data)

        with open("eeg_data_test.json", "w") as json_file:
            json.dump(all_brain_data, json_file, indent = 4)

        print("data saves to eeg data test.json")
unsubscribe = neurosity.brainwaves_raw_unfiltered(callback)

time.sleep(5)#5 seconds of brain data, adjust this for more time.

unsubscribe()
