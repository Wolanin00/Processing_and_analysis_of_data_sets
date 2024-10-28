from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for, flash
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'franchise.db')}"
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Owner(db.Model):
    __tablename__ = "owners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

    locations = db.relationship("FranchiseLocation", back_populates="owner")


class FranchiseType(db.Model):
    __tablename__ = "franchise_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    locations = db.relationship("FranchiseLocation", back_populates="franchise_type")
    dishes = db.relationship("Dish", back_populates="franchise_type")


class Dish(db.Model):
    __tablename__ = "dishes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    franchise_type_id = db.Column(db.Integer, db.ForeignKey("franchise_types.id"))

    franchise_type = db.relationship("FranchiseType", back_populates="dishes")


class FranchiseLocation(db.Model):
    __tablename__ = "franchise_locations"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id"))
    franchise_type_id = db.Column(db.Integer, db.ForeignKey("franchise_types.id"))

    owner = db.relationship("Owner", back_populates="locations")
    franchise_type = db.relationship("FranchiseType", back_populates="locations")


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    owners = Owner.query.all()
    franchise_types = FranchiseType.query.all()
    return render_template('index.html', owners=owners, franchise_types=franchise_types)


@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        email = request.form['email']  # unique
        phone_number = request.form['phone_number']

        existing_owner = Owner.query.filter_by(email=email).first()
        if existing_owner:
            flash('Email already exists. Please use a different email.')
            return render_template('add_owner.html', name=name, surname=surname, age=age, phone_number=phone_number)
        try:
            age_int = float(age)
            if not age_int.is_integer():
                flash('Age must be integer.')
                return render_template('add_owner.html', name=name, surname=surname, email=email, phone_number=phone_number)
            if age_int < 18:
                flash('To become a founder, you must be of legal age.')
                return render_template('add_owner.html', name=name, surname=surname, email=email, phone_number=phone_number)
        except (ValueError, TypeError):
            flash('Age must be integer.')
            return render_template('add_owner.html', name=name, surname=surname, email=email, phone_number=phone_number)

        new_owner = Owner(name=name, surname=surname, age=age_int, email=email, phone_number=phone_number)
        db.session.add(new_owner)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_owner.html')


@app.route('/add_franchise_type', methods=['GET', 'POST'])
def add_franchise_type():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_type = FranchiseType(name=name, description=description)
        db.session.add(new_type)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_franchise_type.html')


@app.route('/add_dish_to_franchise_type', methods=['GET', 'POST'])
def add_dish_to_franchise_type():
    franchise_types = FranchiseType.query.all()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        franchise_type_id = request.form['franchise_type_id']
        new_dish = Dish(name=name, description=description, franchise_type_id=franchise_type_id, price=price)
        db.session.add(new_dish)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_dish_to_franchise_type.html', franchise_types=franchise_types)


@app.route('/assign_franchise_to_owner', methods=['GET', 'POST'])
def assign_franchise_to_owner():
    owners = Owner.query.all()
    franchise_types = FranchiseType.query.all()
    if request.method == 'POST':
        owner_id = request.form['owner_id']
        franchise_type_id = request.form['franchise_type_id']
        address = request.form['address']
        city = request.form['city']

        new_location = FranchiseLocation(
            address=address,
            city=city,
            owner_id=owner_id,
            franchise_type_id=franchise_type_id
        )
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('assign_franchise_to_owner.html', owners=owners, franchise_types=franchise_types)


@app.route('/get_franchise_types/<int:owner_id>')
def get_franchise_types(owner_id):
    franchises = FranchiseLocation.query.filter_by(owner_id=owner_id).all()
    franchise_types = [
        {"id": franchise.franchise_type.id, "name": franchise.franchise_type.name, "city": franchise.city,
         "address": franchise.address}
        for franchise in franchises
    ]
    return {"franchise_types": franchise_types}


@app.route('/get_dishes/<int:franchise_type_id>')
def get_dishes(franchise_type_id):
    dishes = Dish.query.filter_by(franchise_type_id=franchise_type_id).all()
    dish_data = [{"name": dish.name, "description": dish.description, "price": dish.price} for dish in dishes]
    return {"dishes": dish_data}


if __name__ == '__main__':
    app.run(debug=True)
