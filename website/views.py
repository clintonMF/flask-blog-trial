from ssl import HAS_TLSv1_1
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user,login_required
from .models import Post,User, Comment, Like
from . import db

views = Blueprint('views', __name__,)

@views.route('/')
@views.route('/home')
@login_required
def home():
    """the home function which returns the user to the homepage"""
    posts = Post.query.all()

    return render_template('home.html', user=current_user, posts=posts)
    #user=current_user and posts=posts are used to pass information to the front end regarding the users being logged in or not
    
@views.route('/create-post', methods=['GET','POST'])
@login_required
def create_post():
    """ this is the function that handles the creation of post"""
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty', category = "message")
        else:
            post = Post(text=text,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created!")
        return redirect(url_for('views.home', user=current_user))
    return render_template('create_post.html', user=current_user)


@views.route('/delete-post/<id>')
@login_required
def delete_post(id):
    """ This is a function that enables the author of a post to delete it."""
    post = Post.query.filter_by(id=id).first()
    
    if not post:
        flash('post does not exist', category='error')
    elif post.author != current_user.id:
        flash("you don't have permission to delete this post", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('post deleted!', category='success')
        
    return redirect(url_for('views.home', user=current_user))

@views.route('/posts/<username>/')
@login_required
def posts(username):
    """ this function helps in showing all the post a certain user has created"""
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('user does not exist', category="error")
        return redirect(url_for('views.home', user=current_user))
    
    posts = user.posts
    return render_template('post.html',user=user,posts=posts) 

@views.route('/create_comment/<post_id>', methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('comment cannot be empty', category="error")
    
    else:
        post = Post.query.filter_by(id=post_id).first()
        
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('comment posted successfully', category="success")
            
        else:
            flash("post does not exist", category="error")
            
    return redirect(url_for('views.home'))

@views.route('/delete-comment/<int:comment_id>')
@login_required
def deletecomment(comment_id):
    """This function enables the author of a post or the comment
    author to delete the post"""
    
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('comment does not exist',category='error')
    elif comment.author != current_user.id and  current_user.id != comment.post.author:
        flash("you don't have permission to delete this post", category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("post has been", category="success")
     
    return redirect(url_for('views.home'))


@views.route('like-post/<int:post_id>')
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    
    if not post:
        flash("post does not exist",category="error")
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id,post_id=post_id)
        db.session.add(like)
        db.session.commit()
    
    return redirect(url_for('views.home'))
    