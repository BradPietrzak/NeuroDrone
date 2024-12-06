import numpy as np
import os


def load_data(file_path):
    """
    Loads EEG data from a .npy file.

    Parameters:
        file_path (str): Path to the .npy file.

    Returns:
        numpy.ndarray: Loaded EEG data.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")

    try:
        data = np.load(file_path)
        print(f"Successfully loaded data from '{file_path}'. Shape: {data.shape}")
        return data
    except Exception as e:
        raise ValueError(f"Error loading '{file_path}': {e}")


def combine_data(file_label_pairs):
    """
    Combines data from multiple files and assigns labels.

    Parameters:
        file_label_pairs (list of tuples): Each tuple contains the file path and its corresponding label.

    Returns:
        tuple: Combined data and labels as numpy arrays.
    """
    data_list = []
    label_list = []

    for file_path, label in file_label_pairs:
        print(f"Loading '{file_path}' with label {label}...")
        try:
            data = load_data(file_path)
            data_list.append(data)
            labels = np.full((data.shape[0],), label)
            label_list.append(labels)
            print(f"Appended {data.shape[0]} samples with label {label}.")
        except Exception as e:
            print(f"Skipping file '{file_path}' due to error: {e}")
            continue

    if not data_list:
        raise ValueError("No data was loaded. Please check the file paths and file contents.")

    # Combine all data and labels
    combined_data = np.vstack(data_list)  # Shape: (total_samples, time_steps, features)
    combined_labels = np.concatenate(label_list)  # Shape: (total_samples,)

    print(f"Total combined samples: {combined_data.shape[0]}")
    return combined_data, combined_labels


def shuffle_data(data, labels, seed=42):
    """
    Shuffles data and labels in unison.

    Parameters:
        data (numpy.ndarray): Data array.
        labels (numpy.ndarray): Labels array.
        seed (int): Random seed for reproducibility.

    Returns:
        tuple: Shuffled data and labels.
    """
    assert data.shape[0] == labels.shape[0], "Data and labels must have the same number of samples."
    np.random.seed(seed)
    permutation = np.random.permutation(data.shape[0])
    shuffled_data = data[permutation]
    shuffled_labels = labels[permutation]
    print("Data and labels shuffled successfully.")
    return shuffled_data, shuffled_labels


def save_shuffled_data(data, labels, data_save_path, labels_save_path):
    """
    Saves shuffled data and labels into .npy files.

    Parameters:
        data (numpy.ndarray): Shuffled EEG data.
        labels (numpy.ndarray): Shuffled labels.
        data_save_path (str): Path to save the shuffled data.
        labels_save_path (str): Path to save the shuffled labels.
    """
    try:
        np.save(data_save_path, data)
        np.save(labels_save_path, labels)
        print(f"Shuffled data saved to '{data_save_path}'.")
        print(f"Shuffled labels saved to '{labels_save_path}'.")
    except Exception as e:
        print(f"Error saving shuffled data: {e}")


def verify_label_distribution(labels):
    """
    Prints the distribution of labels.

    Parameters:
        labels (numpy.ndarray): Labels array.
    """
    unique, counts = np.unique(labels, return_counts=True)
    label_distribution = dict(zip(unique, counts))
    print(f"Label Distribution: {label_distribution}")


def main():
    """
    Main function to combine, shuffle, and save EEG data with labels.
    """
    # Define the paths to your .npy files and their corresponding labels
    # Label 1: "UP"
    # Label 0: "Not UP"
    file_label_pairs = [
        (r"C:\Users\bradp\PycharmProjects\relearning python\BrainDroneInterface\brainData\UP_controlled_filtered.npy",
         1),
        (r"C:\Users\bradp\PycharmProjects\relearning python\BrainDroneInterface\brainData\UP_uncontrolled_filtered.npy",
         1),
        (
        r"C:\Users\bradp\PycharmProjects\relearning python\BrainDroneInterface\brainData\neutral_controlled_filtered.npy",
        0),
        (
        r"C:\Users\bradp\PycharmProjects\relearning python\BrainDroneInterface\brainData\neutral_uncontrolled_filtered.npy",
        0)
    ]

    # Combine data and labels
    try:
        combined_data, combined_labels = combine_data(file_label_pairs)
    except Exception as e:
        print(f"Error during data combining: {e}")
        return

    # Shuffle the combined data and labels
    shuffled_data, shuffled_labels = shuffle_data(combined_data, combined_labels)

    # Define paths to save the shuffled data and labels
    data_save_path = 'combined_eeg_data_shuffled.npy'
    labels_save_path = 'combined_eeg_labels_shuffled.npy'

    # Save the shuffled data and labels
    save_shuffled_data(shuffled_data, shuffled_labels, data_save_path, labels_save_path)

    # Verify the shapes
    print(f"Shuffled Data Shape: {shuffled_data.shape}")  # Expected: (total_samples, time_steps, features)
    print(f"Shuffled Labels Shape: {shuffled_labels.shape}")  # Expected: (total_samples,)

    # Check label distribution
    verify_label_distribution(shuffled_labels)


if __name__ == "__main__":
    main()
