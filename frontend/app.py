from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)

@app.route('/uploaded', methods=['POST'])
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

