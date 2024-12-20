import sys
import os
import re
# Add the project_directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fitz 
from makeDocs import parseRoster as parseRoster
import makeDocs.parseLaneChart as parseLaneChart

#get class roster
fullClasses = parseRoster.load_progress_roster("InstructorRosterV2.pdf")

#get coaches from lane chart
coachRoster = parseLaneChart.load_lane_chart('laneChart.pdf')


#print(fullClasses)
'''
page 0 - lions and cubs, ss1, ss2
page 1 - ss3, ss4
page 2 - basic 5, 6
page 3 - basic 1, 2, 3, 4
page 4 - prefree, free 1, 2
page 5 - freeskate 3, 4, 5, 6
page 6 - adult gold
page 7 - adult bronze, silver
page 8 - LK SS, Adv SS
page 9 - academy 1, 2
page 10 - spin comp 1 2 // intro to spin
page 11 - power
'''
doc = fitz.open()
temp = fitz.open("pdfImports/progressReport.pdf")

#removes blank classes
fullClasses = [aClass for aClass in fullClasses if len(aClass) >= 4]

#remove non alphanumeric characters
def cleanString(s):
    return re.sub(r'[^A-Za-z0-9]', '', s).upper()

#VARIABLES
date = "7/1/24"
currentPage = 0
pageToInsert = 0
side = 1 #which side to print on
index = 0
laneChartIndex = 0

