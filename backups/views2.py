from flask import Blueprint, render_template, redirect, url_for, request
import os

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/badges')
def badges():
    return render_template('badges.html')

@views.route('/certificates')
def certificates():
    return render_template('certificates.html')

@views.route('/progress-reports')
def progressReports():
    return render_template('progressReports.html')


@views.route('/return-to-home')
def goHome():
    return redirect(url_for('views.home'))


@views.route('/upload', methods=['POST'])
def upload():
    lane_chart = request.files['laneChart']
    roster = request.files['roster']
    date = request.form['date']

    if lane_chart and roster and date:
        lane_chart.save(os.path.join('uploads', lane_chart.filename))
        roster.save(os.path.join('uploads', roster.filename))
        # Process the files and date as needed
        return redirect(url_for('views.progressReports'))
    else:
        return "Please upload both files and select a date", 400


