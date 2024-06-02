from flask import Flask, request,render_template, redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)

# MySQL Configuration choose your port no and password this is a dummy thing i have set up
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/HiveHaven'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
app.secret_key="secret"

app.config['SQLALCHEMY_ECHO'] = True


class Apartment(db.Model):
    apartment_id = db.Column(db.String(100), primary_key=True)
    apartment_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))


class Users(db.Model):
    user_id = db.Column(db.String(100), primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(40))
    apartment_id = db.Column(db.String(100), db.ForeignKey('apartment.apartment_id'))
    house_no = db.Column(db.Integer)
    email = db.Column(db.String(255), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)

    def __init__(self,user_id,user_name,phone_no,apartment_id,house_no,email,user_password):
        self.user_id=user_id
        self.user_name=user_name
        self.phone_no=phone_no
        self.apartment_id=apartment_id
        self.house_no=house_no
        self.email=email
        self.user_password=bcrypt.hashpw(user_password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,user_password):
        return bcrypt.checkpw(user_password.encode('utf-8'),self.user_password.encode('utf-8'))


class Admin(db.Model):
    admin_id = db.Column(db.String(100), primary_key=True)
    admin_name = db.Column(db.String(100), nullable=False)
    apartment_id = db.Column(db.String(100), db.ForeignKey('apartment.apartment_id'))
    email = db.Column(db.String(255), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)

    def __init__(self, admin_id, admin_name, apartment_id, email, admin_password):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.apartment_id = apartment_id
        self.email = email
        self.admin_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, admin_password):
        return bcrypt.checkpw(admin_password.encode('utf-8'), self.admin_password.encode('utf-8'))


class Department(db.Model):
    apartment_id = db.Column(db.String(100), db.ForeignKey('apartment.apartment_id'), primary_key=True)
    dep_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)

class DepartmentComplaint(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), db.ForeignKey('users.user_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.dep_id'))
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(800))
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class NeighborComplaint(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), db.ForeignKey('users.user_id'))
    neighbor_user_id = db.Column(db.String(100), db.ForeignKey('users.user_id'))
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(800))
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


# Routes for users
@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/register',methods=['GET','POST'])
def register():
    all_apartments=Apartment.query.all()
    if request.method=='POST':
        user_name=request.form['user_name']
        phone_no=request.form['phone_no']
        apartment_id=request.form['apartment_id']
        house_no=request.form['house_no']
        email=request.form['email']
        user_password=request.form['user_password']
        user_id=apartment_id+"-"+house_no
        
        try:
            user_exist=Users.query.filter_by(user_id=user_id).first()
        except error as e:
            return render_template('./register.html',error=e,all_apartments=all_apartments)

        # user_exist1=Users.query.filter_by(user_id=user_id).first()
        if user_exist and user_exist.apartment_id==apartment_id:
            error="User already exist please"
            return render_template('./register.html',error=error,all_apartments=all_apartments)
        else:
            user=Users(user_id=user_id,user_name=user_name,phone_no=phone_no,apartment_id=apartment_id,house_no=house_no,email=email,user_password=user_password)
            db.session.add(user)
            db.session.commit() 
            sucess="Registered Sucessfull Please login"
            return render_template('./register.html',sucess=sucess,all_apartments=all_apartments)

    
    return render_template('./register.html',all_apartments=all_apartments)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=Users.query.filter_by(email=email).first()

        if user and user.check_password(password):
            print("valid")
            session['email']=email
            session['user_id']=user.user_id
            session['apartment_id']=user.apartment_id
            return redirect(url_for("home"))
        else:
            print("invalid")
            error="Incorrect Password"
            return render_template('/login.html',error=error)

    return render_template('/login.html')


@app.route('/home',methods=['GET','POST'])
def home(): 
    if session['user_id']:
        user_id=session['user_id']
        user=Users.query.filter_by(user_id=user_id).first()
        personal_complaints = NeighborComplaint.query.filter_by(user_id=user_id).all()
        department_complaints = DepartmentComplaint.query.filter_by(user_id=user_id).all()
        complaints_on_me = NeighborComplaint.query.filter_by(neighbor_user_id=user_id).all()
        # print(user)
        # print(complaints_on_me )
        # print("Personal Complaints:", personal_complaints)
        # print("Department Complaints:", department_complaints)
        # print("Complaints On Me:", complaints_on_me)
        return render_template('/home.html',user=user,personal_complaints=personal_complaints,department_complaints=department_complaints,complaints_on_me=complaints_on_me)
    return render_template('/home.html')

@app.route('/personal_complaint', methods=['GET','POST'])
def personal_complaint():
    user_id=session['user_id']
    apartment_id=session['apartment_id']
    all_user=Users.query.filter_by(apartment_id=apartment_id).all()
    if request.method=='POST':
        neighbor_user_id=request.form['neighbor_user_id']
        subject=request.form['subject']
        description=request.form['description']
        
        complaint=NeighborComplaint(user_id=user_id,neighbor_user_id=neighbor_user_id,subject=subject,description=description)
        db.session.add(complaint)
        db.session.commit()

        sucess="Complainent registered Sucessfully"
        return redirect(url_for('personal_complaint'))
    return render_template("./personal_complaint.html",all_user=all_user)


@app.route('/department_complaint', methods=['GET','POST'])
def department_complaint():
    user_id=session['user_id']
    apartment_id=session['apartment_id']
    all_department=Department.query.filter_by(apartment_id=apartment_id).all()
    
    if request.method=='POST':
        department_id=request.form['department_id']
        subject=request.form['subject']
        description=request.form['description']

        complaint=DepartmentComplaint(user_id=user_id,department_id=department_id,subject=subject,description=description)
        db.session.add(complaint)
        db.session.commit()
        print("done")
        return redirect(url_for('department_complaint'))
    return render_template("/department_complaint.html",all_department=all_department)


#admin routes for the appartment
app.route('/admin/login',methods=['GET','POST'])
def admin_login():
    return 

app.route('/admin/login/home',methods=['GET','POST'])
def admin_home():
    return

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=3000)
