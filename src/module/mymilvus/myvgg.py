import numpy as np
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg
from keras.preprocessing import image
from numpy import linalg as LA
from src.module.picseach.common.const import input_shape
import tensorflow as tf

# input_shape = (224,224,3)

def load_model():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    config.gpu_options.per_process_gpu_memory_fraction = 0.5

    global sess
    sess = tf.Session(config=config)

    global graph
    graph = tf.get_default_graph()

    global model
    model = VGG16(weights='imagenet',
                  input_shape=input_shape,
                  pooling='max',
                  include_top=False)


# def vgg_extract_feat(img_path, model, graph, sess):
def vgg_extract_feat(img_path):
    load_model()
    with sess.as_default():
        with graph.as_default():
            img = image.load_img(img_path, target_size=(input_shape[0], input_shape[1]))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input_vgg(img)
            print("img:")
            print(img)
            feat = model.predict(img)
            norm_feat = feat[0] / LA.norm(feat[0])
            norm_feat = [i.item() for i in norm_feat]
            return norm_feat

if __name__ == "__main__":
    vgg_extract_feat("/tmp/pic2/2008_007028.jpg")