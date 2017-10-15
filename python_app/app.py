""" Landmark prediction model

Todo:
    * Add more label options. Make it easier to add label options first.
    * Add tests

"""
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from flask import Flask, request
from PIL import Image
import tensorflow as tf
import numpy as np
import requests
import location_information

FLASK_APP = Flask(__name__)


def landmark_predicter():
    """
    This is a convolutional neural network model for training our dataset.
    """
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(56, 56, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    return model

@FLASK_APP.route("/predict", methods=["POST"])
def predict():
    """
    This recieves requests from our node server which will contain an image. The image is then saved locally and sent through to the model to give us a prediction.
    The prediction is then sent back to the node server.
    """
    # A url to image sent by user is recieved in request.data and then requests.get downloads it and assigns to image_file.
    image_file = requests.get(request.data).content
    print "Image received from user."
    # image_file is saved locally and then reopened as an Image object. The below method is probably inefficient, look into improving.
    write_file = open('userimage', 'w')
    write_file.write(image_file)
    write_file.close()
    local_image = Image.open(('userimage'))

    # Resize image to a size our model expects
    local_image = local_image.resize((56, 56), Image.ANTIALIAS)
    # Encode image as a numpy array
    local_image = np.asarray(local_image)
    # Use default tensorflow graph
    with GRAPH.as_default():
        # Pass image to predict function of model
        prediction = MODEL.predict(np.array([local_image]))
    # Retrive location information based off prediction label.
    location_info = location_information.get_all_location_info(LABELS[int(prediction.item(0))])
    print "Predicted image to be " + LABELS[int(prediction.item(0))] + "."

    return location_info

if __name__ == '__main__':
    GRAPH = tf.get_default_graph()
    MODEL = landmark_predicter()
    MODEL.load_weights('landmark_weights.h5')
    LABELS = ['queens university belfast', 'belfast city hall']
    FLASK_APP.run(debug=True)
