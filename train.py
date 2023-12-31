
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np
import pandas as pd
import cv2
import numpy
from glob import glob
import scipy.io
from sklearn.model_selection import train_test_split
import tensorflow as tf

from tensorflow.python.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping, CSVLogger
from unet import build_unet

""" Global parameters """
global IMG_H
global IMG_W
global NUM_CLASSES
global CLASSES
global COLORMAP

""" Creating a directory """
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

""" Load and split the dataset """
def load_dataset(path, split=0.2):
    train_x = sorted(glob(os.path.join(path, "Training", "Images", "*")))
    train_y = sorted(glob(os.path.join(path, "Training", "Categories", "*")))



    images = [cv2.imread(image_path, cv2.IMREAD_COLOR) for image_path in train_x]
    masks = [cv2.imread(mask_path, cv2.IMREAD_COLOR) for mask_path in train_y]

    # Print dimensions of the first image and mask for verification
    
    split_size = int(split * len(images))

    split_size = int(split * len(train_x))

    train_x, valid_x = train_test_split(train_x, test_size=split_size, random_state=42)
    train_y, valid_y = train_test_split(train_y, test_size=split_size, random_state=42)

    train_x, test_x = train_test_split(train_x, test_size=split_size, random_state=42)
    train_y, test_y = train_test_split(train_y, test_size=split_size, random_state=42)

    return (train_x, train_y), (valid_x, valid_y), (test_x, test_y)

def get_colormap(path):
    mat_path = os.path.join(path, "data.mat")
    colormap = scipy.io.loadmat(mat_path)["colormap"]
    colormap = colormap * 256
    colormap = colormap.astype(np.uint8)
    colormap = [[c[2], c[1], c[0]] for c in colormap]

    classes = [
        "acne",
        "blemish",
        "clogged_pores",
        "dark_circles",
        "freckle_beauty_spot",
        "hyperpigmentation_dark_marks",
        "redness",
        "uneven_skintone",
        "wrinkle_fine_lines"
    ]

    return classes, colormap

def read_image_mask(x, y):
    """ Reading """
    x = cv2.imread(x, cv2.IMREAD_COLOR)
    y = cv2.imread(y, cv2.IMREAD_COLOR)
    assert x.shape == y.shape

    """ Resizing """
    x = cv2.resize(x, (IMG_W, IMG_H))
    y = cv2.resize(y, (IMG_W, IMG_H))

    """ Image processing """
    x = x / 255.0
    x = x.astype(np.float32)

    """ Mask processing """
    output = []
    for color in COLORMAP:
        cmap = np.all(np.equal(y, color), axis=-1)
        output.append(cmap)
    output = np.stack(output, axis=-1)
    output = output.astype(np.uint8)

    return x, output

def preprocess(x, y):
    def f(x, y):
        x = x.decode()
        y = y.decode()
        image, mask = read_image_mask(x, y)
        return image, mask

    image, mask = tf.numpy_function(f, [x, y], [tf.float32, tf.uint8])
    image.set_shape([IMG_H, IMG_W, 3])
    mask.set_shape([IMG_H, IMG_W, NUM_CLASSES])

    return image, mask

def tf_dataset(x, y, batch=8):
    dataset = tf.data.Dataset.from_tensor_slices((x, y))
    dataset = dataset.shuffle(buffer_size=5000)
    dataset = dataset.map(preprocess)
    dataset = dataset.batch(batch)
    dataset = dataset.prefetch(2)

    return dataset


if __name__ == "__main__":
    """ Seeding """
    np.random.seed(42)
    tf.random.set_seed(42)

    """ Directory for storing files """
    create_dir("files")

    """ Hyperparameters """
    IMG_H = 1024
    IMG_W =1024
    NUM_CLASSES = 9
    input_shape = (IMG_H, IMG_W, 3)

    batch_size = 7
    lr = 1e-4
    num_epochs = 100
    dataset_path = "C:\\Users\\Arpit Mohanty\\Documents\\iot"

    model_path = os.path.join("files", "model.h5")
    csv_path = os.path.join("files", "data.csv")

    """ Loading the dataset """
    (train_x, train_y), (valid_x, valid_y), (test_x, test_y) = load_dataset(dataset_path)
    print(f"Train: {len(train_x)}/{len(train_y)} - Valid: {len(valid_x)}/{len(valid_y)} - Test: {len(test_x)}/{len(test_x)}")
    print("")

    """ Process the colormap """
    CLASSES, COLORMAP = get_colormap(dataset_path)
  
    """ Dataset Pipeline """
    train_dataset = tf_dataset(train_x, train_y, batch=batch_size)
    valid_dataset = tf_dataset(valid_x, valid_y, batch=batch_size)

    """ Model """
    model = build_unet(input_shape, NUM_CLASSES)
    # model.load_weights(model_path)
    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"]
    )
    # model.summary()

    """ Training """
    callbacks = [
        ModelCheckpoint(model_path, verbose=1, save_best_only=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5, min_lr=1e-7, verbose=1),
        CSVLogger(csv_path, append=True),
        EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=False)
    ]

    model.fit(train_dataset,
        validation_data=valid_dataset,
        epochs=num_epochs,
        callbacks=callbacks
    )