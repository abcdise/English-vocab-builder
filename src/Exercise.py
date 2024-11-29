import pyperclip
from abc import ABC, abstractmethod
import re
from copy import deepcopy
import random
import prompts
import json
from pathlib import Path
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


class Exercise(ABC):

    def __init__(self, word_entries:dict):
        self.word_entries = word_entries
        self.word_list = list(self.word_entries.keys())
        self.generation_prompt = None
        self.exercise_dict: dict = dict() # A dictionary to store the exercise. The keys are usually 'exercise', 'solution', etc.


    @abstractmethod
    def finish_import(self):
        pass


    @abstractmethod
    def _flatten_word_entries(self, word_entries:dict):
        pass


    @abstractmethod
    def _generate_exercise(self, dict:str):
        pass

    def get_prompt(self):
        if self.generation_prompt is not None:
            pyperclip.copy(self.generation_prompt)
        else:
            print('There is no prompt yet.')


    def _partition_list(self, letters:list, unit_size:int=5):
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


    def _string_processing(self, text):
        '''
        Parse strings
        '''
        text = self.__unify_quotes(text)
        text = self.__replace_en_dashes(text)
        text = self.__replace_quotes(text)
        text = self.__replace_pounds(text)
        return text
    

    def __unify_quotes(self, text):
        text = text.replace("’", "'")
        text = text.replace("‘", "'")
        text = text.replace("“", '"')
        text = text.replace("”", '"')
        return text
                            

    def __replace_quotes(self, text):
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
        return ' '.join(text_list_new)


    def __replace_pounds(self, text):
        return text.replace('£', r'\pounds')


    def __replace_en_dashes(self, text):
        return text.replace('–', '--')
    

    def _write_box(self, word_list:list):
        shuffled_word_list = deepcopy(word_list)
        shuffled_word_list = self._remove_duplicates(shuffled_word_list)
        random.shuffle(shuffled_word_list)
        return r' \qquad '.join(shuffled_word_list)
    

    def _remove_duplicates(self, data: list):
        return list(set(data))



# class Definition(Exercise):
#     '''
#     A class representing a definition exercise.

#     Inherits from the Exercise class.

#     Attributes:
#     - word_list (list): A list of words for which the definitions need to be imported.
#     - definition (str): The formatted definitions and examples from the dictionary.
#     - exercise (str): The fill-in-the-gap exercise generated from the examples.
#     - solution (str): The solutions for the fill-in-the-gap exercise.

#     Methods:
#     - __init__(self, word_list: list): Initializes a Definition object with the given word list.
#     - import_definition_from_dictionary(self, dictionary_path:str='../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/English/Dictionary/Collins.json') -> None: Imports definitions and examples from the dictionary and generates the fill-in-the-gap exercise.
#     - finish_import(self): Adds the definition, exercise, and solution to the exercise dictionary.
#     '''

#     def __init__(self, word_entries: dict):
#         super().__init__(word_entries=word_entries)
#         self.box = self._write_box(word_list=self.word_list)
#         self.definition = None
#         self.definition_dict = dict()

#     def import_definition_from_dictionary(self, dictionary_path:str='../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/English/Dictionary/Collins.json') -> None:
#         '''
#         The method looks for the words in the dictionary and write the definitions and the examples from the dictionary as a form
#         that the LaTeX template is expecting. In the end, the methods gathers the examples and makes the fill-in-the-gap exercise.

#         Args:
#         - dictionary_path (str): The path of the json file that saves the dictionary.
#         '''
#         dictionary_json = Path(dictionary_path)
#         try:
#             with open(dictionary_json) as json_file:
#                 dictionary = json.load(json_file)

