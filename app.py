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
db.init_app(app)


class RegisterForm(Form):
    userName = StringField('userName', [validators.Length(min=5, max=30)])
    email = StringField('emailAddress', [validators.Length(min=5, max=30)])
    password = PasswordField('passwordHash', [
        validators.Length(min=5, max=15),
        validators.EqualTo('confirm', message='Passwords do not mach')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.userName.data
        email = form.email.data
        password = form.password.data
        # passwordHash = User.set_password(form.password.data)

        new_user = User(username=user, emailaddress=email, passwordhash=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/register')
    return render_template('register.html', form=form)


@app.route("/articles")
def articles():
    return render_template('articles.html', articles = Articles)


@app.route("/article/<int:id>")
def article(id):
    return render_template('article.html', id = id, article = article)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = Post(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    elif request.method == 'GET':
        all_posts = Post.query.order_by(Post.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = Post(title = post_title, content = post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    elif request.method == 'GET':
        all_posts = Post.query.order_by(Post.date_posted).all()
        return render_template('new_post.html', posts=all_posts)


if __name__ == '__main__':
    app.run()
