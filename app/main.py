
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('main', __name__, url_prefix="")

@bp.route('/main', methods=['GET'])
def register():
    return render_template('main.html')