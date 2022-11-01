# Bottlers (Jeff Chen, Yusha Aziz, Fang Chen)
# SoftDev
# P00
# 2022-11-01

from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object

@app.route("/")
def loginpage():
    return render_template( 'login.html' )

@app.route("/signup")
def newplayer():
    return render_template( 'signup.html' )

@app.route("/auth")
def addlinepage():
    return render_template( 'play.html' )

@app.route("/success")
def storypage():
    return render_template( 'story.html' )

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
