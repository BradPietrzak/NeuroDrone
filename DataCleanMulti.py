import json
import os

def load_json_from_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file is not found: {file_path}")

    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in {file_path}: {e}")
    return data

def merge_json_data(json_data):
    new_json_data = [[] for _ in range(8)]
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
        json.dump(json_obj, file, indent=4)
    print(f"Merged JSON data saved to {file_path}")



def main():
    input_dir = r"C:\Users\bradp\PycharmProjects\relearning python\BrainDroneInterface\brainData\neutral_uncontrolled"
    output_dir = r"C:\Users\bradp\PycharmProjects\relearning python\BrainDroneInterface\brainData\neutral_uncontrolled_filtered"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List all JSON files in the input directory
    input_files = [
        f for f in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, f)) and f.endswith('.json')
    ]

    for filename in input_files:
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename)  # Save with the same filename

        print(f"Processing file {input_file_path}")

        try:
            json_data = load_json_from_file(input_file_path)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error processing {input_file_path}: {e}")
            continue  # Skip to the next file if there's an error

        if not isinstance(json_data, list):
            print(f"The JSON file {input_file_path} should contain a list of JSON objects")
            continue

        try:
            merged_json = merge_json_data(json_data)
        except ValueError as e:
            print(f"Error merging data from {input_file_path}: {e}")
            continue

        save_json_to_file(merged_json, output_file_path)

if __name__ == "__main__":
    main()
