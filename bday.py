from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wiki import findBirths

class loginForm(FlaskForm):
    email=StringField(label="Enter email", validators=[DataRequired(), Email()])
    password=PasswordField(label="Enter password", validators=[DataRequired(), Length(min=6, max=16)])
    submit=SubmitField(label="Login")

passwords = {}
passwords['dthong@uw.edu'] = '1234567890'

app = Flask(__name__)
app.secret_key = "a secret"

search_query = ("03/28", "1986", 20)

@app.route("/results")
def results():
    return render_template("results.html", found_bdays=findBirths(*search_query))

@app.route("/")
def redirectToLogin():
    return redirect("/login")
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    form=loginForm()
    if form.validate_on_submit() and request.method == "POST":
        user=request.form["email"]
        pw=request.form["password"]
        if user is not None and user in passwords and passwords[user] == pw:
            return redirect('/results')
    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)