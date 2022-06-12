from app import db

class userId(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

def __repr__(self):
    return '<UserId {}>'.format(self.email)