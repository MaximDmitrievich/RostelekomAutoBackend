import tensorflow as tf
from PIL import Image
from base64 import b64decode, b64decode
import io
import numpy as np
import cv2
import numpy as np
import tensorflow as tf
import time
from yolov4.tf import YOLOv4

class ModelProvider:
    def __init__(self, path_to_model):
        self.model = YOLOv4()#tf.open_model(path_to_model)
        self.model.classes = "./model/coco.names"
        self.model.make_model()
        self.model.load_weights("./model/yolov4.weights", weights_type="yolo")

    def detect(self, imageb64string):
        imgdata = b64decode(imageb64string)
        image = Image.open(io.BytesIO(imgdata))
        res_image = np.array(image)
        resized_image = self.model.resize_image(res_image)
        resized_image = resized_image / 255
        input_data = resized_image[np.newaxis, ...].astype(np.float32)
        candidates = self.model.model.predict(input_data)

        _candidates = []
        for candidate in candidates:
            batch_size = candidate.shape[0]
            grid_size = candidate.shape[1]
            _candidates.append(
                tf.reshape(
                    candidate, shape=(1, grid_size * grid_size * 3, -1)
                )
            )
        # candidates == Dim(batch, candidates, (bbox))
        candidates = np.concatenate(_candidates, axis=1)

        # pred_bboxes == Dim(candidates, (x, y, w, h, class_id, prob))
        pred_bboxes = self.model.candidates_to_pred_bboxes(candidates[0])
        pred_bboxes = self.model.fit_pred_bboxes_to_original(
            pred_bboxes, image.shape
        )

        if pred_bboxes is not None:
            return { "free_places" : len(pred_bboxes) }