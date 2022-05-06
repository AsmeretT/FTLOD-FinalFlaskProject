from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

ftlod = Blueprint('ftlod', __name__, template_folder='ftlod_templates')

from .forms import CreatePostForm, UpdatePostForm
from app.models import db, Post

@ftlod.route('/posts')
def posts():
    posts = Post.query.all()[::-1]
    return render_template('posts.html', posts = posts)

@ftlod.route('/newpost', methods=["GET", "POST"])
@login_required
def createPost():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post = Post(title, img_url, caption, current_user.id)

            db.session.add(post)
            db.session.commit()   

            return redirect(url_for('home')) 

    return render_template('newpost.html', form = form)

@ftlod.route('/posts/<int:post_id>')
def singlepost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('ftlod.posts'))
    return render_template('singlepost.html', post = post)

@ftlod.route('/posts/update/<int:post_id>', methods=["GET","POST"])
@login_required
def updatePost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('ftlod.posts'))
    if post.user_id != current_user.id:
        return redirect(url_for('ftlod.posts'))
    form = UpdatePostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            # update the original post
            post.title = title
            post.image = img_url
            post.caption = caption

            db.session.commit()   

            return redirect(url_for('home'))         
    return render_template('updatepost.html', form=form, post = post)

@ftlod.route('/posts/delete/<int:post_id>', methods=["POST"])
@login_required
def deletePost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('ftlod.posts'))
    if post.user_id != current_user.id:
        return redirect(url_for('ftlod.posts'))

    db.session.delete(post)
    db.session.commit()
               
    return redirect(url_for('ftlod.posts'))