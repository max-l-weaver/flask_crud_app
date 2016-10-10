#!/usr/bin/python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
import uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/cruddyapp.db'
db = SQLAlchemy(app)

class User(db.Model):

	__tablename__ = 'users'

 	id = db.Column(db.String, primary_key=True)
	ip = db.Column(db.String(50))
	username = db.Column(db.String(50), unique=True)
	timestamp = db.Column(db.String(100))

	def __init__(self, username):
		self.username = username
		self.ip = request.environ['REMOTE_ADDR']
		self.id = str(uuid.uuid1())
		self.timestamp = str(datetime.now())

	def __repr__(self):
		return '<user %r>' % self.ip


@app.route('/')
def index():
	return "Welcome to the world's greatest CRUD app"

@app.route('/user/<username>')
def add_user(username):
	new_user = User(username)
	try:
		db.session.add(new_user)
		db.session.commit()
		return 'New user added, sucka!'
	except:
		return 'Whoops, user already exists, fool!'


@app.route('/user/listall')
def list_all_users():
	all_users = User.query.all()
	list_dict = []

	for user in all_users:
		user_dict = {
			"id": user.id,
			"username": user.username,
			"ip": user.ip,
			"time_created": user.timestamp
		}
		list_dict.append(user_dict)
	return jsonify(list_dict)

@app.route('/user/delete/<username>')
def delete_user(username):
	user_to_delete = User.query.filter_by(username=username).first()
	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		return 'Dey gone!'
	except:
		return "That user ain't there to delete, dummy!"


if __name__ == '__main__':
	db.create_all()
	app.run(debug=True, host='0.0.0.0', port=5000)