#             def_text = ''
#             ex_text = ''
#             sol_text = r'\begin{enumerate}' + '\n'
#             americanize_word_list = [get_american_spelling(word) for word in self.word_list]
#             exercise_list = []
#             for word in americanize_word_list:
#                 if word in dictionary:
#                     def_text += r'\vocabulary{' + word + r'}'
#                     def_text += r'{' + dictionary[word][0] + r'}' + '\n'
#                     for entry in dictionary[word][1]:
#                         def_text += r'\defitem{' + entry['part_of_speech'] + r'}'
#                         definition = entry['definition']
#                         definition = self._string_processing(definition)
#                         definition = remove_brackets_and_contents(definition)
#                         def_text += r'{' + definition + r'}'
#                         sentence_with_gap, solution_list = replace_term(
#                             original_string=definition, 
#                             old_value=word,
#                             new_value=f'\\fillin[{word}][{len(word) ** 0.1 - 0.3:.2f}in]'
#                         )
#                         if sentence_with_gap != definition and sentence_with_gap and solution_list:
#                             sentence_with_gap = sentence_with_gap.replace('...', r'{[\ldots] }')
#                             solution = ', '.join(solution_list)
#                             exercise_list.append((sentence_with_gap, solution))
#                         if entry['example_sentences']:
#                             sentence = entry['example_sentences'][0]
#                             sentence = self._string_processing(sentence)
#                             def_text += r'{' + sentence + r'}' + '\n'
#                         else:
#                             # If there is no example sentence, we still need a `{}` for the LaTeX command.
#                             def_text += r'{}' + '\n'
#                 else:
#                     print(f'The word {word} does not exist in the dictionary.')
#             random.shuffle(exercise_list)
#             for pair in exercise_list:
#                 sentence_with_gap = self._string_processing(pair[0])
#                 solution = self._string_processing(pair[1])
#                 ex_text += r'\question ' + sentence_with_gap + '\n'
#                 sol_text += r'\item ' + solution + '\n'
#             sol_text += r'\end{enumerate}'
#             self.definition = def_text # No need to preprocess the string because it has be done in the for loop
#             self.exercise = ex_text
#             self.solution = sol_text

#         except FileNotFoundError:
#             print(f"The dictionary file '{dictionary_json}' does not exist.")

#     def finish_import(self):
#         self.exercise_dict['definition'] = self.definition
#         self.exercise_dict['exercise'] = self.exercise
#         self.exercise_dict['solution'] = self.solution
#         self.exercise_dict['box'] = self.box


class FillInTheGapExercise(Exercise):

    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        keys = ['exercise', 'solution', 'box']
        self.exercise_dict = dict.fromkeys(keys)
        self.exercise_dict['box'] = self._write_box(word_list=self.word_list)
        self.create_prompt()
 

    def create_prompt(self):
        # Create a list of dictionaries for the prompt
        flattened_entries = self._flatten_word_entries(self.word_entries) # A list of dictionaries with word and definition
        random.shuffle(flattened_entries)


        dict_for_prompt = [] # A list of dictionaries with words and definitions. The list is used to create the prompt.
        # Add elements to the list dict_for_prompt
        for i in range(len(flattened_entries)):
            if i != len(flattened_entries) - 1:
                word_1 = flattened_entries[i].keys()[0]
                definition_1 = flattened_entries[i][word_1]
                word_2 = flattened_entries[i + 1].keys()[0]
                definition_2 = flattened_entries[i + 1][word_2]
            else:
                word_1 = flattened_entries[i].keys()[0]
                definition_1 = flattened_entries[i][word_1]
                word_2 = flattened_entries[0].keys()[0]
                definition_2 = flattened_entries[0][word_2]
            dict_for_prompt.append({"words": [word_1, word_2], "definitions": [definition_1, definition_2]})
        word_entries_str = json.dumps(dict_for_prompt, ensure_ascii=False)
        # Assemble the prompt
        prompt = prompts.fill_in_the_gap_prompt + '\n'
        prompt += f'{word_entries_str}'
        self.generation_prompt = prompt

    
    def generate_exercise(self, text: str):
        imported_dict = json.loads(text)
        self.exercise_dict['exercise'], self.exercise_dict['solution'] = self._generate_exercise(dicts=imported_dict)

    
    def _generate_exercise(self, dicts: list):
        exercise_list = [] # A list to store the questions, solutions, and definitions
        # Add elements to the list exercise_list
        for dict in dicts:
            word = dict['words'][1]
            sentence = dict['sentences']
            definition = dict['definitions'][1]
            question, sol_list = replace_term(
                original_string=sentence,
                old_value=word,
                new_value=f'\\fillin[{word}][{len(word) ** 0.1 - 0.3:.2f}in]'
            )
            if question != sentence:
                exercise_list.append((question, ', '.join(sol_list), definition))
        random.shuffle(exercise_list)
        # Write the LaTeX code for the exercise and the solution
        ex = ''
        sol = r'\begin{enumerate}' + '\n'
        for exercise in exercise_list:
            ex += r'\question ' + self._string_processing(exercise[0]) + '\n'
            sol += r'\item ' + exercise[1] + '. ' + self._string_processing(exercise[2]) + '\n'
        sol += r'\end{enumerate}' + '\n'
        return ex, sol


    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        for word in word_entries:
            for definition in word_entries[word]:
                flattened_entries.append({word: definition})
        return flattened_entries


