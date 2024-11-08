import json
import os

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
    #debug function ignore
    print("hello")
    for row in array:
        if isinstance(row, list):  # Check if row is a list (for 2D)
            for item in row:
                print(item)
        else:
            print(row)


def merge_json_data(json_data):
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
    print("I am here")
    with open(file_path, 'w') as file:
        json.dump(json_obj, file, indent = 4)
    print(f"Merged JSON data saved to {file_path}")

def main():
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
