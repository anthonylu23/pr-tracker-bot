import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from config import *

def addNewUser(user, server): #creates a new user under server in database
    ref = db.reference(f"/")
    servRef = ref.child(server)
    servRef.update({
        user : {}
    })

def createServer(server): #creates a new server in database
    ref = db.reference(f"/")
    ref.update({
            server : {}
        })
    
def update_total(user, server):
    ref = db.reference(f"/")
    servRef = ref.child(server)
    userRef = servRef.child(user)
    total = 0
    if "bench" in userRef.get():
        childRef = userRef.child("bench")
        child = childRef.get()
        res = child["latest"]
        total += int(res)
    if "squat" in userRef.get():
        childRef = userRef.child("bench")
        child = childRef.get()
        res = child["latest"]
        total += int(res)
    if "deadlift" in userRef.get():
        childRef = userRef.child("deadlift")
        child = childRef.get()
        res = child["latest"]
        total += int(res)
    servRef = ref.child(server)
    userRef.update({
        "total" : str(total)
    })

def getMax(user, server_id, lift):
    ref = db.reference(f"/")
    serverRef = ref.child(str(server_id))
    userRef = serverRef.child(str(user))
    liftRef = userRef.child(lift)
    liftGet = liftRef.get()
    return liftGet["latest"]