from flask import Flask, render_template, request, redirect, flash, url_for, session, logging
from flask_login import LoginManager
from models import db, Post, User
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators


app = Flask(__name__)

Articles = Articles()

POSTGRES = {
    'user': 'postgres',
    'pw': 'dupa1',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)


class RegisterForm(Form):
    username = StringField('User name', [validators.Length(min=5, max=30)])
    email = StringField('E-mail address', [validators.Length(min=5, max=30)])
    password = PasswordField('Password', [
        validators.Length(min=5, max=15),
        validators.EqualTo('confirm', message='Passwords do not mach')
    ])
    confirm = PasswordField('Confirm Password')


class LoginForm(Form):
    username = StringField('User name', [validators.Length(min=5, max=30)])
    password = PasswordField('Password', [validators.Length(min=5, max=15)])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/profile/<username>')
def profile(username):
    db_query_one_user = User.query.filter_by(username=username).first()

    return render_template('/profile.html', db_query_one_user=db_query_one_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.username.data
        password = form.password.data
        # passwordhash = User.check_password(form.password.data)

        db_query_one_user = User.query.filter_by(username=user).first()

        if db_query_one_user is not None and db_query_one_user.passwordhash == password:
            return redirect('/profile/' + user)

    return render_template('/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.username.data
        email = form.email.data
        password = form.password.data
        # passwordhash = User.set_password(form.password.data)

        new_user = User(username=user, emailaddress=email, passwordhash=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/register')
    return render_template('register.html', form=form)


@app.route("/")
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
