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
    return jsonify(db.execute("SELECT * FROM pickup").fetchall())

#add a new pick-up
@bp.route('/pickups', methods=['POST'])
def index3():
    error = None
    if (request.method == 'POST'):
            
        db = get_db()

        db.execute("INSERT INTO pickup VALUES (NULL,?,?,?,?,?,?,?)", 
        (int(request.form['truckID']), 
        request.form['notes'], 
        request.form['type'],
        float(request.form['startLat']),
        float(request.form['startLog']),
        float(request.form['endLog']),
        float(request.form['endLat'] )
        ))

        db.commit()
    
        return jsonify ({'status' : 'success'})
    else:
        return jsonify({'status' : 'failed'})


@bp.route('/pickups/<int:id>', methods=['GET'])
def index4(id):
    db = get_db()
    
    numEntries = int(db.execute("SELECT COUNT(*) FROM pickup").fetchone()['COUNT(*)'])
    if (id > numEntries):
        return jsonify ({'status': 'failed'})
    else:
        return jsonify(db.execute("SELECT * FROM pickup WHERE id=" + str(id)).fetchall())



@bp.route('/fahrten')
def index():
    pass
