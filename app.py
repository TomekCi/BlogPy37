from flask import Flask, render_template, request, redirect, flash, url_for, session, logging
from flask_security import login_required, SQLAlchemyUserDatastore, Security
from models import db, User, Role
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
app.config['SECRET_KEY'] = 'secret'
app.config['SECURITY_PASSWORD_SALT'] = 'secrethash'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True
# login_manager = LoginManager()
db.init_app(app)
# login_manager.init_app(app)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class RegisterForm(Form):
    # username = StringField('User name', [validators.Length(min=5, max=30)])
    email = StringField('E-mail address', [validators.Length(min=5, max=30)])
    password = PasswordField('Password', [
        validators.Length(min=5, max=15),
        validators.EqualTo('confirm', message='Passwords do not mach')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/profile/<id>')
@login_required
def profile(id):
    db_query_one_user = User.query.filter_by(id=id).first()

    return render_template('/profile.html', db_query_one_user=db_query_one_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # user = form.username.data
        email = form.email.data
        password = form.password.data
        # passwordhash = User.set_password(form.password.data)

        new_user = User(email=email, password=password, active=True)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login1')
    return render_template('register.html', form=form)


@app.route("/")
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
