from flask import Flask, render_template, request, redirect, session, g
from flask_login import LoginManager
from models import db, Post, User


users = []
users.append(User(id=1, username='Tom', password='dupa1'))
users.append(User(id=2, username='Gos', password='dupa2'))

app = Flask(__name__)
app.secret_key ='secretkey'


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


@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
    else:
        g.user = None


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        try:
            user = [x for x in users if x.username == username][0]
        except Exception:
            return redirect('/login')

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect('/profile')

        return redirect('/login')

    return render_template('login.html')


@app.route("/profile")
def profile():
    if not g.user:
        return redirect('/login')

    return render_template('profile.html')


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
        new_post = Post(title = post_title, content = post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    elif request.method == 'GET':
        all_posts = Post.query.order_by(Post.date_posted).all()
        return render_template('new_post.html', posts=all_posts)


if __name__ == '__main__':
    app.run()