class TranslationExercise(Exercise):
    def __init__(self, word_entries: dict):
        '''
        The dictionary word_entries should have the following structure:
        {
            'word': [
                        {
                            'English': '',
                            'Chinese': ''
                        }
                    ]
        }
        '''
        super().__init__(word_entries=word_entries)
        keys = ['exercise', 'solution']
        self.exercise_dict = dict.fromkeys(keys)


    def generate_exercise(self):
        imported_dict = self._flatten_word_entries(self.word_entries)
        random.shuffle(imported_dict)
        self.exercise_dict['exercise'], self.exercise_dict['solution'] = self._generate_exercise(dicts=imported_dict)

    
    def _generate_exercise(self, dicts: list):
        exercise = ''
        solution = r'\begin{enumerate}' + '\n'
        for dictionary in dicts:
            solution += r'\item ' + self._string_processing(dictionary['English']) + '\n'
            exercise += r'\question ' + dictionary['Chinese'] + '\n'
            exercise += r'\begin{solutionbox}{10ex}' + '\n'
            exercise += self._string_processing(dictionary['English']) + '\n'
            exercise += r'\end{solutionbox}' + '\n'
        solution += r'\end{enumerate}' + '\n'
        return exercise, solution

    
    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        # For each word, randomly select a sentence to include in the exercise
        for word in word_entries:
            list_of_sentences = []
            for sentence in word_entries[word]:
                list_of_sentences.append({word: sentence})
            flattened_entries.append(random.choice(list_of_sentences))
        return flattened_entries
                

class SentenceCorrectionExercise(Exercise):
    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        keys = ['exercise', 'solution']
        self.exercise_dict = dict.fromkeys(keys)
        self.create_prompt()

    
    def create_prompt(self):
        # Create a list of dictionaries for the prompt
        flattened_entries = self._flatten_word_entries(self.word_entries)
        random.shuffle(flattened_entries)
        prompt = prompts.sentence_correction_prompt + '\n'
        prompt += f'{json.dumps(flattened_entries, ensure_ascii=False)}'
        self.generation_prompt = prompt

    
    def generate_exercise(self, text: str):
        imported_dict = json.loads(text)
        self.exercise_dict['exercise'], self.exercise_dict['solution'] = self._generate_exercise(dicts=imported_dict)
    

    def _generate_exercise(self, dicts: list):
        exercise = ''
        solution = r'\begin{enumerate}' + '\n'
        for dictionary in dicts:
            correct_sentence = dictionary['correct sentence']
            incorrect_sentence = dictionary['incorrect sentence']
            option = random.choice([0, 1])
            exercise += r'\question ' + (correct_sentence if option == 0 else incorrect_sentence) + r'\answerline' + '\n'
            solution += r'\item ' + ('Correct' if option == 0 else correct_sentence) + '\n'
        solution += r'\end{enumerate}' + '\n'
        return exercise, solution

    
    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        for word in word_entries:
            for entries in word_entries[word]:
                for pattern in entries['patterns']:
                    flattened_entries.append({'word': word, 'definition': entries['definition'], 'pattern': pattern['pattern']})
        return flattened_entries


