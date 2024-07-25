import fitz  # PyMuPDF
import io
import sys
import os
from flask import Response
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from makeDocs.parseRoster import load_roster

#generate mini certificates
def generate_mini_certificates(roster_stream, mini_class_session):

    # Prepare to create the output PDF
    output_pdf_stream = io.BytesIO()

    fullClasses, miniClasses = load_roster(roster_stream)#get class rosters
    temp = fitz.open('pdfImports/certificate.pdf') #open certificate template
    output_pdf = fitz.open()  # Create an empty PDF
    page_num = 0
    print(miniClasses)

    #generate certificates
    for class_data in miniClasses:
        class_name = class_data[0]
        class_data.pop(1)
        class_data.pop(1)
        class_data.pop(0)

        for name in class_data:
            if page_num % 2 == 0:  # Insert a new page every 2 certificates
                output_pdf.insert_pdf(temp)
            page = output_pdf.load_page(page_num)

            #print name, changes x coordinate based on length
            if len(name) < 9: 
                page.insert_text((260, 198), name, fontsize=25, fontname="helv", overlay=True)
            elif len(name) < 13:
                page.insert_text((235, 198), name, fontsize=25, fontname="helv", overlay=True)
            elif len(name) < 16:
                page.insert_text((220, 198), name, fontsize=25, fontname="helv", overlay=True)
            elif len(name) < 20:
                page.insert_text((210, 198), name, fontsize=25, fontname="helv", overlay=True)
            elif len(name) < 24:
                page.insert_text((175, 198), name, fontsize=25, fontname="helv", overlay=True)
            else:
                page.insert_text((145, 198), name, fontsize=25, fontname="helv", overlay=True)
            #print session
            page.insert_text((180, 235), mini_class_session, fontsize = 20, fontname="helv", overlay=True)
            
            #page.insert_text((180, 235), mini_class_session if session_type == 'mini' else full_class_session, fontsize=20, fontname="helv", overlay=True)
            #print class name
            if len(class_name) < 9:
                page.insert_text((370, 235), class_name, fontsize=20, fontname="helv", overlay=True)
            elif len(class_name) < 13:
                page.insert_text((360, 235), class_name, fontsize=19, fontname="helv", overlay=True)
            elif len(class_name) < 15:
                page.insert_text((360, 235), class_name, fontsize=15, fontname="helv", overlay=True)
            else:
                page.insert_text((360, 235), class_name, fontsize=13, fontname="helv", overlay=True)

            page_num += 1

    # Save the output PDF to the stream
    output_pdf.save(output_pdf_stream)
    output_pdf_stream.seek(0)  # Reset the stream position to the beginning

    return output_pdf_stream

#generate full certificates
def generate_full_certificates(roster_stream, full_class_session):
    # Load the roster PDF into a stream
    #roster_pdf = fitz.open(stream=roster_stream, filetype="pdf")

    # Prepare to create the output PDF
    output_pdf_stream = io.BytesIO()

    #get class rosters
    fullClasses, miniClasses = load_roster(roster_stream)

    temp = fitz.open('pdfImports/certificate.pdf') #open certificate template
    output_pdf = fitz.open()  # Create an empty PDF
    page_num = 0

    for class_data in fullClasses:
        class_name = class_data[0]
        class_data.pop(1)
        class_data.pop(1)
        class_data.pop(0)

        for name in class_data:
            if page_num % 2 == 0:  # Insert a new page every 2 certificates
                output_pdf.insert_pdf(temp)
            page = output_pdf.load_page(page_num)

            #print name, changes x coordinate based on length
            if len(name) < 9: 
                page.insert_text((260, 198), name, fontsize=25, fontname="helv", overlay=True)
            elif len(name) < 13:
                page.insert_text((235, 198), name, fontsize=25, fontname="helv", overlay=True)
            elif len(name) < 16:
                page.insert_text((220, 198), name, fontsize=25, fontname="helv", overlay=True)
            elif len(name) < 20:
                page.insert_text((210, 198), name, fontsize=25, fontname="helv", overlay=True)
            elif len(name) < 24:
                page.insert_text((175, 198), name, fontsize=25, fontname="helv", overlay=True)
            else:
                page.insert_text((145, 198), name, fontsize=25, fontname="helv", overlay=True)
            #print session
            page.insert_text((180, 235), full_class_session, fontsize = 20, fontname="helv", overlay=True)
            
            #page.insert_text((180, 235), mini_class_session if session_type == 'mini' else full_class_session, fontsize=20, fontname="helv", overlay=True)
            #print class name
            if len(class_name) < 9:
                page.insert_text((370, 235), class_name, fontsize=20, fontname="helv", overlay=True)
            elif len(class_name) < 13:
                page.insert_text((360, 235), class_name, fontsize=19, fontname="helv", overlay=True)
            elif len(class_name) < 15:
                page.insert_text((360, 235), class_name, fontsize=15, fontname="helv", overlay=True)
            else:
                page.insert_text((360, 235), class_name, fontsize=13, fontname="helv", overlay=True)

            page_num += 1

    # Save the output PDF to the stream
    output_pdf.save(output_pdf_stream)
    output_pdf_stream.seek(0)  # Reset the stream position to the beginning

    return output_pdf_stream

