# Bottlers (Jeff Chen, Yusha Aziz, Fang Chen)
# SoftDev
# P00
# 2022-11-01

from flask import Flask, render_template, request, session
import sqlite3

### SETUP ###
DB_FILE = "logins.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #the "check_same_thread=False" is needed to stop errors
c = db.cursor()

testingUser = "test"

# CREATING login TABLE in logins.db
tbleName = "login"
parameters = "UserID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Password TEXT"

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

currentUser = 0

### FLASK ###
app = Flask(__name__)    #create Flask object
app.secret_key = b'ekifl@&n&!urniwer7[23[q894;8^'

@app.route("/")
def routing():
    print("routing...")
    entriesList = c.execute('select * from entries').fetchall()
    
    if 'user' in session:
        entered = False
        for entry in entriesList:
            if entry[0] == session['user']:
                entered = True 
                break
        if entered:
            storyText = ""
            for phrase in entriesList:
                storyText = storyText + "\n" + str(phrase[1])
            return render_template('addedStory.html', story=storyText)
        else:
            if len(entriesList) == 0:
                return render_template('storyInput.html')
            else:
                return render_template('storyInput.html', lastEntry = str(entriesList[-1][1]))
    return render_template('login.html')

@app.route("/auth", methods=['POST'])
def authenticate():
    print("authenticating...")

    username = request.form['username']
    password = request.form['password']
    logList = c.execute('select * from login').fetchall()
    entriesList = c.execute('select * from entries').fetchall()
    
    userExists = False
    
    # Find if username exists in login database
    for IDs in logList:
        if username == IDs[1]:
            combo = IDs
            userExists = True
            break #not needed but makes it faster
    if(not(userExists)):
        print("\n")
        print("WRONG USERNAME \n") #code to see it working in the terminal
        return render_template('login.html', error = "Username Does not Exist, GO BACK") #calls the function with the error
    else:
        print("\n") 
        print("Username is correct")
    
    # Username EXISTS; check if password matches
    if(password == combo[2]):
        print("password Works")
        session['user'] = combo[0] #Start a session
        
        entered = False
        for entry in entriesList:
            if entry[0] == session['user']:
                entered = True 
                break
        if entered:
            storyText = ""
            for phrase in entriesList:
                storyText = storyText + "\n" + str(phrase[1])
            return render_template('addedStory.html', story=storyText)
        else:
            if len(entriesList) == 0:
                return render_template('storyInput.html')
            else:
                return render_template('storyInput.html', lastEntry = str(entriesList[-1][1]))
    else:
        print("wrong password")
        return render_template('login.html', error = "Wrong Password") #calls the HTML file with the error
        

@app.route("/signUp")
def signUp(): #this code will change the HTML template from login.html to signUp.html
    print("signing up...")
    return render_template( 'signup.html' )

@app.route("/register", methods=['POST'])
def register():
    print("registering...")
    username = request.form['username']
    pass1 = request.form['password1']
    pass2 = request.form['password2']
    newID = 1
    logList = c.execute('select * from login').fetchall()
    print("List of Logins ") 
    print(logList)
    for useID in logList :
        print(useID[0])
        if username == useID[1]:
            print(useID[1])
            return render_template('signup.html', 
                                   error= "Username already exists") #redirects back to page with error
    if pass1 != pass2: 
        error = "Passwords Do Not Match Try Again!"
        return render_template('signup.html', 
            error=error)
    command = (f"INSERT INTO login VALUES(NULL, \"{username}\", \"{pass1}\")") #the \"\"
    c.execute(command)
    print(c.execute('select * from login').fetchall())
    db.commit() #commit to update the db
    return render_template('login.html')

@app.route("/addedStory", methods=['POST'])
def addedStory():
    inUserList = c.execute('select UserID from entries').fetchall()

    if session['user'] not in inUserList:
        print("adding and printing story...")
        # add entry into the main story
        newEntry = request.form['newEntry']
        command = (f"INSERT INTO entries VALUES(\"{session['user']}\", \"{newEntry}\")")
        c.execute(command)
        db.commit()
    
    inputList = c.execute('select Line from entries').fetchall()
    storyText = ""

    # get the str of the whole story
    for phrase in inputList:
        storyText = storyText + "\n" + str(phrase[0])

    return render_template('addedStory.html', story=storyText)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('user')
    return render_template('login.html')


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()

db.commit()
db.close()  #close database
