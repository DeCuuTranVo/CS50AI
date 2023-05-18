import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 20
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images_list = []
    labels_list = []
    
    # images: list of all image in data directory
    dir_list = os.listdir(data_dir) # ['.DS_Store', '0', '1', '2']
    
    for category_dir in dir_list:
        category_dir_path = os.path.join(data_dir,category_dir)
        if os.path.isdir(category_dir_path):
            for file_name in os.listdir(category_dir_path):
                # print(file_name)
                label = int(category_dir)
                image_path = os.path.join(category_dir_path, file_name)
                # print(image_path, label)
                raw_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                
                resized_image = cv2.resize(raw_image, (IMG_WIDTH, IMG_HEIGHT), interpolation = cv2.INTER_LINEAR)
                
                rescaled_image = resized_image / 255.0

                # filename = 'savedImage.jpg'
                # cv2.imwrite(filename, image)
                
                images_list.append(rescaled_image)
                labels_list.append(label)
                
        # print("category:", category_dir, "loaded")
        
    # print("Dataset loaded!")
    return (images_list, labels_list)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, Flatten, Dropout
    
    def define_model():     
        NUM_FILTERS_CONV = 128
        NUM_UNITS_DENSE = 32
        DROPOUT_RATE = 0.5
            
        visible = Input(shape=(IMG_WIDTH,IMG_HEIGHT,3))      
        
        conv1 = Conv2D(NUM_FILTERS_CONV, kernel_size=3, activation='relu')(visible)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
        conv2 = Conv2D(NUM_FILTERS_CONV, kernel_size=3, activation='relu')(pool1)
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
        conv3 = Conv2D(NUM_FILTERS_CONV, kernel_size=3, activation='relu')(pool2)
        pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
     
        flat = Flatten()(pool3)
        # hidden1 = Dense(NUM_UNITS_DENSE, activation='relu')(flat)
        dropout1 = Dropout(DROPOUT_RATE)(flat)      
        # hidden2 = Dense(NUM_UNITS_DENSE, activation='relu')(dropout1)
        # dropout2 = Dropout(DROPOUT_RATE)(hidden2)   
        # hidden3 = Dense(NUM_UNITS_DENSE, activation='relu')(dropout2)
        # dropout3 = Dropout(DROPOUT_RATE)(hidden3) 
        
        output = Dense(NUM_CATEGORIES, activation='softmax')(dropout1)
        model = Model(inputs=visible, outputs=output)
        return model

    model = define_model()

    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    # print(model.summary())
    return model


if __name__ == "__main__":
    main()
