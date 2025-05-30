from flask import Flask, request, jsonify
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # allow requests from React frontend
# initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///greencycle.db'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

@app.route('/uploaded', methods=['POST', 'GET'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image uploaded'}), 400

    image_file = request.files['image']
    file_name = image_file.filename
    mime = image_file.mimetype
    category = 'unknown'

    try:
        # Read image data as bytes
        image_bytes = image_file.read()
        
        # Save to database
        from models.image import Image
        new_image = Image(data=image_bytes, file_name=file_name, mimetype=mime, category=category)
        db.session.add(new_image)
        db.session.commit()
        
        return jsonify({'message': f"Image saved. {new_image}"})

    except Exception as e:
        return jsonify({'message': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

