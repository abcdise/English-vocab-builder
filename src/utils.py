import json
import re
import spacy
nlp = spacy.load('en_core_web_sm')

def json_string_to_dict(json_string: str):
    try:
        # Convert the JSON string to a Python dictionary
        python_dict = json.loads(json_string)
        return python_dict
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None


def remove_brackets_and_contents(text):
    """
    Removes brackets and their contents from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with brackets and their contents removed.
    """
    return re.sub(r'\[.*?\]', '', text)


def replace_term(original_string: str, old_value: str, new_value: str):
    doc = nlp(original_string)
    new_string_list = []
    old_value_list = []
    # Handle the case where the old value is a multi-word term
    if '-' in old_value:
        units = original_string.split(' ')
        for unit in units:
            if old_value in unit:
                new_string_list.append(unit.replace(old_value, new_value))
                old_value_list.append(old_value)
            else:
                new_string_list.append(unit)
        if new_string_list:
            new_string = ' '.join(new_string_list)
        else:
            new_string = ''
    else:
        for token in doc:
            if token.lemma_.lower() == old_value or token.text.lower() == old_value:
                new_string_list.append(new_value + token.whitespace_)
                # Append the solution to a list
                old_value_list.append(token.text)
            else: 
                new_string_list.append(token.text_with_ws)
        if new_string_list:
            new_string = ''.join(new_string_list)
        else:
            new_string = ''
    return new_string, old_value_list


def swap_words(sentence, word1, word2):
    """
    Swaps the positions of two words in a sentence, preserving punctuation.

    Args:
        sentence: The input sentence.
        word1: The first word to swap.
        word2: The second word to swap.

    Returns:
        The modified sentence with the words swapped.
    """
    # Check if both words are in the sentence (ignoring case)
    pattern1 = re.compile(r'\b' + re.escape(word1) + r'\b', re.IGNORECASE)
    pattern2 = re.compile(r'\b' + re.escape(word2) + r'\b', re.IGNORECASE)
    
    if not (pattern1.search(sentence) and pattern2.search(sentence)):
        raise ValueError("Both words must be in the sentence.")

    # Function to replace the word while preserving punctuation and case
    def replace_word(match, replacement):
        matched_word = match.group(0)
        if matched_word.islower():
            return replacement.lower()
        elif matched_word.isupper():
            return replacement.upper()
        elif matched_word.istitle():
            return replacement.capitalize()
        else:
            return replacement

    # Perform the swap
    temp_word = "TEMP_WORD_FOR_SWAP"
    sentence = pattern1.sub(lambda m: replace_word(m, temp_word), sentence)
    sentence = pattern2.sub(lambda m: replace_word(m, word1), sentence)
    sentence = re.compile(r'\b' + re.escape(temp_word) + r'\b', re.IGNORECASE).sub(lambda m: replace_word(m, word2), sentence)

    return sentence


def partition_list(letters:list, unit_size:int=5):
    # Calculate the number of full units
    num_full_units = len(letters) // unit_size
    # Calculate the remainder if any
    remainder = len(letters) % unit_size
    
    # Create the units
    units = [letters[i * unit_size:(i + 1) * unit_size] for i in range(num_full_units)]
    
    # Add the remaining letters if there are any
    if remainder > 0:
        units.append(letters[num_full_units * unit_size:])
    
    # Format the output as a space-separated string
    formatted_output = ' '.join([''.join(unit) for unit in units])
    
    return formatted_output


def string_processing_for_latex(text):
    '''
    Parse strings
    '''
    # Unify quotes
    text = text.replace("’", "'")
    text = text.replace("‘", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')

    # Replace en-dashes
    text = text.replace('–', '--')

    # Replace quotes
    text_list = text.split(' ')
    text_list_new = []
    for word in text_list:
        if word.startswith("'"):
            word = '`' + word[1:]
        if word.startswith('"'):
            word = '``' + word[1:]
        if word.endswith('"'):
            word = word[:-1] + "''"
        text_list_new.append(word)

    text = ' '.join(text_list_new)

    # Replace pounds
    text = text.replace('£', '\\pounds')

    return text
    

