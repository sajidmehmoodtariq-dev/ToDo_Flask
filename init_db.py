#!/usr/bin/env python3
"""
Database initialization script for Todo Flask App
This script creates all database tables with the correct schema
"""

from app import app, db

def init_database():
    """Initialize the database with all tables"""
    with app.app_context():
        # Drop all existing tables (if any)
        db.drop_all()
        print("🗑️  Dropped existing tables")
        
        # Create all tables with new schema
        db.create_all()
        print("✅ Created all tables with new schema")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"📊 Tables created: {tables}")
        
        # Check User table columns
        if 'user' in tables:
            user_columns = [col['name'] for col in inspector.get_columns('user')]
            print(f"👤 User table columns: {user_columns}")
        
        # Check Todo table columns
        if 'todo' in tables:
            todo_columns = [col['name'] for col in inspector.get_columns('todo')]
            print(f"📝 Todo table columns: {todo_columns}")
        
        print("🎉 Database initialization complete!")

if __name__ == '__main__':
    init_database()
