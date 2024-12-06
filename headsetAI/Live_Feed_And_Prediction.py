from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import json
import time

# Load environment variables
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

# Loop 500 times to save each segment
while(1):
    all_brain_data = []  # Clear data for the current segment

    def callback(data):
        print("data", data)

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
    file_path = f"C:\\Users\\bradp\\PycharmProjects\\relearning python\\BrainDroneInterface\\brainData\\UP_uncontrolled\\UP_uncontrolled{i}.json"
    with open(file_path, "w") as json_file:
        json.dump(all_brain_data, json_file, indent=4)



    print(f"Data saved to {file_path}")

print("Data collection complete!")
