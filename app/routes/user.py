from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Course

user = Blueprint('user', __name__)

@user.route('/dashboard')
@login_required
def dashboard():
    courses = Course.query.all()
    return render_template('dashboard.html', courses=courses)