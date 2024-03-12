from flask import Flask, request,render_template, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

# MySQL Configuration choose your port no and password this is a dummy thing i have set up
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/Hivehaven'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.secret_key="secret"



class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(40))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    house_no = db.Column(db.Integer)
    email = db.Column(db.String(255), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)

    def __init__(self,user_name,phone,apartment_id,house_no,email,password):
        self.user_name=user_name
        self.phone_no=phone
        self.apartment_id=apartment_id
        self.house_no=house_no
        self.email=email
        self.user_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.user_password.encode('utf-8'))
        

    
class Department(db.Model):
    dep_id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    department_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)

class DepartmentComplaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.dep_id'))
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(800))
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class NeighborComplaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    neighbor_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(800))
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


@app.route('/')
def index_page():
    return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('/login.html')


@app.route('/register',methods=['GET','POST'])
def register():
    return render_template('register.html')


@app.route('/home')
def home():
    return render_template('/home.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

