import uuid

import requests
from config.config import Config
from flask import render_template, redirect, url_for, flash, request, Blueprint, abort, current_app, session, jsonify
from flask_login import current_user, login_user, login_required, logout_user
import random
from Services import data_services
from forms import RegisterForm, VerifyForm, LoginForm
from models.database import db, User
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from Services.user_services import Admin
from urllib.parse import quote
controller = Blueprint("controller", __name__)



@controller.route("/checkhealth")
def check():
    return "OK", 200

# @controller.route("/mail")
# def mail_test():
#
#     try:
#         msg = Message(
#             subject="SMTP Test",
#             recipients=[current_app.config['MAIL_USERNAME']],  # send to yourself
#
#         )
#         msg.body = "If you see this, your email client does not support HTML."
#
#         # Render HTML template (put your template inside templates/ folder)
#         msg.html = render_template("registration_email.html")
#
#         mail.send(msg)
#         return "Email sent ✅"
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return f"Email failed ❌: {e}", 500

@controller.route("/")
def home():
    all_courses = data_services.courses
    faq_data = data_services.information
    featured = random.sample(all_courses, min(6, len(all_courses)))
    return render_template("index.html",faq_data=faq_data,featured=featured)

@controller.route("/courses")
def courses():

    all_courses = data_services.courses

    featured = random.sample(all_courses, min(8, len(all_courses)))


    tech = []
    marketing = []
    design = [ ]
    writing = []
    for course in all_courses:
        if course["cat"] == 'tech':
            tech.append(course)
        elif course["cat"] == 'marketing':
            marketing.append(course)
        elif course["cat"] == 'design':
            design.append(course)
        elif course["cat"] == 'writing':
            writing.append(course)

    return render_template("courses.html",tech=tech,marketing=marketing,design=design,writing=writing,featured=featured)

@controller.route("/courses/<slug>")
def course_details(slug):
    courses = data_services.courses
    course = None
    for c in courses:
        if c["slug"] == slug:
            course = c
            break
    if not course:
        abort(404)
    return render_template("course-details.html", course=course )

def send_registration_email(user, course):
    subject = "Course Enrollment!!!"
    to_email = user.email
    pay_link = url_for("controller.make_payment", slug=course["slug"],email=user.email, _external=True)
    message = Mail(
        from_email=(Config.FROM_EMAIL, "THE TECH POWA"),
        to_emails=to_email,
        subject=subject,
        plain_text_content=f"Hi {user.fullname}, Welcome to THE TECH POWA!!!",
        html_content=render_template("registration_email.html", user=user,pay_link=pay_link, course=course)
    )

    try:
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)
        if response.status_code == 202:
            return "Email sent ✅"
        else:
            print(f"SendGrid error: {response.status_code} {response.body.decode()}")
            return f"Email failed ❌: {response.status_code}", 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Email failed ❌: {e}", 500


