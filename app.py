# Bottlers (Jeff Chen, Yusha Aziz, Fang Chen)
# SoftDev
# P00
# 2022-11-01

from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object

@app.route("/")
def disp_loginpage():
    return render_template( 'login.html' )

@app.route("/auth")
def authenticate():
    return render_template( 'adding.html' )

    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
