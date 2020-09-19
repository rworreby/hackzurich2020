from flask import (
    Blueprint, request, jsonify
)
from app.firebase import get_firebase_db
import datetime

bp = Blueprint('api', __name__, url_prefix="/api")


@bp.route('/trucks', methods=['GET'])
def index_trucks():
    """
    curl -X GET \
    http://127.0.0.1:5000/api/trucks
    """
    db = get_firebase_db()
    trucks = db.child("trucks").get().val()
    return jsonify(trucks)


@bp.route('/trucks', methods=['POST'])
def create_trucks():
    """
    curl -X POST \
    -F 'truck_id=1' \
    -F 'userId=321' \
    -F 'currentLocationLon=10' \
    -F 'currentLocationLat=9' \
    -F 'homeLocationLon=10' \
    -F 'homeLocationLat=10' \
    -F 'payload=concret' \
    -F 'maxLoad=1' \
    -F 'angle=0' \
    http://127.0.0.1:5000/api/trucks
    """
    db = get_firebase_db()
    trucks = db.child("trucks").get().val()
    id = trucks[-1]['id'] + 1 if trucks else 0
    data = {
        "id": int(id),
        "userId": int(request.form['userId']),
        "currentLocationLon": float(request.form['currentLocationLon']),
        "currentLocationLat": float(request.form['currentLocationLat']),
        "homeLocationLon": float(request.form['homeLocationLon']),
        "homeLocationLat": float(request.form['homeLocationLat']),
        "createdAt": "2020-09-19-15-58-33", #str(datetime.datetime.now()),
        "payload": request.form['payload'],
        "maxLoad": int(request.form['maxLoad']),
        "angle": int(request.form['angle'])
    }
    db.child("trucks/" + str(id)).set(data)
    return jsonify([])


@bp.route('/trucks/<int:id>', methods=['GET'])
def show_trucks(id):
    """
    curl -X GET \
    http://127.0.0.1:5000/api/trucks/1
    """
    db = get_firebase_db()
    trucks = db.child("trucks").get().val()
    for truck in trucks:
        if truck['id'] == id:
            return jsonify(truck)
    return jsonify([])


@bp.route('/trucks/<int:id>', methods=['PUT'])
def update_trucks(id):
    """
    curl -X PUT \
    -F 'truck_id=1' \
    -F 'userId=321' \
    -F 'currentLocationLon=11' \
    -F 'currentLocationLat=11' \
    -F 'homeLocationLon=10' \
    -F 'homeLocationLat=10' \
    -F 'payload=concret' \
    -F 'maxLoad=1' \
    -F 'angle=0' \
    http://127.0.0.1:5000/api/trucks/1
    """
    db = get_firebase_db()
    data = {
        "id": int(id),
        "userId": int(request.form['userId']),
        "currentLocationLon": float(request.form['currentLocationLon']),
        "currentLocationLat": float(request.form['currentLocationLat']),
        "homeLocationLon": float(request.form['homeLocationLon']),
        "homeLocationLat": float(request.form['homeLocationLat']),
        "createdAt": "2020-09-19-15-58-33", #str(datetime.datetime.now()),
        "payload": request.form['payload'],
        "maxLoad": int(request.form['maxLoad']),
        "angle": int(request.form['angle'])
    }
    db.child("trucks/" + str(id)).update(data)
    return jsonify([])


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
