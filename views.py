from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, send_file, jsonify
import os
import sys
import io

# Import the progress report script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'makeDocs')))
from makeDocs.progressReport import generate_progress_reports
from makeDocs.certificate import generate_full_certificates, generate_mini_certificates, generate_both_certificates, upload_to_s3, generate_presigned_url, BUCKET_NAME

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
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    return send_from_directory(directory, filename, as_attachment=True)

#upload and process progress report
@views.route('/upload-progress-report', methods=['POST'])
def upload_progress_report():
    lane_chart = request.files.get('laneChart')
    roster = request.files.get('roster')
    date = request.form.get('date')

    if lane_chart and roster and date:
        # Read files into memory
        lane_chart_stream = io.BytesIO(lane_chart.read())
        roster_stream = io.BytesIO(roster.read())
        
        # Debugging: Print lengths to ensure they're not empty
        if lane_chart_stream.getvalue() == b'':
            return "Lane chart file is empty.", 400
        if roster_stream.getvalue() == b'':
            return "Roster file is empty.", 400
        
        try:
            output_pdf_stream = generate_progress_reports(lane_chart_stream, roster_stream, date)
            
            # Check if the PDF stream is empty
            if output_pdf_stream.getvalue() == b'':
                return "Generated PDF is empty.", 500
            
            # Return the PDF file as a downloadable response
            output_pdf_stream.seek(0)
            return send_file(
                output_pdf_stream,
                as_attachment=True,
                download_name='progressToPrint.pdf',
                mimetype='application/pdf'
            )
        except Exception as e:
            return f"An error occurred: {e}", 500
    else:
        return "Please upload both files and select a date", 400



#upload and process certificates
@views.route('/upload-mini-class', methods=['POST'])
def upload_mini_class():
    roster = request.files.get('roster')
    mini_class_session = request.form.get('miniClassSession')

    if roster and mini_class_session:
        roster_stream = io.BytesIO(roster.read())
        output_pdf_stream = generate_mini_certificates(roster_stream, mini_class_session)

        if output_pdf_stream.getvalue() == b'':
            return "Generated PDF is empty.", 500

        # Upload to S3
        file_name = 'mini_class_certificates.pdf'
        output_pdf_stream.seek(0)  # Ensure we are at the beginning of the stream
        success = upload_to_s3(output_pdf_stream, file_name, BUCKET_NAME)
        
        if not success:
            return "Failed to upload to S3.", 500

        # Generate presigned URL
        url = generate_presigned_url(BUCKET_NAME, file_name)
        if url is None:
            return "Failed to generate download link.", 500

        return render_template('download-certificate.html', url=url)
    else:
        return "Please upload the roster and provide a mini class session.", 400

@views.route('/upload-full-class', methods=['POST'])
def upload_full_class():
    roster = request.files.get('roster')
    full_class_session = request.form.get('fullClassSession')

    if roster and full_class_session:
        roster_stream = io.BytesIO(roster.read())
        output_pdf_stream = generate_full_certificates(roster_stream, full_class_session)

        if output_pdf_stream.getvalue() == b'':
            return "Generated PDF is empty.", 500

        # Upload to S3
        file_name = 'full_class_certificates.pdf'
        output_pdf_stream.seek(0)
        success = upload_to_s3(output_pdf_stream, file_name, BUCKET_NAME)
        
        if not success:
            return "Failed to upload to S3.", 500

        # Generate presigned URL
        url = generate_presigned_url(BUCKET_NAME, file_name)
        if url is None:
            return "Failed to generate download link.", 500

        return render_template('download-certificate.html', url=url)
    else:
        return "Please upload the roster and provide a full class session.", 400

@views.route('/upload-both-classes', methods=['POST'])
def upload_both_classes():
    roster = request.files.get('roster')
    mini_class_session = request.form.get('miniClassSession')
    full_class_session = request.form.get('fullClassSession')

    if roster and mini_class_session and full_class_session:
        roster_stream = io.BytesIO(roster.read())
        output_pdf_stream = generate_both_certificates(roster_stream, mini_class_session, full_class_session)

        if output_pdf_stream.getvalue() == b'':
            return jsonify({"error": "Generated PDF is empty."}), 500

        # Upload to S3
        file_name = 'both_classes_certificates.pdf'
        output_pdf_stream.seek(0)
        success = upload_to_s3(output_pdf_stream, file_name, BUCKET_NAME)
        
        if not success:
            return jsonify({"error": "Failed to upload to S3."}), 500

        # Generate presigned URL
        url = generate_presigned_url(BUCKET_NAME, file_name)
        if url is None:
            return jsonify({"error": "Failed to generate download link."}), 500

        return render_template('download-certificate.html', url=url)
    else:
        return jsonify({"error": "Please upload the roster and provide both class sessions."}), 400
        
