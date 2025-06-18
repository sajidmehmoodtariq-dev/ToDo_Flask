from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database configuration
# For Railway (production) or local development
if os.environ.get('DATABASE_URL'):
    # Railway PostgreSQL URL - Handle postgres:// to postgresql:// conversion for Vercel
    database_url = os.environ.get('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local SQLite for development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/todo.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access your todos.'
login_manager.login_message_category = 'info'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with todos
    todos = db.relationship('Todo', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Todo Model (updated with user relationship)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to link todos to users
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.title}>'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        if not username or not password:
            flash('Username and password are required!', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=bool(remember))
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))

# Main Routes (updated with authentication)
@app.route('/')
@login_required
def index():
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos, user=current_user)

@app.route('/add', methods=['POST'])
@login_required
def add_todo():
    title = request.form.get('title')
    description = request.form.get('description', '')
    
    if not title:
        flash('Title is required!', 'error')
        return redirect(url_for('index'))
    
    todo = Todo(title=title, description=description, user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
    flash('Todo added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
@login_required
def complete_todo(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    todo.completed = not todo.completed
    todo.updated_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required
def delete_todo(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_todo(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        todo.title = request.form.get('title')
        todo.description = request.form.get('description', '')
        todo.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Todo updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', todo=todo)

# API Routes (updated with authentication)
@app.route('/api/todos')
@login_required
def api_todos():
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.created_at.desc()).all()
    return jsonify([{
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat(),
        'updated_at': todo.updated_at.isoformat()
    } for todo in todos])

# Profile route
@app.route('/profile')
@login_required
def profile():
    user_todos = Todo.query.filter_by(user_id=current_user.id).all()
    stats = {
        'total_todos': len(user_todos),
        'completed_todos': len([t for t in user_todos if t.completed]),
        'pending_todos': len([t for t in user_todos if not t.completed]),
        'join_date': current_user.created_at.strftime('%B %d, %Y')
    }
    return render_template('profile.html', user=current_user, stats=stats)

# Health check route for Vercel
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

# Route to initialize database tables (for production deployment)
@app.route('/init-db')
def init_db():
    """Initialize database tables - call this once after deployment"""
    try:
        with app.app_context():
            db.create_all()
        return jsonify({"message": "Database tables created successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Error handlers for better production experience
@app.errorhandler(404)
def not_found(error):
    return render_template('base.html', 
                         title='Page Not Found',
                         content='<h2>404 - Page Not Found</h2><p>The page you are looking for does not exist.</p>'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html',
                         title='Server Error', 
                         content='<h2>500 - Internal Server Error</h2><p>Something went wrong on our end.</p>'), 500

# Create tables only in development/local environment
# Skip table creation in serverless environments like Vercel
if not os.environ.get('DATABASE_URL') and not os.environ.get('VERCEL'):
    with app.app_context():
        db.create_all()

# Vercel serverless function handler
app = app

if __name__ == '__main__':
    # Only run in debug mode for local development
    app.run(debug=os.environ.get('FLASK_ENV') == 'development')
