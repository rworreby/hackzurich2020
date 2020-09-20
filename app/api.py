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
    -F 'userId=321' \
    -F 'currentLocationLon=9' \
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
        "createdAt": str(datetime.datetime.now()),
        "payload": request.form['payload'],
        "maxLoad": int(request.form['maxLoad']),
        "angle": int(request.form['angle']),
        "route": str(request.form['route'])
    }
    truck = db.child("trucks/" + str(len(trucks) if trucks else 0)).set(data)
    return jsonify(truck)


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
        "angle": int(request.form['angle']),
        "route": str(request.form['route'])
    }
    db.child("trucks/" + str(id)).update(data)

    # If at goal?
    # check for new pick ups and get it

    # if at pick up location -> delete pick up

    return jsonify([])

@bp.route('/trucks', methods=['DELETE'])
def delete_all_trucks():
    """
    curl -X DELETE \
    http://127.0.0.1:5000/api/trucks
    """
    db = get_firebase_db()
    trucks = db.child("trucks").remove()
    return jsonify(trucks)


@bp.route('/fahrten', methods=['GET'])
def index_fahrten():
    """
    curl -X GET \
    http://127.0.0.1:5000/api/fahrten
    """
    db = get_firebase_db()
    fahrten = db.child("fahrten").get().val()
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
    db = get_firebase_db()
    fahrten = db.child("fahrten").get().val()
    id = fahrten[-1]['id'] + 1 if fahrten else 0
    data = {
        "id": int(id),
        "truck_id": request.form['truck_id'],
        "load": request.form['load'],
        "start_location_log": float(request.form['start_location_log']),
        "start_location_lat": float(request.form['start_location_lat']),
        "end_location_log": float(request.form['end_location_log']),
        "end_location_lat": float(request.form['end_location_lat'])
    }
    db.child("fahrten/" + str(len(fahrten))).set(data)
    return jsonify([])


@bp.route('/fahrten/<int:id>', methods=['GET'])
def show_fahrten(id):
    """
    curl -X GET \
    http://127.0.0.1:5000/api/fahrten/1
    """
    db = get_firebase_db()
    fahrten = db.child("fahrten").get().val()
    for fahrt in fahrten:
        if fahrt['id'] == id:
            return jsonify(fahrt)
    return jsonify([])


@bp.route('/facilities', methods=['GET'])
def index_facilities():
    """
    curl -X GET \
    http://127.0.0.1:5000/api/facilities
    """
    db = get_firebase_db()
    facilities = db.child("facilities").get().val()
    return jsonify(facilities)


#get all pick-ups
@bp.route('/pickups', methods=['GET'])
def index_pickups():
    """
    curl -X GET \
    http://127.0.0.1:5000/api/pickups
    """
    db = get_firebase_db()
    pickups = db.child("pickups").get().val()
    return jsonify(pickups)


#add a new pick-up
@bp.route('/pickups', methods=['POST'])
def create_pickup():
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
    http://127.0.0.1:5000/api/pickups
    """
    db = get_firebase_db()
    pickups = db.child("pickups").get().val()
    id = pickups[-1]['id'] + 1 if pickups else 0
    data = {
        "id": int(id),
        "notes": request.form.get('notes'),
        "type": request.form['type'],
        "locationLog": float(request.form['longitude']),
        "locationLat": float(request.form['latitude']),
        "payload": int(request.form['amount'])
    }
    db.child("pickups/" + str(len(pickups))).set(data)
    return jsonify([])


@bp.route('/pickups/<int:id>', methods=['GET'])
def show_pickups(id):
    """
    curl -X GET \
    http://127.0.0.1:5000/api/pickups/1
    """
    db = get_firebase_db()
    pickups = db.child("pickups").get().val()
    for pickup in pickups:
        if pickup['id'] == id:
            return jsonify([pickup])
    return jsonify([])

