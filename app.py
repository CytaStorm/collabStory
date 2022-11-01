# Bottlers (Jeff Chen, Yusha Aziz, Fang Chen)
# SoftDev
# P00
# 2022-11-01

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)    #create Flask object

@app.route("/")
def disp_loginpage():
    return render_template( 'login.html' )

@app.route("/auth")
def authenticate():
    return render_template( 'adding.html' )

@app.route("/signUp", methods=['GET','POST'])
def signup():
    if request.method == 'GET': #if opening this route
        return render_template('signup.html') 
    if request.method == 'POST': #if submitting information
        usernames = users.keys()
        newuser = request.form.get('username') #when using "POST" request.args DNE
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        if newuser in usernames: #check if user exists
            error = "Username already exists"
            return render_template('signup.html', 
                error=error) #redirects back to page with error
        if password != confirmation: 
            error = "PASSWORDS DO NOT MATCH!!!!!!"
            return render_template('signup.html', 
                error=error)

        with open('users.csv','a') as csvfile: #if newuser works, add to csv
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([newuser,password])
        get_users() #update local dict to match csv

        return render_template('login.html')
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
