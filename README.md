# 📝 Beautiful Todo List App with Authentication

A modern, responsive Todo List application built with Flask featuring **complete user authentication and authorization**. Designed for easy deployment on Vercel and Railway.

## ✨ Features

- **🔐 User Authentication** - Secure registration, login, and session management
- **👤 User Profiles** - Personal dashboards with productivity statistics
- **🔒 Private Todo Lists** - Each user has their own private todos
- **Beautiful Modern UI** - Clean, responsive design with gradient backgrounds
- **Full CRUD Operations** - Create, Read, Update, Delete todos
- **Task Management** - Mark tasks as complete/incomplete
- **Task Statistics** - View total, completed, and pending tasks
- **Timestamps** - Track creation and update times
- **Database Support** - SQLite for development, PostgreSQL for production
- **Easy Deployment** - Ready for Vercel (frontend) and Railway (database)
- **Security Features** - Password hashing, CSRF protection, user isolation

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ToDo_Flask
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Visit `http://localhost:5000` to see your Todo app!

## 🌐 Deployment Guide

### Step 1: Deploy Database on Railway

1. Go to [Railway.app](https://railway.app) and sign up/login
2. Click "New Project" → "Provision PostgreSQL"
3. Once created, go to your PostgreSQL service
4. In the "Variables" tab, copy the `DATABASE_URL`
5. Your database is ready!

### Step 2: Deploy App on Vercel

1. Push your code to GitHub
2. Go to [Vercel.com](https://vercel.com) and sign up/login
3. Click "New Project" and import your GitHub repository
4. In the deployment settings:
   - Framework Preset: Other
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: Leave empty
5. Add Environment Variables:
   - `DATABASE_URL`: The URL you copied from Railway
   - `SECRET_KEY`: A random secret key (generate one)
6. Deploy!

## 🛠️ Environment Variables

Create a `.env` file for local development (copy from `.env.example`):

```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

For production:
- **Vercel**: Add variables in Vercel dashboard
- **Railway**: DATABASE_URL is automatically provided

## 📁 Project Structure

```
ToDo_Flask/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel deployment config
├── runtime.txt        # Python version specification
├── templates/         # HTML templates
│   ├── base.html      # Base template with styling
│   ├── index.html     # Main todo list page
│   └── edit.html      # Edit todo page
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## 🎨 Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Font Awesome
- **Deployment**: Vercel (app), Railway (database)

## 🔧 API Endpoints

### Authentication Routes
- `GET /register` - User registration page
- `POST /register` - Create new user account
- `GET /login` - User login page
- `POST /login` - Authenticate user
- `GET /logout` - Logout current user

### Todo Management Routes (Authentication Required)
- `GET /` - Home page with user's todo list
- `POST /add` - Add new todo
- `GET /complete/<id>` - Toggle todo completion
- `GET /delete/<id>` - Delete todo
- `GET /edit/<id>` - Edit todo page
- `POST /edit/<id>` - Update todo
- `GET /profile` - User profile with statistics
- `GET /api/todos` - JSON API for user's todos

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Need Help?

If you encounter any issues:
1. Check the environment variables are set correctly
2. Ensure the database connection is working
3. Check the Vercel and Railway logs for errors
4. Make sure all dependencies are installed

Happy coding! 🎉