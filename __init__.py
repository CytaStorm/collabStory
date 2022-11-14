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

def updateStory(): #returns string story with all story from database
    list = c.execute('select * from entries').fetchall()
    storyText = ""
    for phrases in list:
        storyText = storyText + "\n" + phrases[1]
    return storyText

def lastEntry():
    list = c.execute('select * from entries').fetchall()
    return list[-1][1]

def hasSubmitted(usrID): #returns if the user has already submitted
    command = f"select submitted from login where userID = {usrID}"
    submitted = c.execute(command)
    if submitted == 1:
        return True
    return False

# CREATING login TABLE in logins.db
tbleName = "login"
parameters = "UserID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Password TEXT, Submitted INTEGER"

command = (f"create table if not exists {tbleName} ({parameters})")
c.execute(command)
db.commit() #save changes

# #CREATING User entries TABLE in logins.db
# tbleName = "entries"
# parameters = "UserID INT, Line TEXT"

# """
# command = "drop table entries"
# c.execute(command)
# """

# command = (f"create table if not exists {tbleName} ({parameters})")
# c.execute(command)
# db.commit() #save changes

### FLASK ###
app = Flask(__name__)    #create Flask object
app.secret_key = b'ekifl@&n&!urniwer7[23[q894;8^'

@app.route("/")
def routing():
    print("routing...")
    
    if 'user' in session:
        # if hasSubmitted(session['user']):
        #     return render_template('addedStory.html', story = updateStory())
        # else:
        #     story = updateStory()
        #     if len(story) == 0:
        #         return render_template('storyInput.html')
        #     else:
        #         return render_template('storyInput.html', line = lastEntry())
        return render_template('home.html')
    return render_template('login.html')

@app.route("/auth", methods=['POST'])
def authenticate():
    print("authenticating...") #only accessible after LOGGING IN

    username = request.form['username']
    password = request.form['password']
    logList = c.execute('select * from login').fetchall()
    
    #Find if username exists in login database
    userExists = False
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
        print("Username is correct \n")
    
    #Username EXISTS; check if password matches
    if(password == combo[2]):
        print("password Works")
        session['user'] = combo[0] #Start a session with stored value of UserID
        #Render story page if the user already submitted an entry, otherwise render entry page
        if hasSubmitted(session['user']): 
            return render_template('addedStory.html', story = updateStory()) #User has already submitted, so takes to response page
        else:
            return render_template('storyInput.html', line = lastEntry())
    else:
        print("wrong password")
        return render_template('login.html', error = "Wrong Password") #calls the HTML file with the error
        
@app.route("/signUp")
def signUp(): #this code will change the HTML template from login.html to signUp.html
    print("signing up...")
    return render_template( 'signup.html' )

@app.route("/register", methods=['POST'])
def register():

    print("registering...") #only accessible after SIGNING UP
    username = request.form['username']
    pass1 = request.form['password1']
    pass2 = request.form['password2']

    logList = c.execute('select * from login').fetchall()
    # print(logList)

    for used in logList :
        # print(used[0])
        if username == used[1]:
            # print(used[1])
            return render_template('signup.html', error = "Username already exists") #redirects back to page with error
    if pass1 != pass2: 
        return render_template('signup.html', error ="Passwords Do Not Match Try Again!")
    
    #add newly created login information to table of all login
    command = (f"INSERT INTO login VALUES(NULL, \"{username}\", \"{pass1}\", 0)") #the \"\"
    c.execute(command)
    # print(c.execute('select * from login').fetchall()) # See new login table
    db.commit() #commit to update the db

    return render_template('login.html') # Return to login page

@app.route("/addedStory", methods=['POST'])
def addedStory():

    if not(hasSubmitted(session['user'])):
        print("adding and printing story...")
        # add entry into the main story
        newEntry = request.form['newEntry']
        command = (f"INSERT INTO entries VALUES(\"{session['user']}\", \"{newEntry}\")")
        c.execute(command)
        c.execute(f"UPDATE login SET submitted = 1 WHERE userID = {session['user']}") #Update submit status
        db.commit()
    
    return render_template('addedStory.html', story=updateStory())

@app.route("/logout", methods=['GET', 'POST'])
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
