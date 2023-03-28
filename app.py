from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, BOOLEAN
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import datetime
import pandas as pd

app = Flask(__name__)
DB_NAME = "amet.db"
db = SQLAlchemy()
ma = Marshmallow(app)
CORS(app)

engine = create_engine("sqlite:///instance/amet.db", echo=True)
app.config['SECRET_KEY'] = 'myKey'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


class PaintingData(db.Model):
    __tablename__ = "paintingsData"

    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(100))
    tech = db.Column("tech", db.String(100))
    size = db.Column("size", db.String(100))
    price = db.Column("price", db.Integer)
    img = db.Column("img", db.String)
    created = db.Column("created", db.String)
    soldDate = db.Column("soldDate", db.String)
    sold = db.Column("sold", db.BOOLEAN)
    reserved = db.Column("reserved", db.BOOLEAN)
    reservedDate = db.Column(db.DateTime, default=datetime.datetime.now)
    showDOM = db.Column("showDOM", db.BOOLEAN)
    registerNum = db.Column("registerNum", db.Integer)

    def __init__(self, title, tech, size, price, img, created, soldDate, sold, reserved, reservedDate, showDOM, registerNum):
        self.title = title
        self.tech = tech
        self.size = size
        self.price = price
        self.img = img
        self.created = created
        self.soldDate = soldDate
        self.sold = sold
        self.reserved = reserved
        self.reservedDate = reservedDate
        self.showDOM = showDOM
        self.registerNum = registerNum

    def __repr__(self):
        return f"({self.id}) {self.title} {self.tech} {self.size} ({self.price}) {self.img} ({self.created}) {self.soldDate} {self.sold}) {self.reserved} {self.reservedDate} {self.showDOM} ({self.registerNum})"


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    telephone = db.Column("telephone", db.Integer)
    country = db.Column("country", db.String(100))
    feedback = db.Column("feedback", db.String(1000))
    registerNum = db.Column(
        db.Integer, ForeignKey("paintingsData.registerNum"))

    def __init__(self, name, last_name, email, telephone, country, feedback, registerNum):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.telephone = telephone
        self.country = country
        self.feedback = feedback
        self.registerNum = registerNum

    def __repr__(self):
        return f"{self.id} {self.name} {self.last_name} {self.email} {self.telephone} {self.country} {self.feedback} ({self.registerNum})"


class Fan(db.Model):
    __tablename__ = "fans"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    telephone = db.Column("telephone", db.Integer)
    country = db.Column("country", db.String(100))
    feedback = db.Column("feedback", db.String(1000))

    def __init__(self, name, last_name, telephone, country, email, feedback):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.telephone = telephone
        self.country = country
        self.feedback = feedback

    def __repr__(self):
        return f"{self.id} {self.name} {self.last_name} {self.email} {self.telephone} {self.country} {self.feedback}"


class PaintingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'tech', 'size',
                  'price', 'img', 'created', 'soldDate', 'sold', 'reserved', 'reservedDate', 'showDOM', 'registerNum')


class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'last_name', 'email', 'telephone',
                  'country', 'feedback', 'registerNum')


class FanSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'last_name',
                  'email', 'telephone', 'country', 'feedback')


painting_schema = PaintingSchema()
paintings_schema = PaintingSchema(many=True)
customer_schema = CustomerSchema()
fan_schema = FanSchema()

'''
with app.app_context():
    db.create_all()
'''


@app.route('/painting', methods=['GET'])
def get_paintings():
    available_paintings = PaintingData.query.all()
    results = paintings_schema.dump(available_paintings)
    return jsonify(results)


@app.route('/painting/<id>', methods=['GET'])
def single_painting(id):
    painting = PaintingData.query.get(id)
    results = painting_schema.jsonify(painting)
    return results


@app.route('/customer', methods=['POST'])
def add_customer():
    name = request.json['name']
    last_name = request.json['last_name']
    email = request.json['email']
    telephone = request.json['telephone']
    country = request.json['country']
    feedback = request.json['feedback']
    registerNum = request.json['registerNum']

    customer = Customer(name, last_name, email,
                        telephone, country, feedback, registerNum)
    db.session.add(customer)
    db.session.commit()

    return customer_schema.jsonify(customer)


@app.route('/fan', methods=['POST'])
def add_fan():
    name = request.json['name']
    last_name = request.json['last_name']
    email = request.json['email']
    telephone = request.json['telephone']
    country = request.json['country']
    feedback = request.json['feedback']

    fan = Fan(name, last_name, email,
              telephone, country, feedback)
    db.session.add(fan)
    db.session.commit()

    return fan_schema.jsonify(fan)


@app.route('/update/<id>', methods=['PATCH'])
def update_painting(id):
    painting = PaintingData.query.get(id)

    reserved = request.json['reserved']
    registerNum = request.json['registerNum']

    painting.reserved = reserved
    painting.registerNum = registerNum

    db.session.commit()
    results = painting_schema.jsonify(painting)

    return results


@app.route('/delete-customer/<id>', methods=['DELETE'])
def delete_customer(id):
    painting = Customer.query.get(id)
    db.session.delete(painting)
    db.session.commit()
    results = painting_schema.jsonify(painting)

    return results


@app.route('/delete-fan/<id>', methods=['DELETE'])
def delete_fan(id):
    painting = Fan.query.get(id)
    db.session.delete(painting)
    db.session.commit()
    results = painting_schema.jsonify(painting)

    return results


# SQL command to retrieve data
comm1 = "SELECT * FROM paintingsData"
comm2 = "SELECT * FROM customers"
comm3 = "SELECT * FROM fans"

# Read data from SQL using pandas
df1 = pd.read_sql_query(comm1, con=engine)
df2 = pd.read_sql_query(comm2, con=engine)
df3 = pd.read_sql_query(comm3, con=engine)

# Export data to excel
with pd.ExcelWriter('Amet_data2.xlsx') as writer:
    df1.to_excel(writer, sheet_name='paintingsData')
    df2.to_excel(writer, sheet_name='customers')
    df3.to_excel(writer, sheet_name='fans')

if __name__ == "__main__":
    app.run(debug=True)
