from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
from flask import jsonify

bp = Blueprint('api', __name__, url_prefix="/api")


#get all pick-ups
@bp.route('/pickups', methods=['GET'])
def index2():
    db = get_db()
    return jsonify(db.executescript("SELECT * FROM pickup").fetchall())

#add a new pick-up
@bp.route('/pickups', methods=['POST'])
def index3():
    error = None
    if (request.method == 'POST'):
        driverID = request.form['driverID']
    
    db = get_db()

    db.execute("INSERT INTO pickup VALUES (NULL,?,?,?,?,?,?,?)", (32, 'notes', 'type', 4.3, 2.1, 2.1, 1.5))
    db.commit()
    
    return "Add a new pick-up with ID " + str(driverID)


    




@bp.route('/fahrten')
def index():
    pass
