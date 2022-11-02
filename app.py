# Bottlers (Jeff Chen, Yusha Aziz, Fang Chen)
# SoftDev
# P00
# 2022-11-01

from flask import Flask, render_template, request
import sqlite3

DB_FILE = "logins.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #the "check_same_thread=False" is needed to stop errors
c = db.cursor()
currentUser = ""

# CREATING login
tbleName = "login"
parameters = "UserID INT, Name TEXT, Password TEXT"

command = (f"create table if not exists {tbleName} ({parameters})")
c.execute(command)
db.commit() #save changes

#CREATING User entries
tbleName = "entries"
parameters = "UserID INT, Line TEXT"

command = (f"create table if not exists {tbleName} ({parameters})")
c.execute(command)
db.commit() #save changes


app = Flask(__name__)    #create Flask object

@app.route("/")
def disp_loginpage():
    return render_template( 'login.html' )

@app.route("/auth")
def authenticate():
    userID = int(request.args['username'])
    password = str(request.args['password'])
    logList = c.execute('select * from login').fetchall()
    
    idExists = False
    
    for IDs in logList:
        if userID == int(IDs[0]):
            combo = IDs
            idExists = True
            break #not needed but makes it faster
    if(idExists == False):
        print("\n")
        print("WRONG USERNAME \n") #code to see it working in the terminal
        return render_template('login.html', error = "Username Does not Exist, GO BACK") #calls the function with the error
    else:
        print("\n") 
        print("Username is correct")
    
    if(password == IDs[2]):
        print("password Works")
        currentUser = userID
        return render_template('storyInput.html') #returns story page with userID stored
    else:
        print("wrong password")
        return render_template('login.html', error = "Wrong Password") #calls the HTML file with the error
        
    return "HEYYYYYYYYYY WHY U HERE MF"

@app.route("/signUp")
def signUp(): #this code will change the HTML template from login.html to signUp.html
    return render_template( 'signup.html' )

@app.route("/register")
def register():
    user1 = int(request.args['username1'])
    pass1 = request.args['password1']
    pass2 = request.args['password2']
    name = str(request.args['name1'])
    logList = c.execute('select * from login').fetchall()
    print("List of Logins ") 
    print(logList)
    for useID in logList :
        print(useID[0])
        if user1 == int(useID[0]):
            print(useID[0])
            return render_template('signup.html', 
                                   error= "Username already exists") #redirects back to page with error
    if pass1 != pass2: 
        error = "Passwords Do Not Match Try Again!"
        return render_template('signup.html', 
            error=error)
    pass1 = str(pass2)
    command = (f"INSERT INTO login VALUES(\"{user1}\", \"{name}\", \"{pass1}\")") #the \"\"
    c.execute(command)
    print(c.execute('select * from login').fetchall())
    db.commit()
    return render_template('login.html')

@app.route("/addStory")
def addStory():
    return render_template('storyInput.html')

@app.route("/addedStory", methods=['POST'])
def addedStory():
    newEntry = request.form['newEntry']
    command = (f"INSERT INTO entries VALUES(\"{currentUser}\", \"{newEntry}\")")
    c.execute(command) 
    print(c.execute('select * from entries'))
    db.commit()
    return render_template('addedStory.html')

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()

db.commit()
db.close()  #close database
