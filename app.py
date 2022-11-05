# Bottlers (Jeff Chen, Yusha Aziz, Fang Chen)
# SoftDev
# P00
# 2022-11-01

from flask import Flask, render_template, request
import sqlite3

### SETUP ###

DB_FILE = "logins.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #the "check_same_thread=False" is needed to stop errors
c = db.cursor()

# CREATING login TABLE in logins.db
tbleName = "login"
parameters = "UserID INT, Name TEXT, Password TEXT"

command = (f"create table if not exists {tbleName} ({parameters})")
c.execute(command)
db.commit() #save changes

#CREATING User entries TABLE in logins.db
tbleName = "entries"
parameters = "UserID INT, Line TEXT"

"""
command = "drop table entries"
c.execute(command)
"""
command = (f"create table if not exists {tbleName} ({parameters})")
c.execute(command)
db.commit() #save changes

#COOKIES


### FLASK ###
app = Flask(__name__)    #create Flask object

@app.route("/")
def disp_loginpage():
    return render_template( 'login.html' )

@app.route("/auth", methods=['POST'])
def authenticate():
    userID = request.form['username']
    password = request.form['password']
    logList = c.execute('select * from login').fetchall()
    
    idExists = False
    
    for IDs in logList:
        if userID == IDs[0]:
            # combo = IDs
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
        #print(currentUser)
        return render_template('storyInput.html') #returns story page with userID stored
    else:
        print("wrong password")
        return render_template('login.html', error = "Wrong Password") #calls the HTML file with the error
        
    return "How'd you even get here?"

@app.route("/signUp")
def signUp(): #this code will change the HTML template from login.html to signUp.html
    return render_template( 'signup.html' )

@app.route("/register", methods=['POST'])
def register():
    username = request.form['username']
    pass1 = request.form['password1']
    pass2 = request.form['password2']
    logList = c.execute('select * from login').fetchall()
    print("List of Logins ") 
    print(logList)
    for useID in logList :
        print(useID[0])
        if username == useID[0] and pass1 == useID[1]:
            print(useID[0] + useID[1])
            return render_template('signup.html', 
                                   error= "Username and Password combination already exists") #redirects back to page with error
    if pass1 != pass2: 
        error = "Passwords Do Not Match Try Again!"
        return render_template('signup.html', 
            error=error)

    command = (f"INSERT INTO login VALUES(\"{username}\", \"{pass1}\", \"{ID}\")") #the \"\"
    c.execute(command)
    print(c.execute('select * from login').fetchall())
    db.commit()
    return render_template('login.html')

@app.route("/addedStory", methods=['POST'])
def addedStory():
    # add entry into the main story
    newEntry = request.form['newEntry']
    command = (f"INSERT INTO entries VALUES(\"{currentUser}\", \"{newEntry}\")")
    c.execute(command) 
    # get the str of the whole story
    list = c.execute('select * from entries').fetchall()
    storyText = ""
    for phrases in list:
        storyText = storyText + "\n" + phrases[1]
    db.commit()
    print(currentUser + "test")
    return render_template('addedStory.html', story=storyText)

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()

db.commit()
db.close()  #close database
