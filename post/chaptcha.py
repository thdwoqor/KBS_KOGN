# from tensorflow.keras.models import load_model
from keras.models import load_model
from tensorflow import keras
from tensorflow import keras
from tensorflow.keras import layers

from glob import glob
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import cv2 
import os


class Chaptcha:
    class CTCLayer(layers.Layer):
        def __init__(self, name=None, **kwargs):
            super().__init__(name=name, **kwargs)
            self.loss_fn = keras.backend.ctc_batch_cost

        def call(self, y_true, y_pred):
            # Compute the training-time loss value and add it
            # to the layer using `self.add_loss()`.
            batch_len = tf.cast(tf.shape(y_true)[0], dtype='int64')
            input_length = tf.cast(tf.shape(y_pred)[1], dtype='int64')
            label_length = tf.cast(tf.shape(y_true)[1], dtype='int64')

            input_length = input_length * tf.ones(shape=(batch_len, 1), dtype='int64')
            label_length = label_length * tf.ones(shape=(batch_len, 1), dtype='int64')

            loss = self.loss_fn(y_true, y_pred, input_length, label_length)
            self.add_loss(loss)

            # At test time, just return the computed predictions
            return y_pred

    def GPU_Set(self):
        # 텐서플로가 첫 번째 GPU만 사용하도록 제한
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except RuntimeError as e:
                print(e)
    
    def Preprocessing(self):
        image = cv2.imread('filename.png') # 이미지 파일 읽어들이기 
        image = cv2.medianBlur(image, 3)
        i=5

        bgrLower = np.array([140-i, 140-i, 140-i]) # 추출할 색의 하한(BGR) 
        bgrUpper = np.array([140+i, 140+i, 140+i]) # 추출할 색의 상한(BGR) 
        img_mask = cv2.inRange(image, bgrLower, bgrUpper) # BGR로 부터 마스크를 작성 

        cv2.imwrite('filename.png', img_mask)
        cv2.destroyAllWindows()

    def __init__(self):
        self.Preprocessing()
        self.GPU_Set()
        self.imgs = []
        self.labels = []
        self.batch_size = 32
        self.img_width = 200
        self.img_height = 50
        self.max_length = 5
        self.characters = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        self.characters = sorted(self.characters)

        self.char_to_num = layers.experimental.preprocessing.StringLookup(
            vocabulary=list(self.characters), num_oov_indices=0, mask_token=None
        )

        self.num_to_char = layers.experimental.preprocessing.StringLookup(
            vocabulary=self.char_to_num.get_vocabulary(), num_oov_indices=0, mask_token=None, invert=True
        )

        self.model = keras.models.load_model('post\models\model.h5', custom_objects={'CTCLayer': self.CTCLayer})
        self.model.summary()

        self.prediction_model = keras.models.Model(
        self.model.get_layer(name='image').input, self.model.get_layer(name='dense2').output
        )

    def decode_batch_predictions(self,pred):
        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        # Use greedy search. For complex tasks, you can use beam search
        results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
            :, :self.max_length
        ]
        # Iterate over the results and get back the text
        output_text = []
        for res in results:
            res = tf.strings.reduce_join(self.num_to_char(res)).numpy().decode('utf-8')
            output_text.append(res)
        return output_text

    def encode_single_sample(self, img_path, label):
        img = tf.io.read_file(img_path)

        img = tf.io.decode_png(img, channels=1)

        img = tf.image.convert_image_dtype(img, tf.float32)

        img = tf.image.resize(img, [self.img_height, self.img_width])

        img = tf.transpose(img, perm=[1, 0, 2])

        label = self.char_to_num(tf.strings.unicode_split(label, input_encoding='UTF-8'))

        return {'image': img, 'label': label}

    def decode_batch_predictions(self, pred):
        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        # Use greedy search. For complex tasks, you can use beam search
        results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
            :, :self.max_length
        ]
        # Iterate over the results and get back the text
        output_text = []
        for res in results:
            res = tf.strings.reduce_join(self.num_to_char(res)).numpy().decode('utf-8')
            output_text.append(res)
        return output_text

    def chaptcha_crawling(self):
        validation_dataset = tf.data.Dataset.from_tensor_slices((np.array(['filename.png']), np.array(['00000'])))
        validation_dataset = (
            validation_dataset.map(
                self.encode_single_sample, num_parallel_calls=tf.data.experimental.AUTOTUNE
            )
            .batch(self.batch_size)
            .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
        )

        for batch in validation_dataset.take(1):
            batch_images = batch["image"]
            batch_labels = batch["label"]

            preds = self.prediction_model.predict(batch_images)
            pred_texts = self.decode_batch_predictions(preds)
            data_split = pred_texts[0].split("'")
            print(data_split[0])
            return data_split[0]