#remove classes that dont need progress reports
for aClass in fullClasses:
    className = aClass[0] #get class name

    #get the coach name if the class matches 
    for coachClass in coachRoster:
        if cleanString(coachClass[1]) == cleanString(className.upper()):
            coach = coachClass[0]
            print(coachClass)
            print(coach)
            coachRoster.remove(coachClass)
            break

    #change coach text size depending on name length
    if len(coach)<12:
        coachSize = 17
    elif len(coach)< 16:
        coachSize = 14
    elif len(coach) < 19:
        coachSize = 12
    else:
        coachSize = 10

    del aClass[1:3] #remove class time and day
    
    #change page based on class
    if className in ["Lions & Cubs", "Snowplow Sam 1", "Snowplow Sam 2"]:
        pageToInsert = 0
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 85, 60, 300, 480, 690, 134, 150, 150, 555, 137, 153, 152.5, 558
    elif className in ["Snowplow Sam 3", "Snowplow Sam 4"]:
        pageToInsert = 1
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 100, 60, 305, 485, 700, 134, 150, 150, 555, 133, 150, 150, 555
    elif className in ["Basic 5", "Basic 6"]:
        pageToInsert = 2
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 100, 60, 300, 490, 700, 138, 154, 154, 560, 139, 154, 154, 560
    elif className in ["Basic 4", "Basic 3", "Basic 2", "Basic 1"]:
        pageToInsert = 3
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 100, 60, 300, 490, 700, 136, 152, 152, 570, 137, 152, 152, 570
    elif className in ["Pre-Freeskate", "Freeskate 1", "Freeskate 2"]:
        pageToInsert = 4
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 95, 60, 300, 490, 700, 134, 151, 151, 571, 134, 151, 151, 571
    elif className in ["Freeskate 3", "Freeskate 4", "Freeskate 5", "Freeskate 6"]:
        pageToInsert = 5
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 100, 60, 315, 490, 700, 131, 146, 146, 573, 134, 149, 149, 575
    elif className in ["Adult Gold"]:
        pageToInsert = 6
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 90, 60, 300, 480, 700, 135, 151, 151, 562, 138, 154, 154, 560
    elif className in ["Adult Bronze", "Adult Silver"]:
        pageToInsert = 7
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 90, 60, 300, 480, 700, 135, 151, 151, 562, 136, 151, 151, 560
    elif className in ["LK Skating Skills 8U", "LK Skating Skills 14U", "LK Adv Skating Skills 8U", "LK Adv Skating Skills 14U"]:
        pageToInsert = 8
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 90, 50, 300, 485, 700, 146, 170, 170, 562, 146, 170, 170, 560
    elif className in ["LK Academy 1 8U", "LK Academy 1 14U", "LK Academy 2 8U", "LK Academy 2 14U"]:
        pageToInsert = 9
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 90, 50, 300, 485, 700, 146, 170, 170, 562, 146, 170, 170, 560
    elif className in ["Spin Comp 1", "Spin Comp 2", "Intro To Spin"]:
        pageToInsert = 10
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 90, 50, 300, 485, 700, 146, 170, 170, 562, 146, 170, 170, 560
    elif className in ["Power 1", "Power 2"]:
        pageToInsert = 11
        x1, x2, x3, x5, x7, y1, y2, y3, y4, y5, y6, y7, y8 = 90, 50, 300, 485, 700, 146, 170, 170, 562, 146, 170, 170, 560
    if index == 0:
        previousPageToInsert = pageToInsert
        index = 1
    

    for name in aClass[1:]: #skip class name
        if pageToInsert != 10:
            if side == 1: #print on left side
               #insert new page 
               doc.insert_pdf(temp, from_page=pageToInsert, to_page=pageToInsert)
               ###############print("page added")##############
               page = doc.load_page(currentPage)
               page.insert_text((x1, y1), name, fontsize=25, fontname="helv", overlay=True)#print name
               page.insert_text((x2, y2), className, fontsize=17, fontname="helv", overlay=True)#print class
               page.insert_text((x3, y3), date, fontsize=17, fontname="helv", overlay=True)#print date
               page.insert_text((220, y4), coach, fontsize=coachSize, fontname="helv", overlay=True)#print instructor
               side = 2
            else: #print on right side
                if previousPageToInsert == pageToInsert: #print on side 2 if new class is on same page
                    page.insert_text((x5, y5), name, fontsize=25, fontname="helv", overlay=True)#print name
                    page.insert_text((450, y6), className, fontsize=17, fontname="helv", overlay=True)#print class
                    page.insert_text((x7, y7), date, fontsize=17, fontname="helv", overlay=True)#print date
                    page.insert_text((620, y8), coach, fontsize=coachSize, fontname="helv", overlay=True)#print instructor
                    side = 1
                    currentPage += 1
                else:
                    #set side to 1 
                    #insert new page
                    currentPage += 1
                    doc.insert_pdf(temp, from_page=pageToInsert, to_page=pageToInsert)
                    page = doc.load_page(currentPage)
                    page.insert_text((x1, y1), name, fontsize=25, fontname="helv", overlay=True)#print name
                    page.insert_text((x2, y2), className, fontsize=17, fontname="helv", overlay=True)#print class
                    page.insert_text((x3, y3), date, fontsize=17, fontname="helv", overlay=True)#print date
                    page.insert_text((220, y4), coach, fontsize=coachSize, fontname="helv", overlay=True)#print instructor
                    side = 2
            previousPageToInsert = pageToInsert
        else: #print on left side for spin comp
            if className == "Spin Comp 1" or className == "Spin Comp 2":
                currentPage += 1
                doc.insert_pdf(temp, from_page=pageToInsert, to_page=pageToInsert)
                page = doc.load_page(currentPage)
                page.insert_text((x1, y1), name, fontsize=25, fontname="helv", overlay=True)#print name
                page.insert_text((x2, y2), className, fontsize=17, fontname="helv", overlay=True)#print class
                page.insert_text((x3, y3), date, fontsize=17, fontname="helv", overlay=True)#print date
                page.insert_text((220, y4), coach, fontsize=coachSize, fontname="helv", overlay=True)#print instructor
                side = 1
            else: #print on right side for intro to spin
                doc.insert_pdf(temp, from_page=pageToInsert, to_page=pageToInsert)
                page = doc.load_page(currentPage)
                page.insert_text((x5, y5), name, fontsize=25, fontname="helv", overlay=True)#print name
                page.insert_text((450, y6), className, fontsize=17, fontname="helv", overlay=True)#print class
                page.insert_text((x7, y7), date, fontsize=17, fontname="helv", overlay=True)#print date
                page.insert_text((620, y8), coach, fontsize=coachSize, fontname="helv", overlay=True)#print instructor
                side = 1
                currentPage += 1
if doc.page_count == 0:
        raise ValueError("The document has zero pages after processing.")

doc.save("toPrint/progressToPrint.pdf")
