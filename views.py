from app import db, app, login_manager
from flask import render_template, request, redirect
from flask_login import login_user, login_required, logout_user
from models import User
from wtforms import Form, StringField, PasswordField, validators


class RegisterForm(Form):
    username = StringField('username', [validators.Length(min=5, max=30)])
    email = StringField('email', [validators.Length(min=5, max=30)])
    password = PasswordField('password', [
        validators.Length(min=5, max=15),
        validators.EqualTo('confirm', message='Passwords do not mach')
    ])
    confirm = PasswordField('Confirm Password')


class LoginForm(Form):
    username = StringField('username', [validators.Length(min=5, max=30)])
    password = StringField('password', [validators.Length(min=5, max=30)])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        db_query_one_user = User.query.filter_by(username=form.username.data).first()
        print(db_query_one_user.verify_password(form.password.data))
        if db_query_one_user is not None and db_query_one_user.verify_password(form.password.data):
            login_user(db_query_one_user)

            return redirect('/profile/' + str(db_query_one_user.id))
    return render_template('login.html')


@app.route('/profile/<id>')
@login_required
def profile(id):
    db_query_one_user = User.query.filter_by(id=id).first()

    return render_template('profile.html', db_query_one_user=db_query_one_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(username=form.username.data, email=form.email.data,
                        password_hash=User.hash_password(form.password.data))

        db.session.add(new_user)
        db.session.commit()
        return redirect('/register')
    return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route("/")
def main():
    print(app.config)
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
