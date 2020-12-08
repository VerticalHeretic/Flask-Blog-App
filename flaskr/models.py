from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class PostComment(db.Model):
    __tablename__ = 'post_comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    body = db.Column(db.Text, nullable=False)

    def __init__(self, user_id,post_id, body):
        self.body = body
        self.user_id = user_id
        self.post_id = post_id

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    likes = db.relationship('PostLike',foreign_keys='PostLike.post_id', backref='post', lazy=True)
    comments = db.relationship('PostComment',foreign_keys='PostComment.post_id', backref='post', lazy=True)

    def __init__(self, author_id, title, body):
        self.author_id = author_id
        self.title = title
        self.body = body

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy=True)

    commented = db.relationship(
        'PostComment',
        foreign_keys='PostComment.user_id',
        backref='user', lazy=True)

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def __init__(self, username, password):
        self.username = username
        self.password = password



