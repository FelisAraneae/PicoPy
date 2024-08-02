import re

def tokenise(text):
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

def tokenise_save(text):
    tokens = re.findall(r'\w+|\S', text)
    return tokens

def seperate_spaces(text):
    text = text.rstrip('\n')
    tokens = text.split(' ')
    return tokens

def is_string(text):
    tokenized = tokenise_save(text)
    if '"' in tokenized[0] or "'" in tokenized[0]:
        return(True)
    else:
        return(False)

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

def count_leading_tabs(line):
    count = 0
    for char in line:
        if char == '\t':
            count += 1
        else:
            break
    return count

def grab_between(text, separator, number):
    # Create a regex pattern to find text between separators, ignoring escaped separators
    pattern = rf'(?<!\\){re.escape(separator)}(.*?)(?<!\\){re.escape(separator)}'
    matches = re.findall(pattern, text)
    
    # Unescape any escaped separators in the matches
    matches = [re.sub(rf'\\{re.escape(separator)}', separator, match) for match in matches]
    
    # Return the specific match based on the number provided
    if 0 <= number < len(matches):
        return matches[number]
    else:
        return None