@controller.route("/register",methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if request.method == 'POST' and register_form.validate_on_submit():

        fullname = register_form.fullname.data
        email = register_form.email.data
        phone = register_form.phone.data
        selected_course = register_form.select_course.data

        course = next((c for c in data_services.courses if c["slug"] == selected_course), None)
        if not course:
            flash("Course not found.", "error")
            return redirect(url_for("controller.register"))
        funnel = register_form.funnel.data
        gender = register_form.gender.data
        check_box = register_form.check_box.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please use another email.','danger')
            return redirect(url_for('controller.register'))
        if not check_box:
            flash('Agree to our privacy policy','danger')
            return redirect(url_for('controller.register'))
        # Create new user
        new_user = User(fullname=fullname,email=email, phone=phone,course=selected_course,funnel=funnel,gender=gender)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Error saving user: ' + str(e), 'danger')
            return redirect(url_for('controller.register'))

        try:
            send_registration_email(user=new_user, course=course)
            print("mail successfully sent")
        except Exception as e:
            print(f"Error sending mail: {e}")
            flash('Account created, but email failed to send.', 'warning')
        print("Account created successfully")
        flash('Account Created successfully!!!', 'success')

        return render_template('success.html', user=new_user, course=course)
    return render_template("register.html",register_form= register_form)

@controller.route("/about_powa")
def about_powa():
    team = data_services.team
    return render_template("about.html", team=team)



@controller.route("/services")
def services():
    faq_data = data_services.information
    return render_template("our-services.html",faq_data=faq_data)

@controller.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        print('already authenticated')
        return redirect(url_for("controller.admin_dashboard"))
    login_form = LoginForm()
    if request.method == "POST" and login_form.validate_on_submit():
        admin_email = login_form.email.data
        admin_password = login_form.password.data

        env_email =current_app.config['ADMIN_EMAIL']
        env_password =current_app.config['ADMIN_PASSWORD']

        if admin_email == env_email and admin_password == env_password:
            admin = Admin(admin_id=1, admin_email=admin_email)
            login_user(admin, remember=True)
            session.permanent = True
            flash("Logged in successfully")
            next_page = request.args.get('next')
            return redirect(next_page or url_for("controller.admin_dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", login_form=login_form)


@controller.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

@controller.route("/terms")
def terms():
    return render_template('terms.html')

@controller.route("/privacy_policy")
def privacy_policy():
    return render_template('privacy.html')


@controller.route("/hq")
@login_required
def admin_dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = 20  # 20 students per page
    students = User.query.paginate(page=page, per_page=per_page)
    total_no_of_students = User.query.count()
    return render_template("admin.html", total=total_no_of_students, students=students)

@controller.route("/contact")
def contact_us():
    return render_template("contact-us.html")

@controller.route("/pay-link/<slug>/<email>")
def generate_pay_link(slug, email):
    # this is NOT the paystack initialization
    # this simply returns the URL to start payment
    return redirect (url_for("controller.make_payment", slug=slug, email=email, _external=True))

@controller.route("/start-payment/<slug>/<email>")
def make_payment(slug,email):

    if not email:
        return "Email is required", 400

    # Find course using your existing method
    courses = data_services.courses
    course = None
    for c in courses:
        if c["slug"] == slug:
            course = c
            break

    if not course:
        abort(404)

    amount = int(course["full_price"].replace(",", "").replace(" ", "")) * 100
    if not amount:
        return "Amount required"

    reference = str(uuid.uuid4())
    headers = {
        "Authorization": f"Bearer {Config.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": email,
        "amount": amount,
        "reference": reference,
        "callback_url": url_for("controller.verify_payment", slug=slug, _external=True)
    }
    try:
         response = requests.post("https://api.paystack.co/transaction/initialize",json=data,headers=headers)
         response.raise_for_status()
         paystack_response = response.json()

         if paystack_response['status']:
             return redirect(paystack_response['data']['authorization_url'])
         else:
             return jsonify({"message": paystack_response['message']}), 400
    except requests.exceptions.RequestException as e:
         return jsonify({"message": f"Error initializing payment: {e}"}), 500


@controller.route("/verify/<slug>")
def verify_payment(slug):
    reference = request.args.get("reference")
    if not reference:
        return jsonify({"message": "Payment reference missing"}), 400

    headers = {
        "Authorization": f"Bearer {Config.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    # Verify transaction
    try:
        response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
        response.raise_for_status()
        paystack_response = response.json()

        if paystack_response['status'] and paystack_response['data']['status'] == 'success':
            courses = data_services.courses
            course = next((c for c in courses if c["slug"] == slug), None)

            if not course:
                abort(404)

            # Build WhatsApp redirect
            message = f"Hello! I just made payment for the {course['title']} class. My name is ..."
            encoded_message = quote(message)

            whatsapp_url = f"https://wa.me/2348141713547?text={encoded_message}"

            return redirect(whatsapp_url)

        else:
            # Payment failed or not successful
            return jsonify({"message": "Payment verification failed", "data": paystack_response['data']}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Error verifying payment: {e}"}), 500

    # Payment was successful
    # Find the course again (same technique)


@controller.route("/verify")
def verify():
    # verify_form = VerifyForm()
    #
    # if request.method == "POST" and verify_form.validate_on_submit():
    #     if request.method == "POST" and verify_form.validate_on_submit():
    #         user = current_user  # Use the currently logged-in user
    #         if not user.is_verified:
    #             # Added verification logic here (e.g., OTP match or email code)
    #             user.is_verified = True
    #             db.session.commit()
    #             flash("Your account has been verified!", "success")
    #             return redirect(url_for('controller.dashboard'))  # Redirect to a relevant page
    #         else:
    #             flash("Account is already verified.", "info")
    user=""
    course=""
    return render_template("success.html",user=user, course=course)
#






