from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, IntegerField, SubmitField, EmailField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError 
import string
from table import Users


class ProductForm(FlaskForm):
    type=StringField("type")
    name=StringField("name")
    description=TextAreaField("description")
    manufacturer=StringField("manufacturer")
    price=IntegerField("price")
    photo=FileField("photo")
    submit=SubmitField("create new product")
    

class LoginForm(FlaskForm):
    login=StringField("login", validators=[DataRequired()])
    password=PasswordField("password", validators=[DataRequired()])
    submit=SubmitField("login in")


class AuthozizateForm(FlaskForm):
    email=EmailField("e-mail", validators=[DataRequired(), Email(message='Your email incorrect')])
    login=StringField("login", validators=[DataRequired(), Length(min=6)])
    password=PasswordField("password", validators=[EqualTo("password22", message='Passwords not equal')])
    password22=PasswordField("confirm password", validators=[DataRequired()])
    submit=SubmitField("registration")


    def validate_password(self, password):

        cont=0

        for i in self.password.data:

            if i in string.ascii_lowercase:
                cont+=1
                break

        for i in self.password.data:

            if i in string.ascii_uppercase:
                cont+=1
                break

        for i in self.password.data:
            if i in string.digits:
                cont+=1
                break
        
        for i in self.password.data:
            if i in string.punctuation:
                cont+=1
                break

        if cont<4:
            raise ValidationError('invalid password! ')

    def validate_login(self, login):

        if self.login.data[0] not in string.ascii_letters:
            raise ValidationError('the first letter in login must be Latin')
        
        for i in self.login.data:
            if i not in string.digits + string.ascii_letters + '_':
                raise ValidationError('invalid characters')

        user = Users.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('this login is already in use')

class CommentForm(FlaskForm):
    like=IntegerField(label=("like"),
                      validators=[DataRequired()])
    comment=TextAreaField("comment")
    submit=SubmitField("add comment")

    def validate_like(self, like):
        if self.like.data>5 or self.like.data<1:
            raise ValidationError('mark should be about 1-5')