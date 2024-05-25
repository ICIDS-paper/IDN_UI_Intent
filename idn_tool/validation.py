import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('validation', __name__, url_prefix='/validation')

@bp.route('/test_the_narrative', methods=('GET', 'POST'))
def test_the_narrative():
    return render_template("validation/test_the_narrative.html", title="Test the Narrative")