from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.mobilenet_v2 import preprocess_input
from keras.applications.mobilenet_v2 import decode_predictions
from keras.preprocessing import image
import numpy as np

model = MobileNetV2(weights='imagenet')
data = np.empty((1, 224, 224, 3))
img_path = 'dataset/train/battery/000027.jpg'
testImage = image.load_img(img_path, target_size=(224, 224))
data[0] = image.img_to_array(testImage)
data = preprocess_input(data)
predictions = model.predict(data)

for name, desc, score in decode_predictions(predictions)[0]:
    print('- {} ({:.2f}%%)'.format(desc, 100 * score))

