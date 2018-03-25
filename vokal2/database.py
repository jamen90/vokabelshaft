import os
import sys
from flask_sqlalchemy import SQLAlchemy
from index import app, db


class Vokabel(db.Model):

	id = db.Column('wort_id', db.Integer, primary_key=True)
	wort = db.Column(db.String(45))
	bedeutung = db.Column(db.String(45))
	beispiel = db.Column(db.String(250))
	quelle_id = db.Column(db.Integer, db.ForeignKey('quelle.id'))

	quelle = db.relationship("Quelle", backref=db.backref("Vokabel", lazy=True))


class Quelle(db.Model):

	id = db.Column('id', db.Integer, primary_key=True)
	title = db.Column(db.String(250), unique=True)

def create():
	db.create_all()

	return

