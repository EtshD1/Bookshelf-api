from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def update(self):
        db.session.commit()
        db.session.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    def getJson(self):
        return jsonify({
            'id': self.id,
            'name': self.name,
            'author': self.author
        })