from flask import render_template, redirect, url_for, flash, request,\
    current_app
from flask_login import current_user, login_required
from .. import db
from ..models import Post, Comment, Upvote, Voter, User
from . import movie
from .forms import MoviePostForm, MovieCommentForm, MovieCommentReplyForm


@movie.route('/<movieid>', methods=['GET', 'POST'])
def bestmovie(movieid):
    form = MoviePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, body_html='test',
                    movie_id=movieid, author_id=current_user.id)
        db.session.add(post)
        return redirect('movie/%s' % movieid)
    page = request.args.get('page', 1, type=int)
    query = Post.query.filter_by(movie_id=movieid)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('movie/%s.html' % movieid, form=form, pagination=pagination,
                           id=movieid, posts=posts, current_user=current_user)


@movie.route('/star/<movieid>', methods=['GET', 'POST'])
@login_required
def star(movieid):
    current_user.star(movieid)
    flash('You are staring the film.')
    return redirect('movie/%s' % movieid)


@movie.route('/unstar/<movieid>', methods=['GET', 'POST'])
@login_required
def unstar(movieid):
    current_user.unstar(movieid)
    flash('You are unstaring the film.')
    return redirect('movie/%s' % movieid)


@movie.route('/post/<postid>', methods=['GET', 'POST'])
@login_required
def post(postid):
    post = Post.query.get_or_404(postid)
    form = MovieCommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post_id=postid,
                          author_id=current_user.id)
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', postid=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['MYSITE_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['MYSITE_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@movie.route('/upvote/<postid>', methods=['GET', 'POST'])
@login_required
def upvote(postid):
    post = Post.query.get_or_404(postid)
    vote = Voter.query.filter_by(post_id=post.id).filter_by(voter_id=current_user.id).first()
    if not vote:
        upvotes = Upvote(post_id=post.id, post_author_id=post.author_id)
        voters = Voter(post_id=post.id, voter_id=current_user.id)
        db.session.add(upvotes)
        db.session.add(voters)
        flash('You upvote the review')
    else:
        flash('You have already upvoted the review')
    return redirect('movie/%s' % post.movie_id)


@movie.route('/comment_reply/<commentid>', methods=['GET', 'POST'])
@login_required
def comment_reply(commentid):
    form = MovieCommentReplyForm()
    comment = Comment.query.get_or_404(commentid)
    commentor = User.query.filter_by(id=comment.author_id).first();
    postid = comment.post_id
    if form.validate_on_submit():
        commentre = Comment(body="reply to" + " " + commentor.username + ": " + form.body.data,
                            post_id=postid,
                            author_id=current_user.id)
        db.session.add(commentre)
        commentre.creply(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', postid=postid, page=-1))
    return render_template('comment_reply.html', form=form)