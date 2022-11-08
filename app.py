# Bottlers (Jeff Chen, Yusha Aziz, Fang Chen)
# SoftDev
# P00
# 2022-11-01

from flask import Flask, render_template, request, session
import sqlite3

### SETUP ###
app = Flask(__name__)
app.secret_key = b'ekifl@&n&!urniwer7[23[q894;8^'
DB_FILE = "logins.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #the "check_same_thread=False" is needed to stop errors
c = db.cursor()


def updateStory(): #returns string story with all story from database
    list = c.execute('select * from entries').fetchall()
    storyText = ""
    for phrases in list:
        storyText = storyText + "\n" + phrases[1]
    return storyText

def hasSubmitted(usrID): #returns if the user has already submitted
    submitted = c.execute('select submitted from login where userID = {{usrID}}')
    if submitted == 1:
        return False
    return True

testingUser = "test"


# CREATING login TABLE in logins.db
tbleName = "login"
parameters = "UserID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Password TEXT, Submitted INTEGER"

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

### COOKIES ###


### FLASK ###
app = Flask(__name__)    #create Flask object

@app.route("/")
def disp_loginpage():
    return render_template( 'login.html' )

@app.route("/auth", methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    logList = c.execute('select * from login').fetchall()
    
    userExists = False
    
    for IDs in logList:
        if username == IDs[1]:
            combo = IDs
            userExists = True
            break #not needed but makes it faster
    if(userExists == False):
        print("\n")
        print("WRONG USERNAME \n") #code to see it working in the terminal
        return render_template('login.html', error = "Username Does not Exist, GO BACK") #calls the function with the error
    else:
        print("\n") 
        print("Username is correct")
    
    if(password == combo[2]):
        print("password Works")
        currentUser = combo[0]
        print(currentUser)
        #if hasSubmitted(session['userID']):
            #return render_template('addedStory.html') #User has already submitted, so takes to response page FANG UNCOMMENT THIS FOR COOKIE TESTING
        return render_template('storyInput.html', lastEntry = "Whatever last entry is") #returns story page with userID stored
    else:
        print("wrong password")
        return render_template('login.html', error = "Wrong Password") #calls the HTML file with the error
        

@app.route("/signUp")
def signUp(): #this code will change the HTML template from login.html to signUp.html
    return render_template( 'signup.html' )

@app.route("/register", methods=['POST'])
def register():
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
    command = (f"INSERT INTO login VALUES(NULL, \"{username}\", \"{pass1}\", 0)") #the \"\"
    c.execute(command)
    print(c.execute('select * from login').fetchall())
    db.commit() #commit to update the db
    return render_template('login.html')

@app.route("/logout", methods=['POST'])
def logout():
    #session.pop('userID', None) FANG UNCOMMENT THIS TO CHECK!!!
    return render_template('login.html')

@app.route("/addedStory", methods=['POST'])
def addedStory():
    # add entry into the main story
    newEntry = request.form['newEntry']
    command = (f"INSERT INTO entries VALUES(\"session['userID']\", \"{newEntry}\")")
    c.execute(command)
    #c.execute('UPDATE login SET submitted = 1 WHERE userID = {{userID}}') #uncomment for cookies FANG
    db.commit()
    storyText = updateStory()
    return render_template('addedStory.html', story=storyText)

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()

db.commit()
db.close()  #close database
