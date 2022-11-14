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

def getStory(story): #returns string story with all story from database
    command = f'select * from {story}'
    list = c.execute(command).fetchall()
    storyText = ""
    for phrases in list:
        storyText = storyText + "\n" + phrases[1]
    return storyText

def lastEntry(story):
    command = f'select line from {story}'
    allEntries = c.execute(command)
    db.commit()
    #print(list(allEntries))
    entrylist= [row[0] for row in allEntries]
    print(entrylist)
    if len(entrylist) > 0:
        return entrylist[-1]
    else:
        return ""

def hasSubmitted(usrID, story): #returns if the user has already submitted
    command = f"select submitted from {story} where userID = {usrID}"
    submitted = c.execute(command)
    db.commit()
    if submitted == 1:
        return True
    return False

def storyList():
    command = 'select name from sqlite_master where type= "table"'
    c.execute(command)
    db.commit()
    stories=c.fetchall()
    storylist = [row[0] for row in stories] #converts list of tuples to list of strings
    print(storylist)
    storylist.remove("login") #removes the login table and the default table
    storylist.remove("sqlite_sequence")
    print(storylist)
    return storylist

# CREATING login TABLE in logins.db
tbleName = "login"
parameters = "UserID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Password TEXT"
command = f"create table if not exists {tbleName} ({parameters})"
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
        return render_template('home.html', listOfStories = storyList())
    """
    if 'user' in session:
        # if hasSubmitted(session['user']):
        #     return render_template('addedStory.html', story = updateStory())
        # else
        #     story = updateStory()
        #     if len(story) == 0:
        #         return render_template('storyInput.html')
        #     else:
        #         return render_template('storyInput.html', line = lastEntry())
        return render_template('home.html')
    """
    return render_template('login.html')

@app.route("/home", methods=['POST'])
def home():
    session.pop('story')
    return render_template('home.html', listOfStories = storyList())

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
        return render_template('home.html', listOfStories = storyList())
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
    command = (f"INSERT INTO login VALUES(NULL, \"{username}\", \"{pass1}\")") #the \"\"
    c.execute(command)
    # print(c.execute('select * from login').fetchall()) # See new login table
    db.commit() #commit to update the db

    return render_template('login.html') # Return to login page

@app.route("/newStory", methods=['POST'])
def newStory():
    if 'story' in session:
        session.pop('story')
    newName = request.form['storyName']
    if request.form['storyName'] == "login":
        return render_template('home.html', error = "Invalid name! Choose something else!")
    session['story'] = newName
    parameters = "userID INT, line TEXT, submitted INT"
    command = f"create table if not exists {newName} ({parameters})"
    c.execute(command)
    db.commit()
    return render_template('storyInput.html', selectedStory = newName, line = "")   

@app.route("/selectStory", methods=['POST'])
def selectStory():
    if 'story' in session:
        session.pop('story')
    selStory = request.form['selStory']
    session['story'] = selStory
    if not hasSubmitted(session['user'], session['story']):
        return render_template('addedStory.html', story=getStory(session['story']))
    return render_template('storyInput.html', story = selStory, line = lastEntry(selStory))

@app.route("/addedStory", methods=['POST'])
def addedStory():
    #print(str(hasSubmitted(session['user'], session['story'])) + " submission test")
    if not (hasSubmitted(session['user'], session['story'])):
        print("adding and printing story...")
        # add entry into the main story
        story = session['story']
        command = (f"INSERT INTO {story} VALUES(\"{session['user']}\", \"{request.form['newEntry']}\", 1)")
        c.execute(command)
        db.commit()
    
    return render_template('addedStory.html', story=lastEntry(session['story']))
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
