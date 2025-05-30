from app import db
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
    category = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Images <id={self.id}> category = {self.category}"
    pass