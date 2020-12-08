from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from flask_login import login_required, current_user
from flaskr.models import Post, db, PostComment, User
from flaskr import csrf

blog = Blueprint('blog', __name__)

@blog.route('/')
def index():
    posts = Post.query.order_by(Post.created).all()
    return render_template('blog/index.html', posts=posts, getPostUser=getPostUser)

@blog.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            data = Post(current_user.id,title,body)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = Post.query.get(id)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post.author_id != current_user.id:
        abort(403)

    return post


@blog.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@blog.route("/<int:id>/delete", methods=('POST',))
@login_required
def delete(id):
    Post.query.filter_by(id=id).delete()
    db.sesssion.commit()
    return redirect(url_for('blog.index'))


@blog.route("/<int:id>/<action>")
@login_required
def like(id, action):
    post = get_post(id)
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

@blog.route("/<int:id>/comments")
def showComments(id):
    post = get_post(id)
    comments = post.comments
    return render_template('blog/comments.html', comments = comments, post = post)

@blog.route("/addComment", methods=('POST',))
def addComment():
    if request.method == 'POST':
        post_id = int(request.form['post_id'])
        print(post_id)
        body = request.form['body']
        
        error = None

        if body == '':
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            comment = PostComment(current_user.id, post_id, body)
            print(current_user.id)
            db.session.add(comment)
            db.session.commit()
            return redirect(request.referrer)

def getPostUser(id):
    return User.query.get(id).username