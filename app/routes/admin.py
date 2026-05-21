from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Course
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            return redirect(url_for('user.dashboard'))
        return f(*args, **kwargs)
    return decorated

@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    courses = Course.query.all()
    return render_template('admin/dashboard.html', users=users, courses=courses)

@admin.route('/admin/courses/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_course():
    if request.method == 'POST':
        course = Course(
            title=request.form['title'],
            description=request.form['description'],
            instructor=request.form['instructor']
        )
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_course.html')

@admin.route('/admin/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_course(id):
    course = Course.query.get_or_404(id)
    if request.method == 'POST':
        course.title = request.form['title']
        course.description = request.form['description']
        course.instructor = request.form['instructor']
        db.session.commit()
        flash('Course updated!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_course.html', course=course)

@admin.route('/admin/courses/delete/<int:id>')
@login_required
@admin_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted!', 'success')
    return redirect(url_for('admin.dashboard'))