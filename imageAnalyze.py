import keras

base_model = keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'  # pretrained weights
)
base_model.trainable = False  # freeze base model

model = keras.Sequential([
    base_model,
    keras.layers.GlobalAveragePooling2D(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(13, activation='softmax')  # adjust for your dataset
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Define image size and batch
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

train_ds = keras.preprocessing.image_dataset_from_directory(
    "dataset/train",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='int'  # or 'categorical' if you want one-hot
)

val_ds = keras.preprocessing.image_dataset_from_directory(
    "dataset/validation",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='int'
)

class_names = train_ds.class_names
print("Class names:", class_names)

model.fit(train_ds, validation_data=val_ds, epochs=10)

import numpy as np
from keras.preprocessing import image

img = image.load_img("dataset/train/styrofoam/000001.jpg", target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)  # Make batch of 1

predictions = model.predict(img_array)
predicted_class = class_names[np.argmax(predictions[0])]
print("Predicted class:", predicted_class)