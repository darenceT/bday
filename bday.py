from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, validators 
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.fields import DateField
# from wtforms.widgets import html5
from wiki import findBirths
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel


class searchForm(FlaskForm):
    date = DateField(label='Date', format='%Y-%m-%d')
    limit = IntegerField(
        label="limit",
        validators=[validators.InputRequired(), validators.NumberRange(min=1, max=20)], 
        default=10)
    search = SubmitField(label="Search")

class loginForm(FlaskForm):
    email=StringField(label="Enter email", validators=[DataRequired(), Email()])
    password=PasswordField(label="Enter password", validators=[DataRequired(), Length(min=6, max=16)])
    submit=SubmitField(label="Login")

app = Flask(__name__)
app.secret_key = "a secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/login.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login.init_app(app)

def addUser(email, password):
    # check if email or username exists
    user = UserModel()
    user.set_password(password)
    user.email = email
    db.session.add(user)
    db.session.commit()

@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email = "dthong@uw.edu").first()
    if user is None:
        addUser("dthong@uw.edu", '1234567890')

@app.route("/home", methods=['GET', 'POST'])
@login_required
def findBirthdays():
    # search_query = ("03/28", "1986", 10)
    form = searchForm()
    # print(form)
    if form.validate_on_submit() and request.method == "POST":
        date = form.dt.data.strftime('%Y%m/%d')
        year = date[:4]
        month_day = date[4:]
        search_query = (month_day, year, form.limit)
        return render_template("home.html", found_bdays=findBirths(*search_query), form=form)
    return render_template("home.html", form=form)

@app.route("/")
def redirectToLogin():
    return redirect("/login")
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    form=loginForm()
    if form.validate_on_submit() and request.method == "POST":
        email=request.form["email"]
        pw=request.form["password"]
        user = UserModel.query.filter_by(email = email).first()
        # if user is not None and user in passwords and passwords[user] == pw:
        if email is not None and user.check_password(pw): 
            login_user(user)
            return redirect('/home')
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)