from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix="/api")


@bp.route('/fahrten', methods=['GET'])
def index():
    db = get_db()
    fahrten = db.execute(
        'SELECT * FROM fahrt ORDER BY id'
    ).fetchall()

    stuff = []

    for row in fahrten:
        jkl = []
        for col in row:
            jkl.append(col)
        stuff.append(jkl)


    print(stuff)
    return jsonify(stuff)

@bp.route('/fahrten', methods=['POST'])
def create():
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
def show(id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM fahrt ORDER BY id'
    ).fetchone()
    return str(id)

@bp.route('/facilities', methods=['GET'])
def index_facilities():
    return jsonify([])