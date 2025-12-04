from flask import (
    Flask, render_template, redirect, url_for,
    flash, request, session, make_response
)
from auth import auth_bp, token_required
from bson.objectid import ObjectId
from datetime import datetime

from mongodb_creation import (
    get_user_collection,
    get_course_collection,
    get_subscription_collection
)
import os

SESSION_KEY = os.environ["SESSION_KEY"]

app = Flask(__name__)

app.secret_key = SESSION_KEY

app.register_blueprint(auth_bp)


# ---------------------- LOGIN ROUTE---------------------- RENDERS LOGIN PAGE
@app.route("/")
@app.route("/login")
def login_page():
    return render_template("loginpage.html")


# ---------------------- HOME ROUTE ----------------------- IT WILL SHOW ALL COURSES
@app.route("/home")
@token_required
def home_page(user_data):
    courses_col = get_course_collection()
    courses = list(courses_col.find(
        {}, {"_id": 1, "title": 1, "description": 1, "price": 1, "image": 1}
    ))

    for c in courses:
        c["_id"] = str(c["_id"])

    return render_template("homepage.html", courses=courses)


# ---------------------- COURSE DETAILS ---------------------- SHOWS DETAILS OF A PARTICULAR COURSE
@app.route("/course_details/<course_id>")
@token_required
def course_details(user_data, course_id):

    courses_col = get_course_collection()
    users_col = get_user_collection()
    subs_col = get_subscription_collection()

    subscribedUser = False
    user_email = user_data.get("email")

    if user_email:
        user = users_col.find_one({"email": user_email})
        if user:
            user_id = str(user["_id"])
            subscription = subs_col.find_one({
                "userId": user_id,
                "courseId": course_id
            })
            if subscription:
                subscribedUser = True

    course = courses_col.find_one({"_id": ObjectId(course_id)})
    if not course:
        return "Course not found", 404

    course["_id"] = str(course["_id"])
    return render_template("coursepage.html", course=course, subscribedUser=subscribedUser)


# ---------------------- SUBSCRIBE PAGE ---------------------- SHOWS SUBSCRIPTION OPTIONS WHEN USER GOING TO ENROLL FREE/PAID COURSE
@app.route("/subscribe/<course_id>")
@token_required
def subscribe(user_data, course_id):

    courses_col = get_course_collection()
    users_col = get_user_collection()
    subs_col = get_subscription_collection()

    try:
        course_obj_id = ObjectId(course_id)
    except:
        flash("Invalid course ID!")
        return redirect(url_for("home_page"))

    course = courses_col.find_one({"_id": course_obj_id})
    if not course:
        flash("Course not found!")
        return redirect(url_for("home_page"))

    course["_id"] = str(course["_id"])

    user_email = user_data["email"]
    user = users_col.find_one({"email": user_email})
    if not user:
        flash("User not found in database!")
        return redirect(url_for("home_page"))

    user_id = str(user["_id"])

    is_enrolled = subs_col.find_one({"userId": user_id, "courseId": course["_id"]})
    already_enrolled = True if is_enrolled else False

    return render_template(
        "subscription.html",
        course=course,
        promo_applied=False,
        already_enrolled=already_enrolled
    )


