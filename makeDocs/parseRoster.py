import PyPDF2
import re

#get text from pdf into a string
def extractTextFromPdf(pdfFile) -> str:
    if isinstance(pdfFile, str):
        with open(pdfFile, 'rb') as pdf:
            reader = PyPDF2.PdfReader(pdf, strict=False)
            pdfText = ''
            for page in reader.pages:
                content = page.extract_text()
                pdfText += (content)
    else:
        reader = PyPDF2.PdfReader(pdfFile, strict=False)
        pdfText = ''
        for page in reader.pages:
            content = page.extract_text()
            pdfText += (content)
    return pdfText

#remove words with specific characters
def removeWordsWithCharacter(string: str) -> str:
    lines = string.strip().split('\n')
    charactersToRemove = ["@", "/", "©", "yrs", "null"]
    processedLines = []

    for line in lines:
        words = line.split()
        filteredWords = []
        for word in words:
            if '-' in word and not word[0].isupper():
                continue  # Skip words with hyphens that are not capitalized (assumed not to be names)
            if any(char in word for char in charactersToRemove):
                continue  # Skip words with any other unwanted characters
            filteredWords.append(word)
        processedLines.append(' '.join(filteredWords))
    
    result = '\n'.join(processedLines)
    return result

#remove blank lines
def removeBlankLines(string: str) -> str:
    lines = string.split('\n')
    linesWithWords = [line for line in lines if line.strip() != '']
    result = '\n'.join(linesWithWords)
    return result

#removes a specific word 
def removeWord(line: str, word: str) -> str:
    pattern = fr'\b{word}\.?\b'
    result = re.sub(pattern, '', line, flags=re.IGNORECASE)
    result = re.sub(r'\s+', ' ', result).strip()
    return result

#removes the line if a word is found
def removeLineWithWord(string: str, word: str) -> str:
    lines = string.strip().split('\n')
    filteredLines = [line for line in lines if word not in line]
    result = '\n'.join(filteredLines)
    return result

def removeTextAfterPipe(string: str) -> str:
    lines = string.strip().split('\n')
    processedLines = [line.split('|')[0].strip() for line in lines]
    result = '\n'.join(processedLines)
    return result

#removes last line
def removeLastLine(string: str) -> str:
    lines = string.strip().split('\n')
    if lines:
        lines.pop()
    result = '\n'.join(lines)
    return result

def removeFirstLine(string: str) -> str:
    lines = string.strip().split('\n')
    if len(lines) > 1:
        return '\n'.join(lines[1:])
    return ''

#removes months age 
def removeAge(string: str) -> str:
    lines = string.strip().split('\n')
    processedLines = []

    for line in lines:
        words = line.split()
        filteredWords = [word for word in words 
            if not (re.search(r'\d', word) and 'm' in word.lower() and not ('a' in word.lower() or 'p' in word.lower()))]
        processedLines.append(' '.join(filteredWords))
    
    result = '\n'.join(processedLines)
    return result

#remove blank items
def removeBlankItems(string: str) -> str:
    str = []
    for item in string:
        if item != "" or item != " ":
            str.append(item)
    return str

#split mini/8 week classes
def splitMini(string: str, phrase: str) -> tuple:
    lines = string.strip().split('\n')
    collectedMini = []
    collectedFullSession = []
    found = False

    for line in lines:
        if not found and phrase.lower() in line.lower():
            found = True
            collectedFullSession.append(line)
        elif found:
            collectedFullSession.append(line)
        else:
            collectedMini.append(line)
    
    mini = '\n'.join(collectedMini)
    fullSession = '\n'.join(collectedFullSession)
    
    return mini, fullSession

#call functions to parse data
def parseData(string: str) -> str:
    lines = string.strip().split('\n')
    wordsToRemove = ["Customer", "NameEmail", "Tel", "Age", "DASH", "Platform", "by", "SportsIT", "Instructor", "Roster", "Season", "LTS", "Printed", "on", "of", "Page", "No"]
    cleanedLines = []

    for line in lines:
        for word in wordsToRemove:
            line = removeWord(line, word)
        cleanedLines.append(line)
    
    data = '\n'.join(cleanedLines)
    data = removeWordsWithCharacter(data)
    data = removeLineWithWord(data, "Instructor")
    data = removeTextAfterPipe(data)
    data = removeLineWithWord(data, "CLOSED")
    data = removeLastLine(data)
    data = removeAge(data)
    return data

#splits classes in format ["Class", class name, day, time, person 1, person 2...]
def splitClasses(string: str) -> list:
    lines = string.strip().split('\n')
    classes = []
    currentClass = None

    for line in lines:
        if line.lower().startswith('class'):
            if currentClass:
                classes.append(currentClass)
            currentClass = []
            currentClass.append(line.strip())
        else:
            if currentClass is not None:
                currentClass.append(line.strip())

    # Append the last class block if it exists
    if currentClass:
        classes.append(currentClass)

    # Process each class block to extract class details and persons
    formattedClasses = []
    for classBlock in classes:
        classInfo = classBlock[0]
        persons = classBlock[1:]
        parts = classInfo.split()
        
        if len(parts) >= 4:
            class_name = ' '.join(parts[1:-2]) 
            day = parts[-2] 
            time = parts[-1]
            class_entry = ["Class", class_name, day, time] + persons
            formattedClasses.append(class_entry)
    for theClass in formattedClasses:
        theClass.pop(0)

    return formattedClasses

#remove random classes 
def filter_random_classes(data: list) -> list:
    filtered_data = []
    valid_classes = ["Basic", "Snowplow", "LK", "Freeskate", "Lions", "Adult", "Power"]

    for item in data:
        class_name = item[0]
        # Check if the class_name contains any of the valid class prefixes
        if any(valid_class in class_name for valid_class in valid_classes):
            filtered_data.append(item)
    return filtered_data

#remove classes that dont need progress reports 
def filter_valid_classes(data: list) -> list:
    filtered_data = []
    valid_classes = ["Basic", "Snowplow", "LK", "Freeskate", "Lions", "Bronze", "Silver", "Gold", "1", "2"]

    for item in data:
        class_name = item[0]
        # Check if the class_name contains any of the valid class prefixes
        if any(valid_class in class_name for valid_class in valid_classes):
            filtered_data.append(item)
    return filtered_data


#load rosters into py files
def load_roster(roster_path:str) -> list:
    #filters data
    filteredData = parseData(extractTextFromPdf(roster_path))

    #split mini/8 week classes
    miniClasses, fullClasses = splitMini(filteredData, "8 Week")
    #remove line with groupon/mini and blank lines
    miniClasses = removeFirstLine(miniClasses)
    fullClasses = removeFirstLine(fullClasses)
    miniClasses = removeBlankLines(miniClasses)
    fullClasses = removeBlankLines(fullClasses)

    #THE FINAL LIST THAT HOLDS ALL THE SECRETS TO THE UNIVERSE
    fullClasses = splitClasses(fullClasses)
    miniClasses = splitClasses(miniClasses)

    #remove random blanks and random classes
    fullClasses = removeBlankItems(fullClasses)
    miniClasses = removeBlankItems(miniClasses)
    fullClasses = filter_random_classes(fullClasses)
    miniClasses = filter_random_classes(miniClasses)
    
    return fullClasses, miniClasses

def load_progress_roster(roster_path:str) -> list:
    fullClasses, miniClasses = load_roster(roster_path)
    progressClasses = filter_valid_classes(fullClasses)
    return progressClasses
