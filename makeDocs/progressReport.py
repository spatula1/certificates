import io
import re
import fitz
import sys
import os
# Add the project_directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from makeDocs import parseRoster as parseRoster
import makeDocs.parseLaneChart as parseLaneChart

def generate_progress_reports(lane_chart_stream, roster_stream, date):
    # Load the roster and lane chart data from in-memory streams
    fullClasses = parseRoster.load_progress_roster(io.BytesIO(roster_stream.read()))
    coachRoster = parseLaneChart.load_lane_chart(io.BytesIO(lane_chart_stream.read()))

    # Initialize in-memory PDF documents
    temp_pdf_stream = io.BytesIO()
    temp_pdf = fitz.open(stream=temp_pdf_stream)

    # Assuming you have a PDF template in-memory for use
    # If not, you need to load it into memory or adapt this part
    template_pdf_path = 'path_to_your_template/progressReport.pdf'
    with open(template_pdf_path, 'rb') as f:
        temp_pdf_stream.write(f.read())
    temp_pdf_stream.seek(0)
    temp_pdf = fitz.open(stream=temp_pdf_stream)

    # Create a new in-memory PDF document
    doc = fitz.open()

    # Clean up empty classes
    fullClasses = [aClass for aClass in fullClasses if len(aClass) >= 4]

    def cleanString(s):
        return re.sub(r'[^A-Za-z0-9]', '', s).upper()

    # VARIABLES
    currentPage = 0
    pageToInsert = 0
    side = 1  # which side to print on
    index = 0
    laneChartIndex = 0

    for aClass in fullClasses:
        className = aClass[0]

        for coachClass in coachRoster:
            if cleanString(coachClass[1]) == cleanString(className.upper()):
                coach = coachClass[0]
                coachRoster.remove(coachClass)
                break

        if len(coach) < 12:
            coachSize = 17
        elif len(coach) < 16:
            coachSize = 14
        elif len(coach) < 19:
            coachSize = 12
        else:
            coachSize = 10

        del aClass[1:3]  # remove class time and day

        if className in ["Lions & Cubs", "Snowplow Sam 1", "Snowplow Sam 2"]:
            pageToInsert = 0
            x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 85, 60, 300, 480, 690, 134, 150, 150, 555, 137, 153, 152.5, 558
        elif className in ["Snowplow Sam 3", "Snowplow Sam 4"]:
            pageToInsert = 1
            x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 100, 60, 305, 485, 700, 134, 150, 150, 555, 133, 150, 150, 555
        # (Other class-to-page mappings are similar to above)
        # Add the rest of your class-to-page mappings here...

        if index == 0:
            previousPageToInsert = pageToInsert
            index = 1

        for name in aClass[1:]:
            if pageToInsert != 10:
                if side == 1:
                    doc.insert_pdf(temp_pdf, from_page=pageToInsert, to_page=pageToInsert)
                    page = doc.load_page(currentPage)
                    page.insert_text((x1, y1), name, fontsize=25, fontname="helv", overlay=True)
                    page.insert_text((x2, y2), className, fontsize=17, fontname="helv", overlay=True)
                    page.insert_text((x3, y3), date, fontsize=17, fontname="helv", overlay=True)
                    page.insert_text((220, y4), coach, fontsize=coachSize, fontname="helv", overlay=True)
                    side = 2
                else:
                    if previousPageToInsert == pageToInsert:
                        page.insert_text((x5, y5), name, fontsize=25, fontname="helv", overlay=True)
                        page.insert_text((450, y6), className, fontsize=17, fontname="helv", overlay=True)
                        page.insert_text((x7, y7), date, fontsize=17, fontname="helv", overlay=True)
                        page.insert_text((620, y8), coach, fontsize=coachSize, fontname="helv", overlay=True)
                        side = 1
                        currentPage += 1
                    else:
                        currentPage += 1
                        doc.insert_pdf(temp_pdf, from_page=pageToInsert, to_page=pageToInsert)
                        page = doc.load_page(currentPage)
                        page.insert_text((x1, y1), name, fontsize=25, fontname="helv", overlay=True)
                        page.insert_text((x2, y2), className, fontsize=17, fontname="helv", overlay=True)
                        page.insert_text((x3, y3), date, fontsize=17, fontname="helv", overlay=True)
                        page.insert_text((220, y4), coach, fontsize=coachSize, fontname="helv", overlay=True)
                        side = 2
                previousPageToInsert = pageToInsert
            else:
                if className == "Spin Comp 1" or className == "Spin Comp 2":
                    currentPage += 1
                    doc.insert_pdf(temp_pdf, from_page=pageToInsert, to_page=pageToInsert)
                    page = doc.load_page(currentPage)
                    page.insert_text((x1, y1), name, fontsize=25, fontname="helv", overlay=True)
                    page.insert_text((x2, y2), className, fontsize=17, fontname="helv", overlay=True)
                    page.insert_text((x3, y3), date, fontsize=17, fontname="helv", overlay=True)
                    page.insert_text((220, y4), coach, fontsize=coachSize, fontname="helv", overlay=True)
                    side = 1
                else:
                    doc.insert_pdf(temp_pdf, from_page=pageToInsert, to_page=pageToInsert)
                    page = doc.load_page(currentPage)
                    page.insert_text((x5, y5), name, fontsize=25, fontname="helv", overlay=True)
                    page.insert_text((450, y6), className, fontsize=17, fontname="helv", overlay=True)
                    page.insert_text((x7, y7), date, fontsize=17, fontname="helv", overlay=True)
                    page.insert_text((620, y8), coach, fontsize=coachSize, fontname="helv", overlay=True)
                    side = 1
                    currentPage += 1

    if doc.page_count == 0:
        raise ValueError("The document has zero pages after processing.")

    output_pdf_stream = io.BytesIO()
    doc.save(output_pdf_stream)
    output_pdf_stream.seek(0)

    return output_pdf_stream
