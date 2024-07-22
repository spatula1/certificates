from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory
import os
import sys

# Import the progress report script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'makeDocs')))
from makeDocs.progressReport import generate_progress_reports

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

@views.route('/hehe')
def home2():
    return "heheheh"

@views.route('/return-to-home')
def goHome():
    return redirect(url_for('views.home'))

@views.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

#download file (progress report)
@views.route('/download/<filename>')
def download_file(filename):
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'toPrint')
    return send_from_directory(directory, filename, as_attachment=True)

#upload and process progress report
@views.route('/upload-progress-report', methods=['POST'])
def upload_progress_report():
    lane_chart = request.files['laneChart']
    roster = request.files['roster']
    date = request.form['date']

    if lane_chart and roster and date:
        uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)

        lane_chart_path = os.path.join(uploads_dir, lane_chart.filename)
        roster_path = os.path.join(uploads_dir, roster.filename)

        lane_chart.save(lane_chart_path)
        roster.save(roster_path)

        # Call the function to generate the progress report
        output_pdf_path = os.path.join(uploads_dir, 'progressToPrint.pdf')
        generate_progress_reports(lane_chart_path, roster_path, date)

        # Redirect to the download route
        return redirect(url_for('views.download_file', filename='progressToPrint.pdf'))
    else:
        return "Please upload both files and select a date", 400
