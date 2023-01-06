
import os
from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.db'
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    notes = db.relationship('Note', backref="person")


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    content = db.Column(db.Text, nullable=False)


with app.app_context():

    db.create_all()

#     person = Person(first_name='Michael', last_name='Boateng')
#     db.session.add(person)
#     db.session.commit()

#     note_1 = Note(person_id=person.id, content='First Note')
#     note_2 = Note(person_id=person.id, content='Second Note')
#     note_3 = Note(person_id=person.id, content='Third Note')

#     db.session.add(note_1)
#     db.session.add(note_2)
#     db.session.add(note_3)
#     db.session.commit()

    



notesFields = {
    'id': fields.Integer,
    'content': fields.String,
    'person_id': fields.Integer,
}

personFields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'notes': fields.List(fields.Nested(notesFields)),
}


class PersonsAPI(Resource):
    @marshal_with(personFields)
    def get(self):
        person = Person.query.all()
        return person

    @marshal_with(personFields)
    def post(self):
        data = request.json
        person = Person(first_name=data['first_name'], last_name=data['last_name'],)
        db.session.add(person)
        db.session.commit()
        return person


class NotesAPI(Resource):
    @marshal_with(notesFields)
    def get(self):
        notes = Note.query.all()
        return notes

    @marshal_with(notesFields)
    def post(self):
        data = request.json
        note = Note(content=data['content'], person_id=data['person_id'],)
        db.session.add(note)
        db.session.commit()
        return note



api.add_resource(PersonsAPI, '/person/')
api.add_resource(NotesAPI, '/notes/')



if __name__ == '__main__':
    app.run(debug=True)