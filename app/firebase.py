import pyrebase

def get_firebase_db():
    config = {
        "apiKey": "AIzaSyBrG-rUgJzi2NNKQKHD4LsWQgr0USIbBdM",
        "authDomain": "hackzurich-b6eb5.firebaseapp.com",
        "databaseURL": "https://hackzurich-b6eb5.firebaseio.com",
        "storageBucket": "hackzurich-b6eb5.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    return firebase.database()