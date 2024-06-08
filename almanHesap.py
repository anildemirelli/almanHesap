from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_wtf import FlaskForm


app = Flask(__name__)
app.secret_key = "ortakHesap"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ortakHesap"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

#Login Form
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":

        username = request.form["text"]
        password_entered = request.form["pswd"]
        cursor = mysql.connection.cursor()
        sorgu = "Select * From users where username = %s"
        result = cursor.execute(sorgu,(username,))

        if result > 0:
            data = cursor.fetchone()
            realPassword = data["password"]

            if sha256_crypt.verify(password_entered,realPassword):
                flash("meraba", "meraba")

                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                flash("Parolanız hatalı !")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor !", "danger")
            return redirect(url_for("login"))
    else:
        return render_template("index.html")




#Kayıt Form
@app.route("/kayit")
def kayit():
    return render_template("kayit.html")

#Kayıt Fonksiyonu
@app.route("/register", methods = ["POST"])
def register():

    name = request.form["name"]
    username = request.form["txt"]
    email = request.form["email"]
    password = request.form["pswd"]
    pwConfirm = request.form["pswd2"]

    if password != pwConfirm:
        flash("Lütfen parolanızı onaylayın !")
        return redirect(url_for("kayit"))
    else:
        try:
            password = sha256_crypt.encrypt(password)
            cursor = mysql.connection.cursor()
            sorgu = "Insert into users (name,username,email,password) VALUES(%s,%s,%s,%s)"
            cursor.execute(sorgu,(name,username,email,password))
            mysql.connection.commit()
            cursor.close()
            a,b = "Başarıyla kayıt oldunuz !","başarı"
            return render_template("index.html",a=a,b=b)
        except:
            flash("Kullanıcı adı zaten kullanılıyor")
            return redirect(url_for("kayit"))









@app.route("/main")
def main():
    flash("merhaba","danger")
    return render_template("main.html")



















if __name__ == "__main__":
    app.run(debug=True)
