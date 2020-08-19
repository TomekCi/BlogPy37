from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from models import db, User
from wtforms import Form, StringField, PasswordField, validators


login_manager = LoginManager()


app = Flask(__name__)
login_manager.init_app(app)


POSTGRES = {
    'user': 'postgres',
    'pw': 'dupa1',
    'db': 'flasklogin',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'itissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


db.init_app(app)


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
        username = form.username.data
        password = form.password.data

        db_query_one_user = User.query.filter_by(username=username).first()
        if db_query_one_user is not None and db_query_one_user.password == password:
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
        username = form.username.data
        email = form.email.data
        password = form.password.data

        new_user = User(username=username, email=email, password=password)
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
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == '__main__':
    app.run()
