
from flask import render_template, redirect, url_for, flash, session, request, Blueprint, abort, current_app
from flask_login import login_required, current_user, login_user

from forms import RegisterForm, VerifyForm, ProfileForm, LoginForm

from models.database import db, User, Admin
from Services import data_services
from flask_mail import Message
from extensions import mail



controller = Blueprint("controller", __name__)

@controller.route("/check")
def check():
    return data_services.courses

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

    return render_template("index.html",courses= data_services.courses)

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
    recipients = [user.email]

    try:
        msg = Message(subject=subject,recipients=recipients)

        msg.body = f"Hi {user.fullname}, your registration was received."
        msg.html = render_template("registration_email.html", user=user, course=course)
        mail.send(msg)
        return "Email sent ✅"
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
            print("User not added")
            return redirect(url_for('controller.register'))

        try:
            send_registration_email(user=new_user, course=course)
            print("mail successfully sent")
        except Exception as e:
            print(f"Error sending mail: {e}")
            flash('Account created, but email failed to send.', 'warning')
        print("Account created successfully")
        flash('Account Created successfully!!!', 'success')

        return "Application submitted successfully. Check your email for next step."
    return render_template("register.html",register_form= register_form)

@controller.route("/about_powa")
def about_powa():

    return render_template("about.html")



@controller.route("/agency")
def agency():

    return render_template("agency.html")

@controller.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        admin_email = login_form.email.data
        admin_password = login_form.password.data

        admin = Admin.query.filter_by(admin_email=admin_email).first()
        if admin and admin.check_password(admin_password):
            login_user(admin)
            return redirect(url_for("controller.admin_dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", login_form=login_form)


@controller.route("/hq")
# @login_required
def admin_dashboard():
    users_list = data_services.get_all_users()
    total_students = len(users_list)
    return render_template("admin.html",users_list=users_list, total=total_students)


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







