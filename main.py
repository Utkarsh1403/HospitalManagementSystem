import flask
from flask import Flask,request,redirect
import sqlite3

con= sqlite3.connect("hospitalmanagement.db",check_same_thread=False)
curr= con.cursor()

listOfTables= con.execute("SELECT name from sqlite_master WHERE type='table' AND name='PATIENTSDETAILS' ").fetchall()

if listOfTables!=[]:
    print("Table Already Exists !")

else:
    con.execute('''CREATE TABLE PATIENTSDETAILS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,Mobilenumber INTEGER,Age INTEGER, 
        Address TEXT,Dob INTEGER, Place TEXT,Pincode INTEGER);''')

print("Table has Created")

app = Flask(__name__)

@app.route("/")
def login():

    return flask.render_template("login.html")

@app.route("/dashboard",methods=["GET","POST"])
def addPatient():
    if request.method=="POST":
        getName=request.form["Name"]
        getMobilno=request.form["mobno"]
        getAge = request.form["age"]
        getAddress = request.form["addr"]
        getDob = request.form["DOB"]
        getPlace = request.form["place"]
        getPincode = request.form["pincd"]

        print(getName)
        print(getMobilno)
        print(getAge)
        print(getAddress)
        print(getDob)
        print(getPlace)
        print(getPincode)

        try:
            con.execute("INSERT INTO PATIENTSDETAILS(Name,Mobilenumber,Age,Address,Dob,Place,Pincode) VALUES('"+getName+"',"+getMobilno+","+getAge+",'"+getAddress+"',"+getDob+",'"+getPlace+"',"+getPincode+")")
            print("Succesfully Inserted")
            con.commit()
            return redirect('/Viewall')
        except Exception as e:
            print(e)

    return flask.render_template("addpatient.html")

@app.route("/search",methods=['GET','POST'])
def search():
    if request.method =="POST":
        getMobilno = request.form["mobno"]
        print(getMobilno)
        try:
            query = "SELECT* FROM PATIENTSDETAILS WHERE Mobilenumber="+getMobilno
            print(query)
            curr.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result= curr.fetchall()
            print(result)
            if len(result)==0:
                print("Invalid Mobile Number")
            else:
                print(len(result))
                return flask.render_template("search.html",Patient=result,status=True)
        except Exception as e:
            print(e)
    return flask.render_template("search.html",Patient=[],status=False)

@app.route("/delete",methods = ['GET','POST'])
def delete():
    if request.method=="POST":
        getMobilno = request.form["mobno"]
        print(getMobilno)
        try:
           query = "DELETE FROM PATIENTSDETAILS WHERE Mobilenumber="+getMobilno
           curr.execute(query)
           print("SUCCESSFULLY DELETED!")
            # result = curr.fetchall()
            # print(result)
           con.commit()
        except Exception as e:
            print(e)
    return flask.render_template("delete.html")


@app.route("/Viewall")
def Viewall():
    curr = con.cursor()
    curr.execute("SELECT* FROM PATIENTSDETAILS")
    result = curr.fetchall()

    return flask.render_template("viewall.html",patients=result)

@app.route("/update",methods=['GET','POST'])
def update():
    if request.method=="POST":
        getMobilno = request.form["mobno"]
        print(getMobilno)
        try:
            curr.execute("SELECT* FROM PATIENTSDETAILS WHERE Mobilenumber="+getMobilno)
            print("SUCCESSFULLY SELECTED!")
            result = curr.fetchall()
            return redirect("/viewupdate")
        except Exception as e:
            print(e)
            # if len(result)==0:
            #     print("Invalid Mobile Number")
            # else:
            #     print(len(result))
            #     return flask.render_template("update.html",)

    return flask.render_template("update.html")

@app.route("/viewupdate",methods=['GET','POST'])
def viewupdate():
    if request.method=="POST":
        getName=request.form["Name"]
        getMobilno=request.form["mobno"]
        getAge = request.form["age"]
        getAddress = request.form["addr"]
        getDob = request.form["DOB"]
        getPlace = request.form["place"]
        getPincode = request.form["pincd"]

        print(getName)
        print(getMobilno)
        print(getAge)
        print(getAddress)
        print(getDob)
        print(getPlace)
        print(getPincode)
        try:
            con.execute("UPDATE PATIENTSDETAILS(Name,Mobilenumber,Age,Address,Dob,Place,Pincode) VALUES('"+getName+"',"+getMobilno+","+getAge+",'"+getAddress+"',"+getDob+",'"+getPlace+"',"+getPincode+")")
            print("SUCCESFULLY UPDATED!")
            con.commit()
            return redirect('/Viewall')
        except Exception as e:
            print(e)
    return flask.render_template("viewupdate.html")

if (__name__) == "__main__":
        app.run(debug=True)