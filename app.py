from flask import Flask, render_template,url_for,redirect,session,flash,request
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key="vivekkali"


@app.route("/",methods=["GET","POST"])
def home():
    return render_template("home.html")
   


@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        name=request.form.get("name")
        college=request.form.get("college")
        gender=request.form.get("gender")
        email=request.form.get("email")
        password=request.form.get("password")

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
        email =request.form.get("email")
        password =request.form.get("password")
        session["email"]=email
        session["password"]=password
        return redirect(url_for("home"))
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





if __name__=="__main__":
    app.run(debug=True)
