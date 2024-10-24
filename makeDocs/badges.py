import sys
import os
import fitz
import io
import boto3
from flask import Flask, render_template, request, jsonify
from botocore.exceptions import NoCredentialsError, ClientError

# Add the project_directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from makeDocs.parseRoster import load_roster

app = Flask(__name__)

# Initialize the S3 client
s3 = boto3.client('s3', region_name='us-east-2', config=boto3.session.Config(signature_version='s3v4'))
BUCKET_NAME = 'tspc-certificates'

# Function to upload file to AWS s3
def upload_to_s3(file_stream, file_name, bucket_name):
    try:
        s3.upload_fileobj(file_stream, bucket_name, file_name)
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except ClientError as e:
        # Print error message to console for debugging
        print(f"Error occurred: {e}")
        return False
    
def generate_presigned_url(bucket_name, file_name, expiration=3600):
    try:
        response = s3.generate_presigned_url('get_object',
                                             Params={'Bucket': bucket_name,
                                                     'Key': file_name},
                                             ExpiresIn=expiration)
        return response
    except ClientError as e:
        print(f"Error occurred: {e}")
        return None
    
# Generate mini class badges
def generate_mini_badges(roster_stream, badge_template_stream):
    
    # Prepare to create the output PDF
    output_pdf_stream = io.BytesIO()

    # Get class rosters
    fullClasses, miniClasses = load_roster(roster_stream)
    badgeNum = 1
    pageNum = 0
    
    # Convert BytesIO stream to bytes
    badge_template_bytes = badge_template_stream.getvalue()

    # Open document
    output_pdf = fitz.open(stream=badge_template_bytes, filetype="pdf")
    page = output_pdf.load_page(0)
    rotation = page.rotation  # Turns the text to face the right way

    '''badge order
    1 2
    3 4
    5 6
    '''

    # Function to print info on badges
    def printInfo(y1: int, y2: int, x1: int, x2: int, x3: int, string: str, wordLen: int, size: int):
        if badgeNum in [1, 3, 5]:
            y = y1
        else:
            y = y2
        if badgeNum in [1, 2]:
            x = x1
        elif badgeNum in [3, 4]:
            x = x2
        else:
            x = x3
        # Change font if name is too long 
        if len(string) > wordLen:
            fontSize = size
        else:
            fontSize = 25

        if string == "LK Adv Skating Skills 8U" or string == "LK Adv Skating Skills 14U":
            fontSize = 12

        if string == "Thurs":
            fontSize = 14
        # Print information on badge
        page.insert_text((x, y), string, fontSize, fontname="helv", rotate=rotation, overlay=True)

    # Prints names on badges
    for aClass in miniClasses:
        className = aClass[0]
        day = aClass[1]
        time = aClass[2]
        for x in range(3):
            aClass.pop(0)
        for word in aClass:
            # Name
            printInfo(560, 260, 177, 440, 706, word, 15, 20)

            # Class
            printInfo(570, 262, 217, 480, 743, className, 9, 15)

            # Day
            printInfo(430, 125, 217, 480, 743, day, 0, 20)

            # Time
            printInfo(380, 74, 217, 480, 743, time, 0, 15)

            # Change badge num
            if badgeNum == 6:
                badgeNum = 1  
                pageNum += 2 
                # Add new badge pages
                tempDoc = fitz.open(badge_template_stream)
                output_pdf.insert_pdf(tempDoc)
                page = output_pdf.load_page(pageNum)   
            else:
                badgeNum += 1
    
    # Save the output PDF to the stream
    output_pdf.save(output_pdf_stream)
    output_pdf_stream.seek(0)  # Reset the stream position to the beginning

    return output_pdf_stream

#generate full class badges
def generate_full_badges(roster_stream, badge_template_stream):
    # Prepare to create the output PDF
    output_pdf_stream = io.BytesIO()

    # Get class rosters
    fullClasses, miniClasses = load_roster(roster_stream)
    badgeNum = 1
    pageNum = 0

    # Convert BytesIO stream to bytes
    badge_template_bytes = badge_template_stream.getvalue()

    # Open document
    output_pdf = fitz.open(stream=badge_template_bytes, filetype="pdf")
    page = output_pdf.load_page(0)
    rotation = page.rotation  # Turns the text to face the right way

    '''badge order
    1 2
    3 4
    5 6
    '''

    # Function to print info on badges
    def printInfo(y1: int, y2: int, x1: int, x2: int, x3: int, string: str, wordLen: int, size: int):
        if badgeNum in [1, 3, 5]:
            y = y1
        else:
            y = y2
        if badgeNum in [1, 2]:
            x = x1
        elif badgeNum in [3, 4]:
            x = x2
        else:
            x = x3
        # Change font if name is too long 
        if len(string) > wordLen:
            fontSize = size
        else:
            fontSize = 25

        if string == "LK Adv Skating Skills 8U" or string == "LK Adv Skating Skills 14U":
            fontSize = 12

        if string == "Thurs":
            fontSize = 14
        # Print information on badge
        page.insert_text((x, y), string, fontSize, fontname="helv", rotate=rotation, overlay=True)

    # Prints names on badges
    for aClass in fullClasses:
        className = aClass[0]
        day = aClass[1]
        time = aClass[2]
        for x in range(3):
            aClass.pop(0)
        for word in aClass:
            # Name
            printInfo(560, 260, 177, 440, 706, word, 15, 20)

            # Class
            printInfo(570, 262, 217, 480, 743, className, 9, 15)

            # Day
            printInfo(430, 125, 217, 480, 743, day, 0, 20)

            # Time
            printInfo(380, 74, 217, 480, 743, time, 0, 15)

            # Change badge num
            if badgeNum == 6:
                badgeNum = 1  
                pageNum += 2 
                # Add new badge pages
                tempDoc = fitz.open(stream=badge_template_bytes, filetype="pdf")
                output_pdf.insert_pdf(tempDoc)
                page = output_pdf.load_page(pageNum)
            else:
                badgeNum += 1

    # Save the output PDF to the stream
    output_pdf.save(output_pdf_stream)
    output_pdf_stream.seek(0)  # Reset the stream position to the beginning

    return output_pdf_stream
