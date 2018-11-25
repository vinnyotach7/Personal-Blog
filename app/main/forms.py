from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required



class BlogForm(FlaskForm):

    user = StringField('Your name',validators=[Required()])

    heading = StringField('Blog Heading',validators=[Required()])

    blog = TextAreaField('Your blog',validators=[Required()])
    
    submit = SubmitField('Post')


class CommentForm(FlaskForm):

    user = StringField('Your name',validators=[Required()])

    comment = TextAreaField('Your comment',validators=[Required()])
    
    submit = SubmitField('Comment')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')   

class DeletePost(FlaskForm):
    comment_id = StringField()
    delete = SubmitField('Delete')
