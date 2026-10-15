from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a_very_secret_key_for_sessions' # Required for secure logins

db = SQLAlchemy(app)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirects users here if they aren't logged in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==========================================
# DATABASE MODELS
# ==========================================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student') # admin, tutor, student
    is_approved = db.Column(db.Boolean, default=False) # Mostly for tutors
    
    # Relationships to link this user to other tables
    courses = db.relationship('Course', backref='tutor', lazy=True)
    bookings = db.relationship('Booking', backref='student', lazy=True)
    testimonials = db.relationship('Testimonial', backref='author', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False) # e.g., "Japanese", "Calculus"
    category = db.Column(db.String(50), nullable=False) # e.g., "Foreign Language", "Math"
    
    courses = db.relationship('Course', backref='subject', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    bookings = db.relationship('Booking', backref='course', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    schedule_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, Confirmed, Completed, Cancelled
    payment_status = db.Column(db.String(20), default='Unpaid') # Unpaid, Paid (For our dummy GCash)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    is_featured = db.Column(db.Boolean, default=False)

# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return "Email already exists! Click back and try again."

        # Scramble the password for security
        hashed_password = generate_password_hash(password)
        
        # Create the new user and save to database
        new_user = User(name=name, email=email, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find the user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password matches
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
            
        return "Invalid email or password. Click back and try again."
        
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name, role=current_user.role)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/tutor/course/create', methods=['GET', 'POST'])
@login_required
def create_course():
    # Security check: Only let tutors in
    if current_user.role != 'tutor':
        return "Access Denied: You must be a tutor to create a course."

    if request.method == 'POST':
        title = request.form.get('title')
        subject_id = request.form.get('subject_id')
        description = request.form.get('description')
        hourly_rate = request.form.get('hourly_rate')

        # Save the new course to the database, linking it to the current logged-in tutor
        new_course = Course(
            title=title, 
            subject_id=subject_id, 
            description=description, 
            hourly_rate=hourly_rate, 
            tutor_id=current_user.id
        )
        db.session.add(new_course)
        db.session.commit()
        
        return redirect(url_for('dashboard'))

    # If it's a GET request (just loading the page), fetch all subjects for the dropdown
    subjects = Subject.query.all()
    return render_template('create_course.html', subjects=subjects)

@app.route('/explore')
def explore():
    # Fetch all active courses from the database
    courses = Course.query.filter_by(is_active=True).all()
    return render_template('explore.html', courses=courses)

@app.route('/book/<int:course_id>', methods=['GET', 'POST'])
@login_required
def book_course(course_id):
    if current_user.role != 'student':
        return "Only students can book courses. <a href='/dashboard'>Go back</a>"
        
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        schedule_str = request.form.get('schedule_date')
        # Convert the HTML datetime string into a Python datetime object
        schedule_date = datetime.strptime(schedule_str, '%Y-%m-%dT%H:%M')
        
        new_booking = Booking(student_id=current_user.id, course_id=course.id, schedule_date=schedule_date)
        db.session.add(new_booking)
        db.session.commit()
        
        # Send them to the dummy payment screen
        return redirect(url_for('gcash_checkout', booking_id=new_booking.id))
        
    return render_template('book.html', course=course)

@app.route('/gcash-checkout/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def gcash_checkout(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if request.method == 'POST':
        # Simulate a successful payment
        booking.payment_status = 'Paid'
        booking.status = 'Confirmed'
        db.session.commit()
        return redirect(url_for('dashboard'))
        
    return render_template('gcash.html', booking=booking)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Access Denied: Admin only."
        
    all_users = User.query.all()
    all_bookings = Booking.query.all()
    return render_template('admin.html', users=all_users, bookings=all_bookings)

# Automatically create database tables and seed subjects on startup
with app.app_context():
    db.create_all()

    from werkzeug.security import generate_password_hash # Add this at the very top of your file if you don't have it

# ... (your other code) ...

# Automatically create database tables, an admin, and seed subjects
with app.app_context():
    db.create_all()
    
    # 1. Create a Master Admin account if it doesn't exist
    if not User.query.filter_by(email='admin@ctrlteach.com').first():
        master_admin = User(
            name='System Admin',
            email='admin@ctrlteach.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(master_admin)
        db.session.commit()
    
    # 2. Seed Subjects if empty
    if not Subject.query.first():
        new_subjects = [
            # ... (Keep your existing subject list here) ...
        ]
        db.session.add_all(new_subjects)
        db.session.commit()
    
    # If the Subject table is empty, seed it with our list
    if not Subject.query.first():
        new_subjects = [
            Subject(name='Japanese', category='Foreign Language'),
            Subject(name='Filipino', category='Foreign Language'),
            Subject(name='German', category='Foreign Language'),
            Subject(name='Spanish', category='Foreign Language'),
            Subject(name='Welsh', category='Foreign Language'),
            Subject(name='Calculus', category='Math'),
            Subject(name='Algebra', category='Math'),
            Subject(name='Physics', category='Science'),
            Subject(name='Biology', category='Science'),
            Subject(name='English Literature', category='English'),
            Subject(name='World History', category='Social Studies'),
            Subject(name='Microcontroller Robotics', category='Engineering'),
            Subject(name='Verilog Digital Logic', category='Computer Science'),
            Subject(name='C++ Programming', category='Computer Science')
        ]
        db.session.add_all(new_subjects)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)