from flask import Blueprint, render_template, request, redirect, session
from models import db, User

auth = Blueprint('auth', __name__)


# ==========================
# Home Page
# ==========================

@auth.route('/')
def home():
    return render_template('index.html')


# ==========================
# Register
# ==========================

@auth.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            role=request.form['role']
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


# ==========================
# Login
# ==========================

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:

            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role

            # Role Based Dashboard
            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template('login.html')


# ==========================
# Logout
# ==========================

@auth.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


# ==========================
# View Users
# ==========================

@auth.route('/users')
def users():

    if 'user_id' not in session:
        return redirect('/login')

    if session['user_role'] != "Admin":
        return "Access Denied"

    all_users = User.query.all()

    return render_template(
        'users.html',
        users=all_users
    )


# ==========================
# Edit User
# ==========================

@auth.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):

    if 'user_id' not in session:
        return redirect('/login')

    if session['user_role'] != "Admin":
        return "Access Denied"

    user = User.query.get_or_404(id)

    if request.method == 'POST':

        user.name = request.form['name']
        user.email = request.form['email']
        user.role = request.form['role']

        db.session.commit()

        return redirect('/users')

    return render_template(
        'edit_user.html',
        user=user
    )


# ==========================
# Delete User
# ==========================

@auth.route('/delete_user/<int:id>')
def delete_user(id):

    if 'user_id' not in session:
        return redirect('/login')

    if session['user_role'] != "Admin":
        return "Access Denied"

    # Prevent Admin from deleting own account
    if id == session['user_id']:
        return "You cannot delete your own account."

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')