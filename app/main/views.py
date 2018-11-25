from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import CommentForm,BlogForm, DeletePost
from flask_login import login_required, current_user
from .. import auth
from ..models import User,Comment,Blog
from .forms import UpdateProfile
from .. import db,photos
import markdown2
from ..email import mail_message


@main.route('/')

def index():
    '''
    View root page function that returns index page and its data
    '''
    title = 'BLOG MANENOS'

    

    return render_template('index.html', title = title, index = index)



@main.route('/comment' , methods = ['GET','POST'])
@login_required
def comment():
    form = CommentForm() 
    del_form = DeletePost()
    if form.validate_on_submit():
        comment = Comment(user=form.user.data,comment=form.comment.data)
        comment.save_comment()
        
        return redirect(url_for('main.comment'))
    elif del_form.validate_on_submit():
        
        comment_id = del_form.comment_id.data
        comment= Comment.query.filter_by(comment=comment_id).first()
        if comment:
            
            comment.delete_comment(comment)
        return redirect(url_for('main.comment'))
        
    comments=Comment.query.all()

    return render_template('comment.html', form = form ,comments=comments, del_form=del_form)    


@main.route('/blog' , methods = ['GET','POST'])
@login_required
def blog():
    form = BlogForm() 
    if form.validate_on_submit():
        blog = Blog(user=form.user.data,blog=form.blog.data,heading=form.heading.data)
        blog.save_blog()
        user=User.query.all()
        for email in user:
            mail_message("Blog updates","email/subscription",email.email,user=user)
        return redirect(url_for('main.blog'))
        
    posts=Blog.query.all()

    return render_template('blog.html',posts=posts, form = form )     




@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)



@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))