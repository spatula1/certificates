import PyPDF2
import re

#VARIABLES

# Function to get text from PDF into a string
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

#removes lines with specific characters
def removeLineWithChar(text: str, chars: str) -> str:
    lines = text.strip().split('\n')
    filtered_lines = []

    for line in lines:
        skipLine = False
        for character in chars:
            if character in line:
                skipLine = True
                break  # Skip this line if any character is found

        if not skipLine:
            filtered_lines.append(line)

    result = '\n'.join(filtered_lines)
    return result

#remove char if in line
def removeChar(text: str) -> str:
    lines = text.strip().split('\n')
    chars = ["9", "8", "7", "0", "LANE", "#", ":", "PM"]
    filtered_lines = []

    for line in lines:
        modified_line = line
        for char in chars:
            # Replace the specific character with an empty string
            modified_line = modified_line.replace(char, '')
        # Append the modified line to the filtered lines after all characters are removed
        filtered_lines.append(modified_line)

    # Join the filtered lines back into a single string with newlines
    result = '\n'.join(filtered_lines)
    return result

#remove char 
def removeAM(text: str) -> str:
    lines = text.strip().split('\n')
    chars = ["AM", "FREE"]
    filtered_lines = []

    for line in lines:
        modified_line = line
        
        # Remove the specified characters if they appear as standalone words
        for char in chars:
            # Create a regex pattern that matches the standalone word
            pattern = fr'\b{re.escape(char)}\b'
            modified_line = re.sub(pattern, '', modified_line)

        # Append the modified line to the filtered lines after all characters are removed
        filtered_lines.append(modified_line.strip())

    # Join the filtered lines back into a single string with newlines
    result = '\n'.join(filtered_lines)
    return result

def removeLeadingNumbers(text: str) -> str:
    lines = text.strip().split('\n')
    filtered_lines = []

    for line in lines:
        # Remove leading digits
        modified_line = re.sub(r'^[\d\s]+', '', line).strip()
        filtered_lines.append(modified_line)

    # Join the filtered lines back into a single string with newlines
    result = '\n'.join(filtered_lines)
    return result

#removes blank lines, keep blank line between classes/coaches
def removeBlankLines(text: str) -> str:
    lines = text.strip().split('\n')
    if len(lines) == 0:
        return text  # If there are no lines, return the original text

    # Initialize a flag to track if the first blank line has been kept
    first_blank_line_kept = False
    filtered_lines = []

    for line in lines:
        if not line.strip():  # Check if the line is blank
            if not first_blank_line_kept:
                filtered_lines.append(line)  # Keep the first blank line
                first_blank_line_kept = True
        else:
            filtered_lines.append(line)  # Add non-blank lines to filtered lines

    # Join the filtered lines into a single string with newlines
    result = '\n'.join(filtered_lines)
    return result

#split into lists of coaches and classes
def splitData(text: str) -> tuple:
    lines = text.strip().split('\n')
    first_blank_index = None

    # Find the index of the first blank line
    for idx, line in enumerate(lines):
        if not line.strip():  # Check if the line is empty or contains only whitespace
            first_blank_index = idx
            break

    if first_blank_index is not None:
        coaches = lines[:first_blank_index]  # Lines before the first blank line
        classes = lines[first_blank_index + 1:]  # Lines after the first blank line
    else:
        coaches = lines  # If no blank line found, assume all lines are coaches
        classes = []

    return coaches, classes

#remove random number at the end of coaches
def removeNum(input_list):
    filtered_list = []

    for item in input_list:
        # Split each item by whitespace to separate words
        words = item.split()

        # Filter out any word that consists only of digits
        filtered_words = [word for word in words if not word.isdigit()]

        # Join the remaining words back into a single string
        filtered_item = ' '.join(filtered_words)

        # Append the filtered item to the result list
        filtered_list.append(filtered_item)

    return filtered_list

#combine coaches and classes into one list
def matchPairs(coaches, classes):
    pairs = []
    classNum = 2
    for coach, className in zip(coaches, classes):
        if '/' in className:
            combined_classes = className.split('/')
            name1 = combined_classes[0].split()[0]
            name2 = combined_classes[0].split()[1]
            classNum = 1
            if name1 == "SNOWPLOW": #get first 2 words for SNOWPLOW SAM
                name = combined_classes[0].split()[:2]
                name = name[0] + " " + name[1]
            elif name1 == "LK": #gets full class name for hockey classes 
                if name2 == "ADV": #gets first 4 words for LK ADV SKATING SKILLS 
                    name = combined_classes[0].split()[:4]
                    name = name[0] + " " + name[1] + " " + name[2] + " " + name[3]
                elif name2 == "SKATING" or name2 == "ACADEMY": #gets first 3 words for LK SKATING SKILLS & LK ACADEMY 1 & LK ACADEMY 2
                    name = combined_classes[0].split()[:3]
                    name = name[0] + " " + name[1] + " " + name[2]
            else:
                name = combined_classes[0].split()[0] #get first word to get full class name
            
            #append combined classes
            for combined_class in combined_classes:
                if classNum == 1:
                    pairs.append([coach, combined_class.strip()])
                    classNum = 2
                else:
                    pairs.append([coach, name + " " + combined_classes[1]])
        else: #append single classes
            pairs.append([coach, className])

    return pairs
#removes lists with classes that dont need progress reports
def filterList(data):
    wordsToCheck = ["GP", "LEGACIES", "SYNCHRO", "LA", "CHOREO"]
    filtered_data = []

    for sublist in data:
        remove = False
        for item in sublist:
            # Split the item into words
            words = item.split()
            # Check if any word matches exactly with words_to_check
            if any(word in words for word in wordsToCheck):
                remove = True
                break
        # Add the sublist to filtered_data only if it doesn't contain any exact word match
        if not remove:
            filtered_data.append(sublist)
    
    return filtered_data

#delete classes that dont need progress reports 
def deleteClasses(data: list)-> list:
    classes = ["FREESKATE", "SNOWPLOW", "LIONS", "LK", "BASIC", "BRONZE", "SILVER", "GOLD", "1", "2"]
    filteredData = []

    for coach, className in data:
        # Check if any class name in the list is part of the full class name
        if any(cls in className for cls in classes):
            filteredData.append([coach, className])

    return filteredData

#changes space to a slash for multiple coaches
def addCoachSlash(data: list) -> list:
    modified_data = []

    for item in data:
        if ' ' in item[0]:  # Check if there's a space in the first item
            item[0] = item[0].replace(' ', '/')  # Replace space with '/'
        modified_data.append(item)

    return modified_data


def load_lane_chart(roster_path: str) -> list:
    data = extractTextFromPdf(roster_path)
    data = removeLineWithChar(data, ['*', 'Rink', 'Coach', "WEEK", "Synchro"])
    data = removeChar(data)
    data = removeAM(data)
    data = removeLeadingNumbers(data)
    data = removeBlankLines(data)

    coaches, classes = splitData(data)
    coaches = removeNum(coaches)

    list = matchPairs(coaches, classes)
    list = filterList(list)
    list = deleteClasses(list)
    list = addCoachSlash(list)
    return list
