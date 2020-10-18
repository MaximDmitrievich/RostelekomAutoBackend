import tensorflow as tf
from PIL import Image
from base64 import decodestring

class ModelProvider:
    def __init__(self, path_to_model):
        self.model = None#tf.open_model(path_to_model)

    def detect(self, imageb64string):
        image = Image.fromstring('RGB', decodestring(imageb64string))
        #self.model(image)
        if image is not None:
            return { "places" : 3 }