class VocabMultipleChoiceExercise(Exercise):
    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        keys = ['exercise', 'solution']
        self.exercise_dict = dict.fromkeys(keys)
        self.create_prompt()

    
    def create_prompt(self):
        # Create a list of dictionaries for the prompt
        flattened_entries = self._flatten_word_entries(self.word_entries)
        random.shuffle(flattened_entries)
        prompt = prompts.multiple_choice_prompt + '\n'
        prompt += f'{json.dumps(flattened_entries, ensure_ascii=False)}'
        self.generation_prompt = prompt


    def generate_exercise(self, text: str):
        imported_dict = json.loads(text)
        self.exercise_dict['exercise'], self.exercise_dict['solution'] = self._generate_exercise(dicts=imported_dict)

    
    def _generate_exercise(self, dicts: list):
        exercise = ''
        solution = r'\begin{enumerate}' + '\n'
        for dictionary in dicts:
            word = dictionary['word']
            sentence = dictionary['sentence']
            definition = dictionary['definition']
            question, _ = replace_term(
                original_string=sentence,
                old_value=word,
                new_value='\\fillin'
            )
            options = dictionary['other received pronunciations'] + [dictionary['received pronunciation']]
            random.shuffle(options)
            correct_answer_index = options.index(dictionary['received pronunciation'])
            option_labels = ['A', 'B', 'C', 'D']
            exercise += '\\question ' + question + '\n\n'
            exercise += r'\begin{oneparchoices}' + '\n'
            for option in options:
                if option == dictionary['received pronunciation']:
                    exercise += r'\CorrectChoice ' + option + '\n'
                else:
                    exercise += r'\choice ' + option + '\n'
            exercise += r'\end{oneparchoices}' + '\n'
            exercise += r'\answerline' + '\n'
            solution += r'\item ' + option_labels[correct_answer_index] + r' \\qquad ' + word + '. ' + definition + '\n'
        solution += r'\end{enumerate}' + '\n'
        return exercise, solution
        
    
    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        for word in word_entries:
            for definition in word_entries[word]:
                flattened_entries.append({word: definition})
        return flattened_entries
             

class ExerciseFactory:
    def create_exercise(self, exercise_type:str, word_entries:dict):
        '''
        Create exercises.

        Args:
            exercise_type (str): The type of exercise to create.
            word_list (list): A list of words for the exercise.
            example_sentences (ExampleSentences, optional): An instance of ExampleSentences class. Defaults to None.

        Returns:
            Exercise: An instance of the corresponding exercise class.

        Raises:
            ValueError: If the exercise type is invalid.
        '''
        if exercise_type == 'Fill in the gap':
            return FillInTheGapExercise(word_entries=word_entries)
        elif exercise_type == 'Translation':
            return TranslationExercise(word_entries=word_entries)
        elif exercise_type == 'Correction':
            return SentenceCorrectionExercise(word_entries=word_entries)
        elif exercise_type == 'Multiple choice':
            return VocabMultipleChoiceExercise(word_entries=word_entries)
        raise ValueError('Invalid exercise type!')
    """
    A class that represents an exercise gatherer.

    Attributes:
        exercise_set (list): A list to store exercises.

    Methods:
        import_exercise: Imports an exercise and adds it to the exercise set.
        get_exercise_set: Retrieves an exercise set based on the set index.
        _int_to_roman: Converts an integer to a Roman numeral.
    """

    def __init__(self):
        """
        Initializes an ExerciseGatherer object with an empty exercise set.
        """
        self.exercise_set = []

    def import_exercise(self, exercise):
        """
        Imports an exercise and adds it to the exercise set.

        Args:
            exercise (Exercise): The exercise to be imported.

        Returns:
            None
        """
        exercise_ = deepcopy(exercise)
        self.exercise_set.append(exercise_)