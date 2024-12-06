import numpy as np
import os
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt


def load_split_data():
    """
    Loads the split EEG data and labels from .npy files.

    Returns:
        tuple: Training, validation, and testing data and labels.
    """
    try:
        X_train = np.load('X_train.npy')
        y_train = np.load('y_train.npy')
        X_val = np.load('X_val.npy')
        y_val = np.load('y_val.npy')
        X_test = np.load('X_test.npy')
        y_test = np.load('y_test.npy')
        print("Training, validation, and testing data loaded successfully.")
        return X_train, y_train, X_val, y_val, X_test, y_test
    except Exception as e:
        print(f"Error loading split data: {e}")
        return None, None, None, None, None, None


def preprocess_labels(y_train, y_val, y_test, num_classes=2):
    """
    Converts integer labels to one-hot encoded vectors.

    Parameters:
        y_train (numpy.ndarray): Training labels.
        y_val (numpy.ndarray): Validation labels.
        y_test (numpy.ndarray): Testing labels.
        num_classes (int): Number of classes.

    Returns:
        tuple: One-hot encoded labels.
    """
    y_train_cat = to_categorical(y_train, num_classes)
    y_val_cat = to_categorical(y_val, num_classes)
    y_test_cat = to_categorical(y_test, num_classes)
    return y_train_cat, y_val_cat, y_test_cat


def build_model(input_shape, num_classes=2):
    """
    Defines and compiles the CNN-LSTM model.

    Parameters:
        input_shape (tuple): Shape of the input data (time_steps, features).
        num_classes (int): Number of output classes.

    Returns:
        tensorflow.keras.Model: Compiled model.
    """
    model = Sequential()

    # Convolutional Layer 1
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=input_shape))
    model.add(MaxPooling1D(pool_size=2))

    # Convolutional Layer 2
    model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))

    # LSTM Layer
    model.add(LSTM(100, activation='tanh'))

    # Dropout Layer
    model.add(Dropout(0.5))

    # Output Layer
    model.add(Dense(num_classes, activation='softmax'))

    # Compile the model
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()
    return model


def plot_training_history(history):
    """
    Plots the training and validation accuracy and loss.

    Parameters:
        history (tensorflow.keras.callbacks.History): Training history.
    """
    # Accuracy plot
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy', color='blue')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy', color='orange')
    plt.title('Accuracy Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    # Loss plot
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss', color='blue')
    plt.plot(history.history['val_loss'], label='Validation Loss', color='orange')
    plt.title('Loss Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    plt.show()


def main():
    # Load split data
    X_train, y_train, X_val, y_val, X_test, y_test = load_split_data()
    if X_train is None:
        return

    # Preprocess labels
    y_train_cat, y_val_cat, y_test_cat = preprocess_labels(y_train, y_val, y_test)

    # Define input shape
    time_steps = X_train.shape[1]  # 1280
    features = X_train.shape[2]  # 8
    input_shape = (time_steps, features)

    # Build the model
    model = build_model(input_shape, num_classes=2)

    # Train the model
    history = model.fit(
        X_train, y_train_cat,
        epochs=20,
        batch_size=16,
        validation_data=(X_val, y_val_cat)
    )

    # Plot training history
    plot_training_history(history)

    # Evaluate the model on the test set
    test_loss, test_accuracy = model.evaluate(X_test, y_test_cat)
    print(f"\nTest Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")

    # Make predictions on the test set
    y_pred_prob = model.predict(X_test)
    y_pred = np.argmax(y_pred_prob, axis=1)
    y_true = np.argmax(y_test_cat, axis=1)

    # Classification Report
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=['Not UP', 'UP']))

    # Confusion Matrix
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))

    # Save the trained model
    model.save('eeg_cnn_lstm_model.h5')
    print("Model saved to 'eeg_cnn_lstm_model.h5'.")


if __name__ == "__main__":
    main()
