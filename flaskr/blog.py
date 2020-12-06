from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from flask_login import login_required, current_user
from flaskr.models import Post, db

blog = Blueprint('blog', __name__)

@blog.route('/')
def index():
    posts = Post.query.order_by(Post.created).all()
    return render_template('blog/index.html', posts=posts)

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

@login_required
@blog.route("/<int:id>/like")
def like(id):
    post = get_post(id)

    post.likes += 1
    db.session.commit()
    return redirect(url_for('blog.index'))