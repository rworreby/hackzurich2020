from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix="/api")


@bp.route('/fahrten', methods=['GET'])
def index_fahrten():
    db = get_db()
    fahrten = db.execute(
        'SELECT * FROM fahrt ORDER BY id'
    ).fetchall()
    return jsonify(fahrten)


@bp.route('/fahrten', methods=['POST'])
def create_fahrten():
    """
    curl -X POST \
    -F 'truck_id=1' \
    -F 'load=1000' \
    -F 'start_location_log=9.823311' \
    -F 'start_location_lat=10.305816' \
    -F 'end_location_log=9.773050' \
    -F 'end_location_lat=10.256395' \
    http://127.0.0.1:5000/api/fahrten
    """
    db = get_db()
    db.execute(
        'INSERT INTO fahrt VALUES (NULL, ?, ?, ?, ?, ?, ?)',
        (
            request.form['truck_id'],
            request.form['load'],
            request.form['start_location_log'],
            request.form['start_location_lat'],
            request.form['end_location_log'],
            request.form['end_location_lat']
        )
    )
    db.commit()
    return


@bp.route('/fahrten/<int:id>', methods=['GET'])
def show_fahrten(id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM fahrt ORDER BY id'
    ).fetchone()
    return jsonify(post)


@bp.route('/facilities', methods=['GET'])
def index_facilities():
    return jsonify([])


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
