# Course Management Platform

A Flask-based web application for managing and enrolling in online courses. Users can browse courses, enroll in free courses, or purchase paid courses with promo code support.

## Features

- **User Authentication**: Secure signup and login with JWT token-based authentication
- **Course Browsing**: View all available courses with details
- **Course Enrollment**: Enroll in free courses or purchase paid courses
- **My Courses**: Track all enrolled courses in one place
- **Promo Codes**: Apply discount codes (e.g., BFSALE25 for 50% off)
- **MongoDB Integration**: Persistent data storage for users, courses, and subscriptions

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: HTML, CSS, JavaScript

## Prerequisites

- Python 3.7+
- MongoDB (local or cloud instance)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lokesh-2310/Task-assignment-cwl.git
   cd task-assignment
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create an `envfile.py` file in the root directory with the following variables:
   ```python
   MONGO_DB_STRING = "your_mongodb_connection_string"
   DATABASE_NAME = "your_database_name"
   SECRET_KEY = "your_jwt_secret_key"
   SESSION_KEY = "your_flask_session_key"
   ```

4. **Initialize database**
   
   Run the MongoDB initialization script to create collections and insert dummy data:
   ```bash
   python mongodb_creation.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:5000`

## Project Structure

```
task-assignment/
├── app.py                 # Main Flask application
├── auth.py                # Authentication routes (signup/login)
├── jwtutils.py            # JWT token creation and verification
├── mongodb_creation.py     # Database initialization and dummy data
├── requirements.txt       # Python dependencies
├── envfile.py            # Environment variables (create this)
├── templates/            # HTML templates
│   ├── loginpage.html
│   ├── homepage.html
│   ├── coursepage.html
│   ├── mycourse.html
│   └── subscription.html
└── static/               # Static files
    ├── css_folder/       # Stylesheets
    ├── js_folder/        # JavaScript files
    └── images/           # Course images
```

## API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login

### Course Management
- `GET /` or `GET /login` - Login page
- `GET /home` - Browse all courses (requires authentication)
- `GET /course_details/<course_id>` - View course details
- `GET /subscribe/<course_id>` - Subscription page
- `GET /enroll/<course_id>` - Enroll in free course
- `POST /buy/<course_id>` - Purchase paid course
- `GET /mycourse` - View enrolled courses
- `GET /logout` - Logout user

## Usage

1. **Sign Up**: Create a new account via the signup API endpoint
2. **Login**: Authenticate to receive a JWT token
3. **Browse Courses**: View all available courses on the home page
4. **Enroll**: Click on a course to view details and enroll
5. **My Courses**: Access all your enrolled courses from the "My Courses" page

## Promo Code

Use the promo code `BFSALE25` during checkout to get 50% off on paid courses.

## Dependencies

- `flask` - Web framework
- `pymongo` - MongoDB driver
- `PyJWT` - JWT token handling
- `requests` - HTTP library
- `werkzeug` - Password hashing utilities

## Notes

- The application uses JWT tokens stored in cookies for authentication
- All protected routes require a valid JWT token
- Free courses can be enrolled directly, while paid courses require purchase
- Database initialization script should be run only once to avoid duplicate data