#generate both certificates
def generate_both_certificates(roster_stream, mini_class_session, full_class_session):

    def generate():
        fullClasses, miniClasses = load_roster(roster_stream)#get class rosters
        temp = fitz.open('pdfImports/certificate.pdf') #open certificate template
        output_pdf = fitz.open()  # Create an empty PDF
        page_num = 0

        #generate mini session certificates
        for class_data in miniClasses:
            class_name = class_data[0]
            class_data.pop(1)
            class_data.pop(1)
            class_data.pop(0)

            for name in class_data:
                if page_num % 2 == 0:  # Insert a new page every 2 certificates
                    output_pdf.insert_pdf(temp)
                page = output_pdf.load_page(page_num)

                #print mini session
                #print name, changes x coordinate based on length
                if len(name) < 9: 
                    page.insert_text((260, 198), name, fontsize=25, fontname="helv", overlay=True)
                elif len(name) < 13:
                    page.insert_text((235, 198), name, fontsize=25, fontname="helv", overlay=True)
                elif len(name) < 16:
                    page.insert_text((220, 198), name, fontsize=25, fontname="helv", overlay=True)
                elif len(name) < 20:
                    page.insert_text((210, 198), name, fontsize=25, fontname="helv", overlay=True)
                elif len(name) < 24:
                    page.insert_text((175, 198), name, fontsize=25, fontname="helv", overlay=True)
                else:
                    page.insert_text((145, 198), name, fontsize=25, fontname="helv", overlay=True)
                #print session
                page.insert_text((180, 235), mini_class_session, fontsize = 20, fontname="helv", overlay=True)
                #print class name
                if len(class_name) < 9:
                    page.insert_text((370, 235), class_name, fontsize=20, fontname="helv", overlay=True)
                elif len(class_name) < 13:
                    page.insert_text((360, 235), class_name, fontsize=19, fontname="helv", overlay=True)
                elif len(class_name) < 15:
                    page.insert_text((360, 235), class_name, fontsize=15, fontname="helv", overlay=True)
                else:
                    page.insert_text((360, 235), class_name, fontsize=13, fontname="helv", overlay=True)

                page_num += 1
            
        for class_data in fullClasses:
            class_name = class_data[0]
            class_data.pop(1)
            class_data.pop(1)
            class_data.pop(0)

            for name in class_data:
                if page_num % 2 == 0:  # Insert a new page every 2 certificates
                    output_pdf.insert_pdf(temp)
                page = output_pdf.load_page(page_num)

                #print mini session
                #print name, changes x coordinate based on length
                if len(name) < 9: 
                    page.insert_text((260, 198), name, fontsize=25, fontname="helv", overlay=True)
                elif len(name) < 13:
                    page.insert_text((235, 198), name, fontsize=25, fontname="helv", overlay=True)
                elif len(name) < 16:
                    page.insert_text((220, 198), name, fontsize=25, fontname="helv", overlay=True)
                elif len(name) < 20:
                    page.insert_text((210, 198), name, fontsize=25, fontname="helv", overlay=True)
                elif len(name) < 24:
                    page.insert_text((175, 198), name, fontsize=25, fontname="helv", overlay=True)
                else:
                    page.insert_text((145, 198), name, fontsize=25, fontname="helv", overlay=True)
                #print session
                page.insert_text((180, 235), full_class_session, fontsize = 20, fontname="helv", overlay=True)
                #print class name
                if len(class_name) < 9:
                    page.insert_text((370, 235), class_name, fontsize=20, fontname="helv", overlay=True)
                elif len(class_name) < 13:
                    page.insert_text((360, 235), class_name, fontsize=19, fontname="helv", overlay=True)
                elif len(class_name) < 15:
                    page.insert_text((360, 235), class_name, fontsize=15, fontname="helv", overlay=True)
                else:
                    page.insert_text((360, 235), class_name, fontsize=13, fontname="helv", overlay=True)

                page_num += 1

        # Save the PDF to the in-memory buffer
        output_pdf.save(pdf_buffer)
        pdf_buffer.seek(0)  # Reset the buffer position to the beginning

        # Yield the PDF in chunks
        chunk_size = 8192
        while chunk := pdf_buffer.read(chunk_size):
            yield chunk

    return Response(generate(), content_type='application/pdf')
