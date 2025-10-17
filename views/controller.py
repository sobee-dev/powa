
import requests
from config.config import Config
from flask import render_template, redirect, url_for, flash, request, Blueprint, abort, current_app, session
from flask_login import current_user, login_user, login_required, logout_user

from Services import data_services
from forms import RegisterForm, VerifyForm, LoginForm
from models.database import db, User
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from Services.user_services import Admin
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
    faq_data = data_services.information
    return render_template("index.html",courses= data_services.courses,faq_data=faq_data)

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

    message = Mail(
        from_email=(Config.FROM_EMAIL, "THE TECH POWA"),
        to_emails=to_email,
        subject=subject,
        plain_text_content=f"Hi {user.fullname}, Welcome to THE TECH POWA!!!",
        html_content=render_template("registration_email.html", user=user, course=course)
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

    return render_template("about.html")



@controller.route("/agency")
def agency():

    return render_template("agency.html")

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


@controller.route("/hq")
@login_required
def admin_dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = 20  # 20 students per page
    students = User.query.paginate(page=page, per_page=per_page)
    total_no_of_students = User.query.count()
    return render_template("admin.html", total=total_no_of_students, students=students)


@controller.route("/verify-email")
def verify():
    verify_form = VerifyForm()

    if request.method == "POST" and verify_form.validate_on_submit():
        if request.method == "POST" and verify_form.validate_on_submit():
            user = current_user  # Use the currently logged-in user
            if not user.is_verified:
                # Added verification logic here (e.g., OTP match or email code)
                user.is_verified = True
                db.session.commit()
                flash("Your account has been verified!", "success")
                return redirect(url_for('controller.dashboard'))  # Redirect to a relevant page
            else:
                flash("Account is already verified.", "info")

    return render_template("verify.html", form=verify_form)







