# _*_ coding:utf-8 _*_
import os
from flask import render_template, redirect, url_for, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .. import db
from ..models import User, Role, Permission, Post, Movie, Comment
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, ImageForm
from ..decorators import admin_required, permission_required



@main.route('/')
def index():
    return render_template('index.html')


@main.route('/warmovie', methods=['GET', 'POST'])
def warmovie():
    return render_template('war_movie.html')


@main.route('/crimemovie', methods=['GET', 'POST'])
def crimemovie():
    return render_template('crime_movie.html')


@main.route('/clinteastwood', methods=['GET', 'POST'])
def clinteastwood():
    return render_template('clint_eastwood.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    show_followed = 0
    show_followed = request.cookies.get('show_followed', '')

    if show_followed == '2':
        query = current_user.comments_of_post
    elif show_followed == '1':
        query = current_user.followed_posts
    else:
        query = current_user.posts_of_star

    if show_followed != '2':
        pagination = query.order_by(Post.timestamp.desc()).paginate(
            page, per_page=10, error_out=False)
        posts = pagination.items
        return render_template('user.html', user=user, current_user=current_user,
                               posts=posts, pagination=pagination)
    else:
        pagination = query.order_by(Comment.timestamp.desc()).paginate(
            page, per_page=10, error_out=False)
        comments = pagination.items
        return render_template('user.html', user=user, current_user=current_user,
                               comments=comments, pagination=pagination)


@main.route('/setting/<username>', methods=['GET', 'POST'])
@login_required
def setting(username):
    if current_user.username != username and not current_user.is_administrator():
        flash('You are not authorized to the page')
        return redirect('/')
    form = EditProfileForm()
    user = User.query.filter_by(username=username).first_or_404()
    upload_image = False
    if form.validate_on_submit():
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('Your profile has been updated.')
        return redirect(url_for('main.user', username=user.username))
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    show_account = False
    return render_template('setting.html', form=form, show_account=show_account,
                           user=user, upload_image=upload_image)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'您的基本资料已更新')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('setting.html', form=form, user=current_user)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/upload_image', methods=['GET', 'POST'])
@login_required
def upload_image():
    form = ImageForm()
    uploadimage = True
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        suffix = filename.split(".")[-1]
        form.image.data.save('./app/static/uploads/' + str(current_user.id) +
                             "." + suffix)
        current_user.upload = True
        db.session.add(current_user)
        flash('The profile has been updated.')
    else:
        filename = None
    return render_template('setting.html', form=form, filename=filename, user=current_user,
                           uploadimage=uploadimage)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['MYSITE_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u"的关注者",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['MYSITE_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u"关注了",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/star_movies/<username>')
def star_movies(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = user.starfilm.paginate(
        page, per_page=current_app.config['MYSITE_FOLLOWERS_PER_PAGE'],
        error_out=False)
    stars = [{'movie': Movie.query.filter_by(id=item.movie_id).first()} for item in pagination.items]
    return render_template('star_movie.html', user=user, title=u"收藏的影片",
                           endpoint='.star_movies', pagination=pagination,
                           stars=stars)


@main.route('/all/<username>')
@login_required
def show_star_movie(username):
    resp = make_response(redirect(url_for('.user', username=username)))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed/<username>')
@login_required
def show_followed(username):
    resp = make_response(redirect(url_for('.user', username=username)))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/comment/<username>')
@login_required
def show_comment(username):
    resp = make_response(redirect(url_for('.user', username=username)))
    resp.set_cookie('show_followed', '2', max_age=30*24*60*60)
    return resp
