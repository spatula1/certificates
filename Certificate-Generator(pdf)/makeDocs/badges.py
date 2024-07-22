import sys
import os
# Add the project_directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fitz 
import makeDocs.parseRoster as parseRoster

#get classes rosters
fullClasses = parseRoster.fullClasses
miniClasses = parseRoster.miniClasses

#VARIABLES
session = 'May/June'
template = "pdfImports/badgeTemplate.pdf"

badgeNum = 1
pageNum = 0
x = 0
y = 0

#open document
doc = fitz.open(template)
page = doc.load_page(0)

rotation = page.rotation #turns the text to face the right way

'''badge order
1 2
3 4
5 6
'''

#function to print info on badges
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
    #change font if name is too long 
    if len(string) > wordLen:
        fontSize = size
    else:
        fontSize = 25
    #print information on badge
    page.insert_text((x, y), string, fontSize, fontname="helv", rotate = rotation, overlay=True)

#prints names on badges
for aClass in fullClasses:
    className = aClass[0]
    day = aClass[1]
    time = aClass[2]
    for x in range(3):
        aClass.pop(0)
    for word in aClass:
        #name
        printInfo(560, 260, 177, 440, 706, word, 15, 20)

        #class
        printInfo(570, 262, 217, 480, 743, className, 9, 15)

        #day
        printInfo(430, 125, 217, 480, 743, day, 0, 20)

        #time
        printInfo(380, 74, 217, 480, 743, time, 0, 15)

        #change badge num
        if (badgeNum == 6):
            badgeNum = 1  
            pageNum += 2 
            #add new badge pages
            tempDoc = fitz.open(template)
            doc.insert_pdf(tempDoc)
            page = doc.load_page(pageNum)   
        else:
            badgeNum += 1
#save doc 
doc.save("toPrint/badgesToPrint.pdf")