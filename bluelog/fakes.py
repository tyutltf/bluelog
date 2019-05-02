import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from bluelog import db
from bluelog.models import Admin, Category, Post, Comment, Link

fake = Faker()


def fake_admin():
    '''
    生成虚拟管理员信息

    '''
    admin = Admin(
        username='admin',
        blog_title='Bluelog',
        blog_sub_title="Jupyter notebook使用...",
        name='雨轩恋i',
        about='雨轩恋i,何许人也?祖籍河东也,少小离家,奔波劳碌二十年也,终有一番事业。'
    )
    admin.set_password('ltf1234')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    '''
    生成虚拟分类

    '''
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    '''
    生成虚拟文章
    '''
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    '''
    生成虚拟评论
    '''
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # 未审核评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # 管理员发表评论
        comment = Comment(
            author='雨轩恋i',
            email='18235121656@163.com',
            site='tyutltf.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # 回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    twitter = Link(name='推特', url='#')
    facebook = Link(name='脸书', url='#')
    linkedin = Link(name='领英', url='#')
    google = Link(name='谷歌', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