# ---------------------- ENROLL FREE COURSE ---------------------- ENROLLS USER IN A FREE COURSE
@app.route("/enroll/<course_id>")
@token_required
def enroll_course(user_data, course_id):

    courses_col = get_course_collection()
    users_col = get_user_collection()
    subs_col = get_subscription_collection()

    try:
        course_obj_id = ObjectId(course_id)
    except:
        flash("Invalid course ID!")
        return redirect(url_for("home_page"))

    user_email = user_data["email"]
    user = users_col.find_one({"email": user_email})
    if not user:
        flash("User not found!")
        return redirect(url_for("home_page"))

    user_id = str(user["_id"])

    course = courses_col.find_one({"_id": course_obj_id})
    if not course:
        flash("Course not found!")
        return redirect(url_for("home_page"))

    if course["price"] != 0:
        flash("This is a paid course. Go through Subscribe.")
        return redirect(url_for("subscribe", course_id=course_id))

    existing = subs_col.find_one({"userId": user_id, "courseId": course_id})
    if existing:
        flash("Already enrolled in this free course!")
        return redirect(url_for("mycourses_page"))

    subscription_doc = {
        "userId": user_id,
        "courseId": course_id,
        "pricePaid": 0,
        "subscribedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    subs_col.insert_one(subscription_doc)

    flash(f'Successfully enrolled in "{course["title"]}" for FREE!')
    return redirect(url_for("mycourses_page"))


# ---------------------- BUY / PAID SUBSCRIPTION ---------------------- ENROLLS USER IN A PAID COURSE
@app.route("/buy/<course_id>", methods=["GET", "POST"])
@token_required
def buy_course(user_data, course_id):

    courses_col = get_course_collection()
    users_col = get_user_collection()
    subs_col = get_subscription_collection()

    try:
        course_obj_id = ObjectId(course_id)
    except:
        flash("Invalid course ID!")
        return redirect(url_for("home_page"))

    course = courses_col.find_one({"_id": course_obj_id})
    if not course:
        flash("Course not found!")
        return redirect(url_for("home_page"))

    user_email = user_data["email"]
    user = users_col.find_one({"email": user_email})

    if not user:
        flash("User not found in database!")
        return redirect(url_for("home_page"))

    user_id = str(user["_id"])

    exists = subs_col.count_documents({"userId": user_id, "courseId": course_id})
    if exists > 0:
        flash("You have already subscribed to this course!")
        return redirect(url_for("subscribe", course_id=course_id))

    promo_code = request.form.get("promo_code", "").strip().upper()
    original_price = course["price"]
    final_price = original_price

    if promo_code == "BFSALE25":
        final_price = int(original_price * 0.5)
        flash(f"Promo applied! Subscribed for ₹{final_price} (50% OFF).")
    else:
        flash(f"Subscribed for ₹{original_price}.")

    subscription_doc = {
        "userId": user_id,
        "courseId": course_id,
        "pricePaid": final_price,
        "subscribedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    subs_col.insert_one(subscription_doc)

    return redirect(url_for("mycourses_page"))


# ---------------------- MY COURSES ---------------------- SHOWS ALL COURSES USER IS ENROLLED IN
@app.route("/mycourse")
@token_required
def mycourses_page(user_data):

    email = user_data.get("email")
    if not email:
        return "Invalid user token - Email missing", 400

    users_col = get_user_collection()
    subs_col = get_subscription_collection()
    courses_col = get_course_collection()

    user = users_col.find_one({"email": email})
    if not user:
        return "User not found", 404

    user_id = str(user["_id"])
    subscriptions = list(subs_col.find({"userId": user_id}))

    if len(subscriptions) == 0:
        return render_template("mycourse.html",
                               courses=[],
                               message="You are not enrolled in any course. Enroll now to start learning!")

    course_ids = [ObjectId(sub["courseId"]) for sub in subscriptions]
    enrolled_courses = list(courses_col.find(
        {"_id": {"$in": course_ids}},
        {"title": 1, "description": 1, "price": 1, "image": 1}
    ))

    for c in enrolled_courses:
        c["_id"] = str(c["_id"])

    return render_template("mycourse.html", courses=enrolled_courses, message=None)


# ---------------------- LOGOUT ---------------------- LOGS OUT THE USER BY CLEARING SESSION AND COOKIES(JWT TOKEN)
@app.route("/logout")
@token_required
def logout_user(user_data):

    session.clear()
    resp = make_response(redirect(url_for("login_page")))
    resp.set_cookie("jwt_token", "", expires=0)
    resp.set_cookie("session", "", expires=0)
    return resp


if __name__ == "__main__":
    app.run(debug=True)
