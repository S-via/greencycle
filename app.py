from flask import Flask, request, jsonify
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app) # allow requests from React frontend
# initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///greencycle.db'
db = SQLAlchemy(app)

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

@app.route('/', methods=['POST'])
def upload_image():
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
        
        return jsonify({'message': "Image saved."})

    except Exception as e:
        return jsonify({'message': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

