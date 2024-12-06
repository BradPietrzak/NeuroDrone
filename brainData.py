import requests
import json
import websocket
import threading
import time

# Define lists to store different types of brainwave data
brainwave_data_neutral = []
brainwave_data_up = []
brainwave_data_down = []
brainwave_data_front = []
brainwave_data_back = []
brainwave_data_left = []
brainwave_data_right = []

# Authentication function to get the access token
def authenticate(email, password):
    login_url = "https://api.neurosity.co/v1/login"
    response = requests.post(login_url, json={"email": email, "password": password})
    if response.status_code == 200:
        access_token = response.json().get("token")
        print("Authenticated successfully")
        return access_token
    else:
        print("Authentication failed:", response.text)
        return None

# Function to handle incoming messages from WebSocket
def record_brain_data(ws, message, direction):
    data = json.loads(message)
    brainwave_data_neutral.append(data)  # Append data to the list
    print("Data received:", data)

# Function to handle WebSocket errors
def on_error(ws, error):
    print("WebSocket Error:", error)

# Function to handle WebSocket closure
def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

# Function to handle WebSocket opening and subscribe to data
def on_open(ws):
    subscription_message = json.dumps({
        "command": "subscribe",
        "scope": "brainwaves/raw"
    })
    ws.send(subscription_message)

# Function to set up and start the WebSocket connection
def connect_websocket(websocket_url):
    ws = websocket.WebSocketApp(websocket_url,
                                on_open=on_open,
                                on_message=record_brain_data,
                                on_error=on_error,
                                on_close=on_close)

    # Run WebSocket connection in a separate thread
    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.start()

    return ws, ws_thread

# Main function to authenticate, connect to WebSocket, and save data
def main():
    # Replace with your Neurosity credentials
    device_id = "your_device_id"
    email = "your_email"
    password = "your_password"

    # Authenticate and get access token
    access_token = authenticate(email, password)
    if not access_token:
        return  # Exit if authentication failed

    # WebSocket URL with device ID and access token
    websocket_url = f"wss://api.neurosity.co/{device_id}/data?token={access_token}"

    # Connect to the WebSocket
    ws, ws_thread = connect_websocket(websocket_url)

    # Run for a specified duration or until interrupted
    try:
        time.sleep(30)  # Collect data for 30 seconds
    except KeyboardInterrupt:
        print("Interrupted")

    # Close WebSocket and save data to JSON
    ws.close()
    ws_thread.join()  # Ensure WebSocket thread has fully closed

    input = ''

    while True:
        user_input = input("Enter a command (R, L, U, D, F, B) or press Enter to quit: ").strip()

        # Exit the loop if input is empty
        if user_input == '':
            break

        # Check the input and perform actions based on the input value
        if user_input == 'R':
            # Action for Right
            print("You chose Right")

        elif user_input == 'L':
            # Action for Left
            print("You chose Left")

        elif user_input == 'U':
            # Action for Up
            print("You chose Up")

        elif user_input == 'D':
            # Action for Down
            print("You chose Down")

        elif user_input == 'F':
            # Action for Front
            print("You chose Front")

        elif user_input == 'B':
            # Action for Back
            print("You chose Back")

        else:
            print("Invalid input. Please enter R, L, U, D, F, or B.")

    # Save data to JSON files
    with open("brainwave_data_neutral.json", "w") as f:
        json.dump(brainwave_data_neutral, f, indent=2)

    print("Data saved to brainwave_data_neutral.json")

# Run the main function
if __name__ == "__main__":
    main()
