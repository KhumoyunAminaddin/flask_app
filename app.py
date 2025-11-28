from flask import Flask, redirect, url_for, render_template, request, session, flash
from wtforms import (Form, StringField, IntegerField, FieldList, validators, SubmitField,
					 FormField, SelectField, RadioField, BooleanField)
from datetime import timedelta
from custom_models import db, Menu, Restorant, Employee, Buyurtma, Customer, Ovqat
from flask_migrate import Migrate

def create_app():
	app = Flask(__name__)
	app.secret_key = "adsfihjoiwefhewfh9238h2fh"
	app.permanent_session_lifetime = timedelta(hours=5)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Menu.test.db'

	db.init_app(app)
	migrate = Migrate(app, db)
	with app.app_context():
		from custom_models import Menu
		db.create_all()

	return app

app = create_app()

class MenuForm(Form):
	name = StringField('name', validators=[validators.Length(min=1, max=25)])
	price = IntegerField('price', validators=[validators.NumberRange(min=1)])
	image = StringField('image', validators=[validators.Length(min=1, max=100)])
	submit = SubmitField('Saqlash')

class RestoranForm(Form):
	name = StringField('name', validators=[validators.Length(max=25)])
	filial = StringField('filial', validators=[validators.Length(max=25)])
	izoh = StringField('izoh', validators=[validators.Length(max=25)])
	menu = SelectField("Menu", coerce=int)
	submit = SubmitField('Saqlash')

class EmployeeForm(Form):
	name = StringField('name', validators=[validators.Length(max=100)])
	age = IntegerField('age', validators=[validators.NumberRange(min=1)])
	lavozim = StringField('lavozim', validators=[validators.Length(max=100)])
	gender = RadioField('gender', choices=[(1, 'Male'), (0, 'Female')])
	worktime_from = IntegerField('worktime_from', validators=[validators.NumberRange(min=0, max=23)])
	worktime_to = IntegerField('wortime_to', validators=[validators.NumberRange(min=0, max=23)])
	is_ceoLevel = BooleanField('is_ceoLevel')
	workplace = SelectField("Workplace", coerce=int)
	submit = SubmitField('Saqlash')

# ROUTING
@app.route('/admin', methods=["GET", "POST"])
def admin():
	form = MenuForm(request.form)
	form2 = RestoranForm(request.form)
	form3 = EmployeeForm(request.form)
	form2.menu.choices = [(m.id, m.name) for m in Menu.query.all()]
	form3.workplace.choices = [(m.id, m.name) for m in Restorant.query.all()]
	if request.method == 'POST':
		if form.validate():
			menu = Menu(name=form.name.data,
				 price=form.price.data,
				 image=form.image.data)
			db.session.add(menu)
			db.session.commit()
			flash("Muvafaqiyatli qo'shildi")
			return redirect(url_for('admin'))
		if form2.validate():
			restoran = Restorant(name=form2.name.data,
					 	filial=form2.filial.data,
						izoh=form2.izoh.data,
						menu=form2.menu.data)
			db.session.add(restoran)
			db.session.commit()
			return redirect(url_for('admin'))
		if form3.validate():
			employee = Employee(name=form3.name.data,
								age=form3.age.data,
								lavozim=form3.lavozim.data,
								gender=form3.gender.data,
								worktime_from=form3.worktime_from.data,
								worktime_to=form3.worktime_to.data,
								is_ceoLevel=form3.is_ceoLevel.data,
								workplace=form3.workplace.data
								)
			db.session.add(employee)
			db.session.commit()
			return redirect(url_for('admin'))
	if "user" in session:
		if session["user"] == "Bobur":
			return render_template("admin.html", form=form, form2=form2, form3=form3)
		else:
			return redirect(url_for("login"))
	return redirect(url_for("login"))

@app.route("/")
def home():
		menular = Menu.query.all()
		return render_template("index.html", content=menular)

@app.route("/<param>", methods=["GET", "POST"])
def page(param):
	if "user" in session:
		customer = Customer.query.filter_by(customer_name=session["user"]).first().id
		if request.method == "POST":
			formdata = request.form.to_dict()
			for key, value in formdata.items():
				ov = Ovqat(tanlov=int(key), quantity=value)
				db.session.add(ov)
				db.session.commit()
				b = Buyurtma(ovqat=int(key),
						 total_price=int(value)*Menu.query.filter_by(id=int(key)).first().price,
						 cooking_time=10,
						 payment_type="cash",
						 customer = customer)
				db.session.add(b)
				db.session.commit()
			return render_template("details.html", data=param, menu=Menu.query.all(),
								   content=Buyurtma.query.filter_by(customer=customer).all())

		content = [{"name": Menu.query.filter_by(id=(Ovqat.query.filter_by(id=x.ovqat).first().tanlov)).first().name,
					"quantity": Ovqat.query.filter_by(id=x.ovqat).first().quantity,
					"price": x.total_price } for x in Buyurtma.query.filter_by(customer=customer).all()]
		return render_template("details.html", data=param, menu=Menu.query.all(),
							   content=content)
	return render_template("details.html", data=param, menu=Menu.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
	if "user" in session:
		return redirect(url_for("page", param=session["user"]))
	if request.method == "POST":
		user = request.form["login"]
		session["user"] = user
		cs = Customer(customer_name=user,
					  age=0)
		db.session.add(cs)
		db.session.commit()
		return redirect(url_for("page", param=user))
	return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
	if "user" in session:
		session.pop("user")
		return redirect(url_for("home"))
	else:
		return redirect(url_for("home"))


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
