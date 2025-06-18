from app import app

# This is the entry point for Vercel
# Vercel looks for this file structure: /api/index.py
# and expects a variable named 'app' or a function that returns the app

# Export the Flask application
def handler(event, context):
    return app(event, context)

# For direct import
application = app

if __name__ == "__main__":
    app.run()
