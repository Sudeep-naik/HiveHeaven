from flask import Flask, flash, jsonify, request,render_template, redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
import stripe
app = Flask(__name__)

# MySQL Configuration choose your port no and password this is a dummy thing i have set up
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root%4014@localhost/web_project'
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
    return render_template("./personal_complaint.html",all_user=all_user,user_id=user_id)


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

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


#admin routes for the appartment
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']
        admin = Admin.query.filter_by(admin_id=admin_id).first()

        if admin and admin.check_password(password):  
            session['admin_id'] = admin_id
            session['admin_apartment_id']=admin.apartment_id
            return redirect(url_for("admin_home"))
        else:
            error = "Incorrect Admin ID or Password"
            return render_template('admin_login.html', error=error)

    return render_template('admin_login.html')


@app.route('/admin/login/home',methods=['GET','POST'])
def admin_home():
    if 'admin_id' in session:
        apartment_id = session['admin_apartment_id']
        users = Users.query.filter_by(apartment_id=apartment_id).all()
        return render_template('admin_home.html', users=users)
    return render_template("admin_home.html")


@app.route('/admin/personal_complaints',methods=['GET','POST'])
def personal_complaints():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    apartment_id = session['admin_apartment_id']
    unresolved_complaints = db.session.query(NeighborComplaint).join(
        Users, NeighborComplaint.user_id == Users.user_id
    ).filter(
        NeighborComplaint.status == 0,
        Users.apartment_id == apartment_id
    ).all()
    
    return render_template('show_personal_complaints.html', complaints=unresolved_complaints)

@app.route('/admin/resolve_complaint/<int:complaint_id>', methods=['POST'])
def resolve_complaint(complaint_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    complaint = NeighborComplaint.query.get(complaint_id)
    if complaint:
        complaint.status = 1  # Update status to resolved
        db.session.commit()
    
    return redirect(url_for('personal_complaints'))


@app.route('/admin/department_complaints', methods=['GET'])
def view_department_complaints():
    if 'admin_id' in session:
        apartment_id = session.get('admin_apartment_id')
        unresolved_complaints = (db.session.query(DepartmentComplaint)
                                 .join(Users, DepartmentComplaint.user_id == Users.user_id)
                                 .filter(Users.apartment_id == apartment_id, DepartmentComplaint.status == 0)
                                 .all())
        return render_template('show_department_complaints.html', complaints=unresolved_complaints)
    return redirect(url_for('admin_login'))


@app.route('/admin/resolve_department_complaint/<int:complaint_id>', methods=['POST'])
def resolve_department_complaint(complaint_id):
    complaint = DepartmentComplaint.query.get(complaint_id)
    if complaint:
        complaint.status = 1
        db.session.commit()
    return redirect(url_for('view_department_complaints'))


@app.route('/admin/view_departments', methods=['GET'])
def view_departments():
    if 'admin_id' in session:
        apartment_id = session.get('admin_apartment_id')
        departments = Department.query.filter_by(apartment_id=apartment_id).all()
        return render_template('view_departments.html', departments=departments)
    return redirect(url_for('admin_login'))

@app.route('/admin/add_department', methods=['GET', 'POST'])
def add_department():
    if 'admin_id' in session:
        if request.method == 'POST':
            department_name = request.form['department_name']
            email = request.form['email']
            apartment_id = session.get('admin_apartment_id')

            new_department = Department(
                apartment_id=apartment_id,
                department_name=department_name,
                email=email
            )

            db.session.add(new_department)
            db.session.commit()

            return redirect(url_for('view_departments'))

        return render_template('add_department.html')
    return redirect(url_for('admin_login'))



#provider routes
public_key="pk_test_51PNeFpP65uOQnXwlT6Mscw8mNhequpRd7yIDQRCenPWCnyR7ZqVmmPFzLnqnEdbCdz0Nmb2hdge8pUJ8s6Laevcy00EsVjvCvO"
stripe.api_key="sk_test_51PNeFpP65uOQnXwl0Fv0dEH33o2GN1IVmbePHZ0ImGutSXax3YZHPmZI3f4W6VlvaRMxzgv4eJVkOdWlfN0HQ3iq00Uhkhcnzd"


@app.route('/add_apartment', methods=['POST', 'GET'])
def add_apartment():
    if request.method == 'POST':
        apartment_name = request.form['apartment_name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']

        # try:
            # CUSTOMER INFO
        customer = stripe.Customer.create(
            email=request.form['stripeEmail'],
            source=request.form['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=1999,  # 19.99
            currency='usd',
            description='Donation'
        )
        record_count = db.session.query(Apartment).count()
        apartment_id="APT00"+str(record_count+1)

        apartment=Apartment(apartment_id=apartment_id,apartment_name=apartment_name,address=address,city=city,state=state)
        db.session.add(apartment)
        db.session.commit()
        sucess="Apartment Registered Sucessfully"
        return redirect(url_for('register_admin',apartment_id=apartment.apartment_id,sucess=sucess))
        # except stripe.error.StripeError as e:
        #     # The Stripe API returned an error.
        #     # You can examine the error's type and message to handle different kinds of errors.
        #     flash(f"Stripe Error: {e}")
        #     return redirect(url_for('error'))
        # except KeyError as e:
        #     # The required form data was missing.
        #     flash(f"Missing form data: {e}")
        #     return redirect(url_for('error'))
        # except Exception as e:
        #     # Some other error occurred.
        #     flash(f"Unexpected Error: {e}")
        #     return redirect(url_for('error'))

    return render_template('add_apartment.html',public_key=public_key)


@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    apartment_id = request.args.get('apartment_id')
    all_apartments = Apartment.query.all()
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        apartment_id = request.form['apartment_id']
        email = request.form['email']
        admin_password = request.form['admin_password']
        admin_id = apartment_id + "-admin"

        try:
            admin_exist = Admin.query.filter_by(admin_id=admin_id).first()
        except exc.SQLAlchemyError as e:
            return render_template('./register_admin.html', error=str(e), all_apartments=all_apartments)

        if admin_exist:
            error = "Admin already exists for this apartment"
            return render_template('./register_admin.html', error=error, all_apartments=all_apartments)
        else:
            admin = Admin(admin_id=admin_id, admin_name=admin_name, apartment_id=apartment_id, email=email, admin_password=admin_password)
            db.session.add(admin)
            db.session.commit()
            success = "Admin registered successfully"
            return render_template("admin_login.html")

    return render_template('./register_admin.html', all_apartments=all_apartments, selected_apartment_id=apartment_id)


@app.route('/provider/home')
def provider_home():
    all_apartments=Apartment.query.all()
    return render_template('provider_home.html',all_apartments=all_apartments)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=3000)
