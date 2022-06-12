from app import db
from sqlalchemy.dialects.mysql import TEXT

class kantong(db.Model):
    kantong_id = db.Column(db.Integer, primary_key=True)
    gambar = db.Column(db.TEXT)
    hasil_prediksi = db.Column(db.String(25))
    deskripsi_user = db.Column(db.String(100))

def __repr__(self):
    return '<Kantong {}>'.format(self.kantong_id)