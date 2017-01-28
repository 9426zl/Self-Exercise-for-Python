# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, SelectField,\
    TextAreaField
from wtforms.validators import Required


class MoviePostForm(Form):
    title = StringField(u'题目.', validators=[Required()])
    body = TextAreaField(u'评论', validators=[Required()])
    submit = SubmitField(u'提交')


class MovieCommentForm(Form):
    body = TextAreaField(u'评论', validators=[Required()])
    submit = SubmitField(u'提交')


class MovieCommentReplyForm(Form):
    body = TextAreaField(u'回复', validators=[Required()])
    submit = SubmitField(u'提交')
