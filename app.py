from flask import Flask, request, jsonify
from PIL import Image as Pilimage
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from recyclingGuide import RECYCLING_GUIDE
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
import io

app = Flask(__name__)
CORS(app) # allow requests from React frontend
# initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///greencycle.db'
db = SQLAlchemy(app)
class_names = ['battery', 'cardboard', 'cigarette', 'diaper', 'electronics', 'food_waste', 'glass']
# model
"""
Examples for mimetype
"image/jpeg" for JPEG images
"image/png" for PNG images
"image/gif" for GIF images
"image/bmp" for BMP images
"""
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)
    # category check inside dictionary key

    def __repr__(self):
        return f"Images <id={self.id}> category = {self.category}"
    pass

class User():
    # id
    pass

with app.app_context():
    db.create_all()

@app.route('/uploaded', methods=['GET','POST'])
def upload_image():
    if request.method == 'GET':
        return jsonify({'message': 'GreenCycle upload endpoint is active'}), 200
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'message': 'No image uploaded'}), 400

        image_file = request.files['image']
        file_name = image_file.filename
        mime = image_file.mimetype

        try:
            
            # Read image data as bytes
            image_bytes = image_file.read()
            # Save to database
            new_image = Image(data=image_bytes, file_name=file_name, mimetype=mime)
            db.session.add(new_image)
            db.session.commit()
            print("test")
            # analyze image 
            # Convert binary data to PIL Image
            img_pil = Pilimage.open(io.BytesIO(new_image.data)).convert('RGB')
            print(img_pil)
            model = keras.models.load_model("recycler_model.h5")
            # Convert to array and prepare for prediction
            # Resize to 224x224
            img_resized = img_pil.resize((224, 224))

            # Convert to NumPy array
            img_array = np.array(img_resized)

            # Normalize if needed (depending on your model's preprocessing)
            img_array = img_array / 255.0

            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)  # Shape: (1, 224, 224, 3)

            # Predict
            predictions = model.predict(img_array)
            predicted_class = class_names[np.argmax(predictions[0])]

            print("Predicted class:", predicted_class)
            # find category
            category = predicted_class
            
            return jsonify({'message': f"Image saved. <br> Category: {category}<br> Instruction:<br> {RECYCLING_GUIDE[category]}"})

        except Exception as e:
            return jsonify({'message': f"Error: {str(e)}"}), 500
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)

