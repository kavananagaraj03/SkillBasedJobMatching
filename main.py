from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, login_required, LoginManager, current_user
from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load configuration from config.json
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/p_job'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)

# Define allowed file types and size limit for resume upload
ALLOWED_EXTENSIONS = {'mp4'}


# User Model
class Users(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100))
    address = db.Column(db.String(100))
    def get_id(self):
        return str(self.user_id)  # Convert user_id to string if needed

# Skill Model
class Skill(db.Model):
    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user_skill = db.Column(db.String(1000))

    def get_id(self):
        return str(self.skill_id)
  # Convert user_id to string if needed

# Company Model
class Company(db.Model):
    c_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    requirements = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    def get_id(self):
        return str(self.c_id)

# Resume Model
class Resume(db.Model):
    r_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    r_detail = db.Column(db.String(255), nullable=False, unique=True)  # Increased length to 255 characters
    def get_id(self):
        return str(self.r_id)

class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)

# Login Manager Loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()

        # Compare raw password instead of checking hashed password
        if user and user.password == password:
            login_user(user)
            flash("Login Success", "primary")
            return redirect(url_for('user'))
        else:
            flash("Invalid email or password", "danger")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        raw_password = request.form.get('password')  # Store raw password as is

        # Check if the email already exists
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email Already Exists", "warning")
            return redirect(url_for('signup'))
        else:
            new_user = Users(
                username=username,
                email=email,
                password=raw_password,  # Store password without hashing
                contact=request.form.get('contact'),
                address=request.form.get('address')
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Signup Success! Please Login", "success")
            return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    if request.method == 'POST':
        # Update user information if the form is submitted
        current_user.contact = request.form.get('contact')
        current_user.address = request.form.get('address')
        db.session.commit()
        flash("User details updated successfully", "success")
        return redirect(url_for('upload_resume'))  # Redirect to the same page after updating

    # Fetch user details from the database
    user_details = {
        'username': current_user.username,
        'email': current_user.email,
        'contact': current_user.contact,
        'address': current_user.address
    }

    return render_template('user.html', user_details=user_details)

@app.route('/resume', methods=['GET', 'POST'])
def upload_resume():
    existing_resume = Resume.query.filter_by(user_id=current_user.user_id).first()

    if request.method == 'POST':
        detail = request.form.get('details')
        if detail:
            if existing_resume:
                existing_resume.r_detail = detail
            else:
                new_resume = Resume(r_detail=detail, user_id=current_user.user_id)
                db.session.add(new_resume)

            db.session.commit()
            return redirect(url_for('input_skill'))
        else:
            # If details are not provided, stay on the same page and show an error message
            flash('Error: No resume details provided', 'error')
            return redirect(url_for('upload_resume'))
    
    return render_template('resume.html', existing_resume=existing_resume)


@app.route('/skill', methods=['GET', 'POST'])
@login_required
def input_skill():
    if request.method == 'POST':
        # Retrieve skills from form
        skills = [request.form.get('skill1'), request.form.get('skill2'), request.form.get('skill3')]
        # Filter out None values (if user left a skill dropdown untouched)
        skills = [skill for skill in skills if skill is not None]

        # Update or create Skill entries for the current user
        current_user_skills = Skill.query.filter_by(user_id=current_user.user_id).first()

        if current_user_skills:
            # Update existing skills
            current_user_skills.user_skill = ", ".join(skills)
        else:
            # Create new skills entry
            new_skills = Skill(
                user_id=current_user.user_id,
                user_skill=", ".join(skills)
            )
            db.session.add(new_skills)

        db.session.commit()
        flash('Skills saved successfully', 'success')
        return redirect(url_for('status'))

    return render_template('skill.html')

@app.route('/status')
@login_required
def status():
    matched_users = []
    companies = Company.query.all()
    user_skills = Skill.query.filter_by(user_id=current_user.user_id).all()

    for company in companies:
        for user in user_skills:
            user_skills_list = user.user_skill.split(',')
            company_requirements = company.requirements.split(',')

            if any(skill.strip() in company_requirements for skill in user_skills_list):
                matched_users.append({
                    'user_name': current_user.username,
                    'company_name': company.company_name,
                    'contact': company.contact,
                    'address': company.location
                })
                break

    if matched_users:
        return render_template('status.html', matched_users=matched_users)
    else:
        return redirect(url_for('add_course'))



@app.route('/course')
def add_course():
    # Fetch all courses from the database
    courses = Courses.query.all()
    return render_template('course.html', courses=courses)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul", "warning")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
