from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

app = Flask(__name__)
app.secret_key = "akjsnajkcbahcbs"

ACCESS_CODE = "42"

users = {}


class User:
    def __init__(self, realname, username, password):
        self.realname = realname
        self.username = username
        self.password = password


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('log in')


def validate_accesscode(form, field):
    if field.data != ACCESS_CODE:
        raise ValidationError('Invalid access code')


class RegisterForm(FlaskForm):
    realname = StringField('realname', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('<PASSWORD>', validators=[DataRequired(), EqualTo('password')])
    accesscode = StringField('accesscode', validators=[DataRequired(), validate_accesscode])
    submit = SubmitField('register')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.is_submitted():
        realname = form.realname.data
        username = form.username.data
        password = form.password.data

        new_user = User(realname, username, password)
        users[username] = new_user
        return redirect(url_for('login'))
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        username = form.username.data
        password = form.password.data
        user_info = users.get(username, None)
        if user_info is not None and user_info.password == password:
            print("Login successful!")
            session["username"] = username
            return redirect(url_for("welcome"))
        else:
            print("Login failed!")
            return render_template("login.html",  form=form)
    else:
        return render_template("login.html", form=form)


@app.route("/")
def welcome():
    username = session.get("username", None)
    if username is not None:
        return render_template("welcome.html", realname=users[username].realname)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    del session["username"]
    return redirect(url_for("login"))