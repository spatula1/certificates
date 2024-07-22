import sys
import os
# Add the project_directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fitz 
import makeDocs.parseRoster as parseRoster

#get class rosters
fullClasses = parseRoster.fullClasses
miniClasses = parseRoster.miniClasses

#VARIABLES
fullSession = 'May/June'
miniSession = "May Mini"
template = 'pdfImports/certificate.pdf'
fontSize = 25

doc = fitz.open()
temp = fitz.open(template)
pageNum = 0

#print for 8 week classes
for aClass in fullClasses:
    className = aClass[0]
    aClass.pop(1)
    aClass.pop(1)
    aClass.pop(0)
    for name in aClass:
        if pageNum%2 == 0: #insert new pdf
            doc.insert_pdf(temp)
        page = doc.load_page(pageNum)
        #print name, changes x coordinate based on length
        if len(name) < 9: 
            page.insert_text((260, 198), name, fontsize = 25, fontname="helv", overlay=True)
        elif len(name) < 13:
            page.insert_text((235, 198), name, fontsize = 25, fontname="helv", overlay=True)
        elif len(name) < 16:
            page.insert_text((220, 198), name, fontsize = 25, fontname="helv", overlay=True)
        elif len(name) < 20:
            page.insert_text((210, 198), name, fontsize = 25, fontname="helv", overlay=True)
        elif len(name) < 24:
            page.insert_text((175, 198), name, fontsize = 25, fontname="helv", overlay=True)
        else:
            page.insert_text((145, 198), name, fontsize = 25, fontname="helv", overlay=True)
        pageNum += 1
        #print session
        page.insert_text((180, 235), fullSession, fontsize = 20, fontname="helv", overlay=True)
        #print class name
        if len(className) < 9:
            page.insert_text((370, 235), className, fontsize = 20, fontname="helv", overlay=True)
        elif len(className) < 13:
            page.insert_text((360, 235), className, fontsize = 19, fontname="helv", overlay=True)
        elif len(className) < 15:
            page.insert_text((360, 235), className, fontsize = 15, fontname="helv", overlay=True)
        else:
            page.insert_text((360, 235), className, fontsize = 13, fontname="helv", overlay=True)
        
doc.save("toPrint/certificatesToPrint.pdf")