import json
import os

def load_json_from_file(file_path):
"""
    Loads JSON data from a file.

    Args:
        file_path (str): The path to the JSON file to load.

    Returns:
        dict or list: The parsed JSON data from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file contains invalid JSON.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"the file is not found")

    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"error decoding Json: {e}")
    return data

def print_flat_array(array):
    """
    Prints a flat representation of a potentially nested array.
    This is a debug function for inspecting array contents.

    Args:
        array (list): A list of rows, which may be lists themselves.

    Returns:
        None
    """
    print("hello")
    for row in array:
        if isinstance(row, list):  # Check if row is a list (for 2D)
            for item in row:
                print(item)
        else:
            print(row)


def merge_json_data(json_data):
    """
    Merges the "data" arrays from a list of JSON objects into a new format.

    Args:
        json_data (list): A list of JSON objects, each containing a "data" field.

    Returns:
        list: A new nested list containing the merged data arrays.

    Raises:
        ValueError: If the input data is not structured as expected.
    """
    new_json_data = [[] for _ in range(8)]
    print_flat_array(new_json_data)
    for data_set_obj in json_data:
        print("in the data loop")
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
    """
    Saves a JSON object to a file.

    Args:
        json_obj (dict or list): The JSON data to save.
        file_path (str): The path to the file where the JSON data should be saved.

    Returns:
        None
    """
    print("I am here")
    with open(file_path, 'w') as file:
        json.dump(json_obj, file, indent = 4)
    print(f"Merged JSON data saved to {file_path}")

def main():
    """
    Main function to load, merge, and save JSON data.

    Performs the following steps:
        1. Load JSON data from a file.
        2. Validate that the data is a list of JSON objects.
        3. Merge the "data" arrays from all objects.
        4. Save the merged data to a new file.

    Returns:
        None
    """
    input_file_path = r"C:\Users\bradp\PycharmProjects\relearning python\BrainDroneInterface\brainData\eeg_data_test_wifes brain waves.json"
    output_file_path = r"C:\Users\bradp\PycharmProjects\relearning python\BrainDroneInterface\brainData\merged_data.json.json"
    print("first quarter")
    try:
        json_data = load_json_from_file(input_file_path)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        return

    if not isinstance(json_data, list):
        print("the json file should contain a list of json objects")
        return

    try:
        merged_json = merge_json_data(json_data)
    except ValueError as e:
        print(e)
        return

    save_json_to_file(merged_json, output_file_path)

if __name__ == "__main__":
    main()
