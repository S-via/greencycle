from flask import Flask, request, jsonify
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///greencycle.db'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

@app.route('/updated', methods=['POST','GET'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image uploaded'}), 400

    image_file = request.files['image']

    try:
        image = Image.open(image_file.stream)
        # Dummy analysis
        width, height = image.size
        result = f"Image received. Size: {width}x{height}"
        return jsonify({'message': result})

    except Exception as e:
        return jsonify({'message': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

