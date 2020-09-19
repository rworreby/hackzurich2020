from flask import (
    Blueprint, redirect, render_template
)

bp = Blueprint('main', __name__, url_prefix="")


@bp.route('/')
def index():
    return redirect('main')


@bp.route('/main', methods=['GET'])
def register():
    return render_template('main.html')
