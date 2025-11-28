from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Menu(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column("name", db.String(100))
	price = db.Column("price", db.Float)
	image = db.Column("image", db.String(100))

	def __init__(self, name, price, image):
		self.name = name
		self.price = price
		self.image = image

class Ovqat(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	tanlov = db.Column("tanlov", db.ForeignKey('menu.id', name='fk_ovqat_menu'), nullable=False)
	quantity = db.Column("quantity", db.Integer)

	def __init__(self, tanlov, quantity):
			self.tanlov = tanlov
			self.quantity = quantity

class Customer(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	customer_name = db.Column("customer_name", db.String(100))
	age = db.Column("age", db.Integer)
	last_visit = db.Column("last_visit", db.DateTime)

	def __init__(self, customer_name, age):
		self.customer_name = customer_name
		self.age = age
		self.last_visit = datetime.now()

class Buyurtma(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	ovqat = db.Column("ovqat", db.ForeignKey('ovqat.id', name='fk_buyurtma_ovqat'), nullable=False)
	total_price = db.Column("total_price", db.Float)
	cooking_time = db.Column("cooking_time", db.Float)
	payment_type = db.Column("payment_type", db.String)
	created_at = db.Column("created_at", db.DateTime)
	customer = db.Column("customer", db.ForeignKey('customer.id', name="fk_buyurtma_customer"), nullable=True)

	def __init__(self, ovqat, total_price, cooking_time, payment_type, customer):
		self.ovqat = ovqat
		self.total_price = total_price
		self.cooking_time = cooking_time
		self.total_price = total_price
		self.payment_type = payment_type
		self.customer = customer
		self.created_at = datetime.now()

class Employee(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	lavozim = db.Column("lavozim", db.String(100))
	age = db.Column("age", db.Integer)
	name = db.Column("name", db.String(100))
	gender = db.Column("gender", db.String(100))
	worktime_from = db.Column("worktime_from", db.Integer)
	worktime_to = db.Column("worktime_to", db.Integer)
	is_ceoLevel = db.Column("is_ceoLevel", db.Boolean)
	workplace = db.Column("workplace", db.ForeignKey("restorant.id", name="fk_employee_workplace"), nullable=False)

	def __init__(self, lavozim, age, name, gender, worktime_from, worktime_to, is_ceoLevel, workplace):
		self.lavozim = lavozim
		self.age = age
		self.name = name
		self.gender = gender
		self.worktime_from = worktime_from
		self.worktime_to = worktime_to
		self.is_ceoLevel = is_ceoLevel
		self.workplace = workplace

class Restorant(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column("name", db.String(100))
	filial = db.Column("filial", db.Integer)
	izoh = db.Column("izoh", db.String(100))
	menu = db.Column("menu", db.ForeignKey('menu.id', name="fk_restorant_menu"), nullable=False)
