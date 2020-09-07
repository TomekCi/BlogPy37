from app import app, login_manager
import flask_login
from flask import render_template, request, redirect
from flask_login import login_user, login_required, logout_user
from models import db, Users, Posts, Roles
from wtforms import Form, StringField, PasswordField, validators


@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)


@app.before_first_request
def create_roles():
    roles = ['Admin', 'Standard', 'Author']
    all_roles = Roles.query.order_by(Roles.name).all()
    if not all_roles:
        for role in roles:
            new_post = Roles(name=role)
            db.session.add(new_post)
            db.session.commit()


    '''    for role in roles:
            if
            new_post = Role(name=role)
            db.session.add(new_post)
            db.session.commit()
'''

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
        db_query_one_user = Users.query.filter_by(username=form.username.data).first()
        # db_query_one_user_email = User.query.filter_by(email=form.username.data).first()
        if db_query_one_user is not None and db_query_one_user.verify_password(form.password.data):
            login_user(db_query_one_user)

            return redirect('/profile/' + str(db_query_one_user.id))
    return render_template('login.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile/<id>')
def profile(id):
    if str(flask_login.current_user.id) == id:
        db_query_one_user = Users.query.filter_by(id=id).first()
        return render_template('profile.html', db_query_one_user=db_query_one_user)
    #else:
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = Users(username=form.username.data, email=form.email.data,
                        password_hash=Users.hash_password(form.password.data))

        db.session.add(new_user)
        db.session.commit()
        return redirect('/register')
    return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/roles', methods=['GET', 'POST'])
@login_required
def roles_manager():
    all_roles = Roles.query.order_by(Roles.name).all()
    if request.method == 'POST':
        # roles = ['Admin', 'Standard', 'Author']
        for role in all_roles:
            new_post = Roles(name=role.name)
            db.session.add(new_post)
            db.session.commit()

        return redirect('/roles')
    elif request.method == 'GET':
        return render_template('admin/roles_manager.html', roles=all_roles)


@app.route('/roles/delete/<int:id>')
@login_required
def delete_role(id):
    role = Roles.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return redirect('/roles')


@app.route('/users', methods=['GET'])
@login_required
def users_manager():
    user_db_query_all = Users.query.order_by(Users.username).all()
    role_db_query_all = Roles.query.order_by(Roles.name).all()
    #userroles_db_query_all = UserRoles.query.order_by(UserRoles.user_id).all()
    return render_template('admin/users_manager.html', users=user_db_query_all,
                           roles=role_db_query_all)



@app.route('/users/add_role/<user>/<role>')
def add_userroles(user, role):
    role_query_one = Users.query.get(role)
    role_query_one.role_assignations.append(Users.query.get(user))
    db.session.commit()
    return redirect('/users')

'''
@app.route('/users/delete_role/<user>')
def delete_userroles(user):
    delete_user_role = UserRoles.query.get_or_404(user)
    db.session.delete(delete_user_role)
    db.session.commit()
    return redirect('/users')
'''


@app.route('/users/delete/<int:id>')
@login_required
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = Posts(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    elif request.method == 'GET':
        all_posts = Posts.query.order_by(Posts.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/delete/<int:id>')
@login_required
def delete(id):
    post = Posts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):

    post = Posts.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


@app.route('/posts/new', methods=['GET'])
@login_required
def new_posts():
    return render_template('new_post.html')


if __name__ == '__main__':
    app.run()
