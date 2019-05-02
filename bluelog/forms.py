from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from bluelog.models import Category


class LoginForm(FlaskForm):
    #登录表单
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


class SettingForm(FlaskForm):
    #博客设置表单
    name = StringField('姓名', validators=[DataRequired(), Length(1, 70)])
    blog_title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('副标题', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('关于页面', validators=[DataRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    #文章表单
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('分类', coerce=int, default=1)
    body = CKEditorField('正文', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    #分类创建表单
    name = StringField('姓名', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('姓名已经存在!')


class CommentForm(FlaskForm):
    #评论表单
    author = StringField('姓名', validators=[DataRequired(), Length(1, 30)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('站点', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('评论', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    #管理员表单 隐藏了作者，邮件，站点
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 30)])
    url = StringField('链接', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()
