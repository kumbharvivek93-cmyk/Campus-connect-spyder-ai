from flask import Flask, render_template,url_for,redirect,session,flash,request
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key="vivekkali"
app.permanent_session_lifetime=timedelta(minutes=60)
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///user.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))
    college=db.Column(db.String(30))
    gender=db.Column(db.String(30))
    email=db.Column(db.String(30),unique=True)
    password=db.Column(db.String(30))

@app.route("/",methods=["GET","POST"])
def home():
    return render_template("home.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    session.permanent=True
    if request.method=="POST":
        name=request.form.get("name")
        college=request.form.get("college")
        gender=request.form.get("gender")
        email=request.form.get("email")
        password=request.form.get("password")

        new_user=User(
            name=name,
            college=college,
            gender=gender,
            email=email,
            password=password

        )
        db.session.add(new_user)
        db.session.commit()


        session["name"]=name
        session["college"]=college
        session["gender"]=gender
        session["email"]=email
        session["password"]=password
        
        return redirect(url_for("home"))
    
    else:
        if "name" in session:
            return redirect(url_for("home"))
        else:
            return render_template("signup.html")
        
@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session["email"] = user.email
            session["name"] = user.name
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))

    else:
        if "email" in session:
            return redirect(url_for("home"))
        else:
            return render_template("login.html")

@app.route("/logout",methods=["GET","POST"])
def logout():
    return render_template("confirm_logout.html")


@app.route("/finallogout",methods=["GET","POST"])
def finallogout():
    session.clear()
    return render_template("logout.html")

@app.route("/users")
def users():
    all_users = User.query.all()
    for user in all_users:
        print(user.name, user.email, user.college)

    return "Check terminal"
@app.route("/allusers")
def allusers():
    users = User.query.all()
    return render_template("allusers.html", users=users)


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
