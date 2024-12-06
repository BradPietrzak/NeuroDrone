import numpy as np
import os

from sklearn.model_selection import train_test_split


def load_shuffled_data(data_path, labels_path):
    """
    Loads shuffled EEG data and labels from .npy files.

    Parameters:
        data_path (str): Path to the shuffled EEG data .npy file.
        labels_path (str): Path to the shuffled labels .npy file.

    Returns:
        tuple: EEG data and labels as numpy arrays.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"The data file '{data_path}' was not found.")
    if not os.path.exists(labels_path):
        raise FileNotFoundError(f"The labels file '{labels_path}' was not found.")

    data = np.load(data_path)
    labels = np.load(labels_path)
    print(f"Loaded data from '{data_path}' with shape {data.shape}.")
    print(f"Loaded labels from '{labels_path}' with shape {labels.shape}.")
    return data, labels

def split_dataset(data, labels, train_size=0.7, val_size=0.15, test_size=0.15, random_state=42):
    """
    Splits the dataset into training, validation, and testing sets.

    Parameters:
        data (numpy.ndarray): EEG data array.
        labels (numpy.ndarray): Labels array.
        train_size (float): Proportion of data for training.
        val_size (float): Proportion of data for validation.
        test_size (float): Proportion of data for testing.
        random_state (int): Seed for reproducibility.

    Returns:
        tuple: Training, validation, and testing sets.
    """
    if not np.isclose(train_size + val_size + test_size, 1.0):
        raise ValueError("Train, validation, and test sizes must sum to 1.")

    # First split: Training vs Temporary (Validation + Testing)
    X_train, X_temp, y_train, y_temp = train_test_split(
        data, labels,
        train_size=train_size,
        random_state=random_state,
        stratify=labels
    )
    print(f"Training set: {X_train.shape[0]} samples.")
    print(f"Temporary set (Validation + Testing): {X_temp.shape[0]} samples.")

    # Calculate the proportion of validation within the temp set
    val_ratio = val_size / (val_size + test_size)

    # Second split: Validation vs Testing
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp,
        train_size=val_ratio,
        random_state=random_state,
        stratify=y_temp
    )
    print(f"Validation set: {X_val.shape[0]} samples.")
    print(f"Testing set: {X_test.shape[0]} samples.")

    return X_train, X_val, X_test, y_train, y_val, y_test


def save_split_data(X_train, y_train, X_val, y_val, X_test, y_test):
    """
    Saves the split datasets into separate .npy files within a 'splits' directory.

    Parameters:
        X_train (numpy.ndarray): Training data.
        y_train (numpy.ndarray): Training labels.
        X_val (numpy.ndarray): Validation data.
        y_val (numpy.ndarray): Validation labels.
        X_test (numpy.ndarray): Testing data.
        y_test (numpy.ndarray): Testing labels.
    """
    # Define the directory to save splits
    splits_dir = 'splits'

    # Create the directory if it doesn't exist
    if not os.path.exists(splits_dir):
        os.makedirs(splits_dir)
        print(f"Created directory '{splits_dir}'.")
    else:
        print(f"Directory '{splits_dir}' already exists.")

    try:
        # Define file paths
        train_data_path = os.path.join(splits_dir, 'X_train.npy')
        train_labels_path = os.path.join(splits_dir, 'y_train.npy')
        val_data_path = os.path.join(splits_dir, 'X_val.npy')
        val_labels_path = os.path.join(splits_dir, 'y_val.npy')
        test_data_path = os.path.join(splits_dir, 'X_test.npy')
        test_labels_path = os.path.join(splits_dir, 'y_test.npy')

        # Save the datasets
        np.save(train_data_path, X_train)
        np.save(train_labels_path, y_train)
        np.save(val_data_path, X_val)
        np.save(val_labels_path, y_val)
        np.save(test_data_path, X_test)
        np.save(test_labels_path, y_test)

        print(f"Training set saved to '{train_data_path}'.")
        print(f"Training labels saved to '{train_labels_path}'.")
        print(f"Validation set saved to '{val_data_path}'.")
        print(f"Validation labels saved to '{val_labels_path}'.")
        print(f"Testing set saved to '{test_data_path}'.")
        print(f"Testing labels saved to '{test_labels_path}'.")
    except Exception as e:
        print(f"Error saving split datasets: {e}")


def verify_split(label_set_name, labels):
    """
    Prints the distribution of labels.

    Parameters:
        label_set_name (str): Name of the label set (e.g., 'Training').
        labels (numpy.ndarray): Labels array.
    """
    unique, counts = np.unique(labels, return_counts=True)
    distribution = dict(zip(unique, counts))
    print(f"{label_set_name} Label Distribution: {distribution}")

def main():
    """
    Main function to load, split, and save EEG data and labels.
    """
    # Paths to the shuffled data and labels
    data_path = 'combined_eeg_data_shuffled.npy'
    labels_path = 'combined_eeg_labels_shuffled.npy'

    # Load shuffled data and labels
    try:
        data, labels = load_shuffled_data(data_path, labels_path)
    except Exception as e:
        print(f"Error loading shuffled data: {e}")
        return

    # Split the dataset
    try:
        X_train, X_val, X_test, y_train, y_val, y_test = split_dataset(data, labels)
    except Exception as e:
        print(f"Error during dataset splitting: {e}")
        return

    # Save the split datasets
    save_split_data(X_train, y_train, X_val, y_val, X_test, y_test)

    # Verify label distribution in each set
    verify_split("Training Set", y_train)
    verify_split("Validation Set", y_val)
    verify_split("Testing Set", y_test)

if __name__ == "__main__":
    main()
