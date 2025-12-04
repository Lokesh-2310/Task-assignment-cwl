from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os

MONGO_DB_STRING = os.environ["MONGO_DB_STRING"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
# MONGODB CONNECTION
# DATABASE UTILITY FUNCTIONS

def initialize_db():
    client = MongoClient(MONGO_DB_STRING)
    db = client[DATABASE_NAME]
    return db


def get_user_collection():
    db = initialize_db()
    return db["users"]

def get_course_collection():
    db = initialize_db()
    return db["course_details"]

def get_subscription_collection():
    db = initialize_db()
    return db["subscriptions"]

def insert_dummy_users(users_col):
    
    dummy_users = [
        {"name": "John Doe", "email": "john@example.com", "password": generate_password_hash("pass123")},
        {"name": "Sara Smith", "email": "sara@example.com", "password": generate_password_hash("pass456")},
        {"name": "Lokesh Gupta", "email": "lokesh@gmail.com", "password": generate_password_hash("2310")},
    ]
    
    for user in dummy_users:
        user_doc = {
            "name": user["name"],
            "email": user["email"],
            "password": user["password"]
        }
        users_col.insert_one(user_doc)



# DUMMY DATA INSERT IN FIRST TIME ONLY - NO NEED TO EXECUTE AGAIN AND AGAIN
def insert_dummy_courses(courses_col):
    
    dummy_courses = [
    {
        "title": "Python",
        "description": "Learn Python from scratch.",
        "price": 0,
        "image": "python",

        "requirements": ["Laptop", "Internet Connection", "Basic Computer Knowledge"],
        "createdAt": "2025-09-01",
        "instructor": "Lokesh Gupta",
        "duration": "9 days",
        "level": "Beginner",

        "lessons": [
            "Introduction to Python",
            "Variables & Data Types",
            "Control Flow",
            "Functions",
            "Mini Projects"
        ],
        "rating": 4.8,
        "students_enrolled": 1280,
        "category": "Programming",
        "language": "English",
        "what_you_will_learn": [
            "Write Python scripts",
            "Understand data types & variables",
            "Solve programming challenges",
            "Build small beginner projects"
        ]
    },

    {
        "title": "Web Development",
        "description": "HTML, CSS, JS Full Guide.",
        "price": 499,
        "image": "webdev",

        "requirements": ["Laptop", "Internet Connection", "Basic Computer Knowledge"],
        "createdAt": "2025-08-15",
        "instructor": "Rio Smith",
        "duration": "15 days",
        "level": "Advance",

        "lessons": [
            "HTML Basics",
            "CSS Styling",
            "JavaScript Fundamentals",
            "Responsive Design",
            "Frontend Project"
        ],
        "rating": 4.6,
        "students_enrolled": 980,
        "category": "Frontend Development",
        "language": "English",
        "what_you_will_learn": [
            "Build modern websites",
            "Understand HTML/CSS/JS deeply",
            "Work with flexbox & grid",
            "Make interactive pages"
        ]
    },

    {
        "title": "Data Science",
        "description": "Data analysis & ML basics.",
        "price": 699,
        "image": "datascience",

        "requirements": ["Laptop", "Internet Connection", "Basic Computer Knowledge"],
        "createdAt": "2025-07-20",
        "instructor": "Mike Johnson",
        "duration": "20 days",
        "level": "Intermediate",

        "lessons": [
            "Data Analysis with Python",
            "NumPy & Pandas",
            "Data Cleaning",
            "Intro to Machine Learning",
            "ML Mini Project"
        ],
        "rating": 4.7,
        "students_enrolled": 720,
        "category": "Data Science",
        "language": "English",
        "what_you_will_learn": [
            "Analyze datasets using Python",
            "Clean & preprocess data",
            "Build basic ML models",
            "Work with Pandas & NumPy"
        ]
    },
    {
        "title": "Artificial Intelligence",
        "description": "Introduction to AI concepts, neural networks, and automation.",
        "price": 799,
        "image": "ai",

        "requirements": ["Laptop", "Internet Connection", "Basic Python Knowledge"],
        "createdAt": "2025-09-20",
        "instructor": "Sophia Williams",
        "duration": "18 days",
        "level": "Intermediate",

        "lessons": [
            "What is AI?",
            "Search Algorithms",
            "Neural Networks Basics",
            "AI Applications",
            "AI Mini Project"
        ],
        "rating": 4.9,
        "students_enrolled": 860,
        "category": "Artificial Intelligence",
        "language": "English",
        "what_you_will_learn": [
            "Understand AI fundamentals",
            "Learn about neural networks",
            "Explore automation & ML concepts",
            "Build simple AI-powered apps"
        ]
    },
    {
        "title": "Java Programming",
        "description": "Master Java from basics to OOP and project building.",
        "price": 599,
        "image": "java",

        "requirements": ["Laptop", "Internet Connection", "Basic Computer Knowledge"],
        "createdAt": "2025-10-05",
        "instructor": "Arjun Mehta",
        "duration": "12 days",
        "level": "Beginner",

        "lessons": [
            "Java Basics",
            "Variables & Data Types",
            "OOP Concepts",
            "Exception Handling",
            "Java Mini Project"
        ],
        "rating": 4.7,
        "students_enrolled": 1130,
        "category": "Programming",
        "language": "English",
        "what_you_will_learn": [
            "Understand Java fundamentals",
            "Write object-oriented programs",
            "Work with classes & objects",
            "Build Java applications"
        ]
    }
]

    
    for course in dummy_courses:
        course_doc = {
            "title": course["title"],
            "description": course["description"],
            "price": course["price"],
            "image": course["image"],
            "requirements": course.get("requirements", []),
            "createdAt": course.get("createdAt", None),
            "instructor": course.get("instructor", ""),
            "duration": course.get("duration", ""),
            "level": course.get("level", ""),
            "lessons": course.get("lessons", []),
            "rating": course.get("rating", 0),
            "students_enrolled": course.get("students_enrolled", 0),
            "category": course.get("category", ""),
            "language": course.get("language", "English"),
            "what_you_will_learn": course.get("what_you_will_learn", [])
        }

        courses_col.insert_one(course_doc)

if __name__ == "__main__":
    
    users_col = get_user_collection()
    courses_col = get_course_collection()
    
    insert_dummy_users(users_col)
    insert_dummy_courses(courses_col)
    print("\nMongoDB initialized successfully with:")

