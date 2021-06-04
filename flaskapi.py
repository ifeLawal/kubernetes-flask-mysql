"""Code for a flask API to Create, Read, Update, Delete users"""
import os
from flask import jsonify, request, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# MySQL configurations
username = "root"
password = os.getenv("db_root_password", "")
db_name = os.getenv("db_name", "users")
service = os.getenv("MYSQL_SERVICE_HOST", "localhost")
service += ":" + int(os.getenv("MYSQL_SERVICE_PORT")) if os.getenv("MYSQL_SERVICE_PORT") else ""
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{username}:{password}@{service}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

ma = Marshmallow()  # Not passing `app`
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return "Hello, world!"

@app.route("/first")
def first_user():
    admin = User('admin', 'password', 'admin@example.com')
    db.session.add(admin)
    db.session.commit()
    resp = UserSchema().jsonify(admin)
    resp.status_code = 200
    return resp
    
@app.route("/create", methods=["POST"])
def add_user():
    """Function to create a user to the MySQL database"""
    json = request.json
    name = json["name"]
    email = json["email"]
    pwd = json["pwd"]
    if name and email and pwd and request.method == "POST":
        try:
            user = User(username=name, password=pwd, email=email)
            db.session.add(user)
            db.session.commit()
            resp = jsonify("User created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide name, email and pwd")


@app.route("/users", methods=["GET"])
def users():
    """Function to retrieve all users from the MySQL database"""
    try:
        resp = UserSchema(many=True).jsonify(User.query.all())
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/user/<int:user_id>", methods=["GET"])
def user(user_id):
    """Function to get information of a specific user in the MSQL database"""
    try:
        user = User.query.filter_by(id=user_id).first_or_404()
        resp = UserSchema().jsonify(user)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/update", methods=["POST"])
def update_user():
    """Function to update a user in the MYSQL database"""
    json = request.json
    name = json["name"]
    email = json["email"]
    pwd = json["pwd"]
    user_id = json["user_id"]
    if name and email and pwd and user_id and request.method == "POST":
        # save edits
        try:
            user = User.query.filter_by(id=user_id).first_or_404()
            user.username = name
            user.password = pwd
            user.email = email
            db.session.commit()
            resp = jsonify("User updated successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide id, name, email and pwd")


@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    """Function to delete a user from the MySQL database"""
    try:
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        resp = jsonify("User deleted successfully!")
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))

db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
