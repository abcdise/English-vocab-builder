import pyperclip
from abc import ABC, abstractmethod
import re
from copy import deepcopy
import random
import prompts
import json
from pathlib import Path
import spacy
from breame.spelling import get_american_spelling
from breame.spelling import get_british_spelling

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
    new_string = []
    old_value_list = []

    for token in doc:
        if token.lemma_.lower() == old_value or token.text.lower() == old_value:
            new_string.append(new_value + token.whitespace_)
            # Append the solution to a list
            old_value_list.append(token.text)
        else: 
            new_string.append(token.text_with_ws)
    if new_string:
        new_string = ''.join(new_string)
    else:
        new_string = ''
    return new_string, old_value_list


def int_to_roman(num):
        """
        Converts an integer to a Roman numeral.

        Args:
            num (int): The integer to be converted.

        Returns:
            str: The Roman numeral representation of the integer.
        """
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        syms = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ]
        roman_numeral = ''
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman_numeral += syms[i]
                num -= val[i]
            i += 1
        return roman_numeral


class Exercise(ABC):

    def __init__(self, word_entries:dict):

        self.word_entries = word_entries
        # For each key in the dictionary, use `self._get_british_spelling` to get the British spelling and replace the key with the British spelling.
        self.word_entries = {self._get_british_spelling(key): list(map(remove_brackets_and_contents, value)) for key, value in self.word_entries.items()}
        self.word_list = list(self.word_entries.keys())
        self.generation_prompt = None
        self.exercise: str = None
        self.exercise_dict: dict = dict()
        self.solution: str = None


    @abstractmethod
    def finish_import(self):
        pass


    def get_prompt(self):
        if self.generation_prompt is not None:
            pyperclip.copy(self.generation_prompt)
        else:
            print('There is no prompt yet.')


    def import_exercise(self, text:str):
        self.exercise = self._string_processing(text)

    
    def import_solution(self, text:str):
        self.solution = self._string_processing(text)


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
    

    def _parse_example_sentences(self, text:str):
        sentence_list = text.splitlines()
        return list(filter(lambda x: x, sentence_list))
    

    def _remove_duplicates(self, data: list):
        return list(set(data))
    

    def _get_british_spelling(self, text:str):
        text_tokens = text.split(' ')
        text_tokens = [get_british_spelling(token) for token in text_tokens]
        return ' '.join(text_tokens)


class Definition(Exercise):
    '''
    A class representing a definition exercise.

    Inherits from the Exercise class.

    Attributes:
    - word_list (list): A list of words for which the definitions need to be imported.
    - definition (str): The formatted definitions and examples from the dictionary.
    - exercise (str): The fill-in-the-gap exercise generated from the examples.
    - solution (str): The solutions for the fill-in-the-gap exercise.

    Methods:
    - __init__(self, word_list: list): Initializes a Definition object with the given word list.
    - import_definition_from_dictionary(self, dictionary_path:str='../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/English/Dictionary/Collins.json') -> None: Imports definitions and examples from the dictionary and generates the fill-in-the-gap exercise.
    - finish_import(self): Adds the definition, exercise, and solution to the exercise dictionary.
    '''

    def __init__(self, word_entries: dict):
        super().__init__(word_entries=word_entries)
        self.box = self._write_box(word_list=self.word_list)
        self.definition = None
        self.definition_dict = dict()

    def import_definition_from_dictionary(self, dictionary_path:str='../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/English/Dictionary/Collins.json') -> None:
        '''
        The method looks for the words in the dictionary and write the definitions and the examples from the dictionary as a form
        that the LaTeX template is expecting. In the end, the methods gathers the examples and makes the fill-in-the-gap exercise.

        Args:
        - dictionary_path (str): The path of the json file that saves the dictionary.
        '''
        dictionary_json = Path(dictionary_path)
        try:
            with open(dictionary_json) as json_file:
                dictionary = json.load(json_file)

            def_text = ''
            ex_text = ''
            sol_text = r'\begin{enumerate}' + '\n'
            americanize_word_list = [get_american_spelling(word) for word in self.word_list]
            exercise_list = []
            for word in americanize_word_list:
                if word in dictionary:
                    def_text += r'\vocabulary{' + word + r'}'
                    def_text += r'{' + dictionary[word][0] + r'}' + '\n'
                    for entry in dictionary[word][1]:
                        def_text += r'\defitem{' + entry['part_of_speech'] + r'}'
                        definition = entry['definition']
                        definition = self._string_processing(definition)
                        definition = remove_brackets_and_contents(definition)
                        def_text += r'{' + definition + r'}'
                        sentence_with_gap, solution_list = replace_term(
                            original_string=definition, 
                            old_value=word,
                            new_value=f'\\fillin[{word}][{0.12*len(word):.2f}in]'
                        )
                        if sentence_with_gap != definition and sentence_with_gap and solution_list:
                            sentence_with_gap = sentence_with_gap.replace('...', r'{[\ldots] }')
                            solution = ', '.join(solution_list)
                            exercise_list.append((sentence_with_gap, solution))
                        if entry['example_sentences']:
                            sentence = entry['example_sentences'][0]
                            sentence = self._string_processing(sentence)
                            def_text += r'{' + sentence + r'}' + '\n'
                        else:
                            # If there is no example sentence, we still need a `{}` for the LaTeX command.
                            def_text += r'{}' + '\n'
                else:
                    print(f'The word {word} does not exist in the dictionary.')
            random.shuffle(exercise_list)
            for pair in exercise_list:
                sentence_with_gap = self._string_processing(pair[0])
                solution = self._string_processing(pair[1])
                ex_text += r'\question ' + sentence_with_gap + '\n'
                sol_text += r'\item ' + solution + '\n'
            sol_text += r'\end{enumerate}'
            self.definition = def_text # No need to preprocess the string because it has be done in the for loop
            self.exercise = ex_text
            self.solution = sol_text

        except FileNotFoundError:
            print(f"The dictionary file '{dictionary_json}' does not exist.")

    def finish_import(self):
        self.exercise_dict['definition'] = self.definition
        self.exercise_dict['exercise'] = self.exercise
        self.exercise_dict['solution'] = self.solution
        self.exercise_dict['box'] = self.box


class ReadingExercise(Exercise):
    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        # self.passage_dict = {word: [{"Definition": remove_brackets_and_contents(definition), "Passage": "Write the passage here"} for definition in word_entries[word]] for word in word_entries}
        self.passage: str = None
        self.question: str = None
        self.solution: str = None


    def create_prompt(self, topic:str):
        self.generation_prompt = f'''
        You are Oliver. Given the following terms and a topic, your task is to write a letter to your friend Noah about the topic. Keep the tone of the letter straightforward. Enrich the narrative in your letter. Use the words subtly into your letter. Your writing should follow the rules of British English spelling. Format the response in a txt code block.
        Inputs:
        ```json
        {self.word_entries}
        ```
        Starting sentence:
        {topic}
        '''

    
    def import_passage(self, text:str):
        self.passage = text


    def get_second_prompt(self):
        prompt = '''Based on the following text, write two correct inferences and three false inferences from the text. Ensure all five statements have similar lengths. Format your response in the following format
        ```json
        {"Correct inferences": ["Write the inferences here"], "False inferences": ["Write the inferences here"]}
        ```
        '''
        prompt += f'''Passage:
        {self.passage}'''
        pyperclip.copy(prompt)

    
    def import_exercise(self, text: str):
        imported_dict = json_string_to_dict(text)
        labels = ['A', 'B', 'C', 'D', 'E']

        self.question = r'Choose two correct statements based on the passage.\\'
        options = imported_dict['Correct inferences'] + imported_dict['False inferences']
        random.shuffle(options)
        options_with_labels = [f'{label}. {item}' for label, item in zip(labels, options)]
        solutions = [labels[options.index(option)] for option in imported_dict['Correct inferences']]
        self.solution = ''.join(solutions)
        self.question += (r'\\' + '\n').join(options_with_labels)


    def finish_import(self):
        self.exercise_dict['passage'] = self.passage
        self.exercise_dict['question'] = self.question
        self.exercise_dict['solution'] = self.solution
  

class FillInTheGapExercise(Exercise):

    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        self.word_list = [term for term in self.word_list if len(term.split(' ')) == 1]
        self.box = self._write_box(word_list=self.word_list)
        self.example_sentences = dict()
        self.create_prompt()
 

    def create_prompt(self):
        prompt = prompts.example_sentences_prompt + '\n'
        prompt += f'Use the spelling rules for British English to create two example sentences with each definition in the following list: {self.word_entries}'
        self.generation_prompt = prompt

    
    def import_sentences(self, text: str):
        self.example_sentences = json.loads(text)
        self.exercise, self.solution = self.generate_exercise(self.example_sentences)


    def finish_import(self):
        self.exercise_dict['exercise'] = self.exercise
        self.exercise_dict['box'] = self.box
        self.exercise_dict['solution'] = self.solution

    
    def generate_exercise(self, aug_dict: dict):
        exercise_list = []
        for word in aug_dict:
            for entry in aug_dict[word]:
                for sentence in entry['Example']:
                    question, sol_list = replace_term(
                        original_string=sentence,
                        old_value=word,
                        new_value=f'\\fillin[{word}][{0.12*len(word):.2f}in]'
                    )
                    if question != sentence:
                        exercise_list.append((question, ', '.join(sol_list), entry['Definition']))
    
        random.shuffle(exercise_list)
        ex = ''
        sol = r'\begin{enumerate}' + '\n'
        for exercise in exercise_list:
            ex += r'\question ' + self._string_processing(exercise[0]) + '\n'
            sol += r'\item ' + exercise[1] + '. ' + self._string_processing(exercise[2]) + '\n'

        sol += r'\end{enumerate}' + '\n'
        return ex, sol


class InferenceExercise(Exercise):
    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        self.create_prompt()
        self.example_sentences = dict()

    
    def create_prompt(self):
        prompt = prompts.inference_example_prompt + f'\n```json\n{self.word_entries}\n```'
        self.generation_prompt = prompt


    def get_exercise_prompt(self):
        prompt = prompts.inference_options_prompt + f'\n```json\n{self.example_sentences}\n```'
        pyperclip.copy(prompt)

    
    def import_sentences(self, text:str):
        self.exercise_dict = json.loads(text)
        for word in self.exercise_dict:
            self.example_sentences[word] = []
            for entry in self.exercise_dict[word]:
                self.example_sentences[word].append(entry['Example'])


    def import_exercise(self, text:str):
        # First import the text as a dictionary
        # Combine the options with the definitions and example sentences
        # Generate the exercise
        imported_dict = json_string_to_dict(text)
        for word in self.exercise_dict:
            for i, entry in enumerate(self.exercise_dict[word]):
                entry['Unlikely to happen'] = imported_dict[word][i]['Unlikely to happen']
        self.generate_exercise(self.exercise_dict)
        
    
    def generate_exercise(self, exercise_dict:dict):
        labels = ['A', 'B', 'C']
        solution_list = []
        definition_list = []
        exercise = ''

        for term, question_list in exercise_dict.items():
            for question in question_list:
                sentence = question['Example']
                definition_list.append((term, question['Definition']))
                answer_options = [question['Unlikely to happen']] + question['Likely to happen']
                random.shuffle(answer_options)
                solution_list.append(labels[answer_options.index(question['Unlikely to happen'])])
                exercise += f'\\question {self._string_processing(sentence)}\n'
                exercise += r'\begin{choices}' + '\n'
                for option in answer_options:
                    exercise += '{' + self._string_processing(option) + '}'
                exercise += r'\end{choices}' + '\n'
            
        solution = self._partition_list(solution_list) + '\n\n'
        solution += r'\vspace{3ex}' + '\n\n'
        solution += r'\begin{enumerate}' + '\n'
        for term_def in definition_list:
            solution += r'\item ' + term_def[0] + ': ' + term_def[1] + '\n'
        solution += r'\end{enumerate}' + '\n'
        self.exercise = exercise
        self.solution = solution


    def finish_import(self):
        self.exercise_dict['exercise'] = self.exercise
        self.exercise_dict['solution'] = self.solution
        

class DialogueExercise(Exercise):
    """
    Represents a dialogue exercise for vocabulary building.

    Args:
        word_list (list): A list of words for the exercise.

    Attributes:
        phrase_dict (dict): A dictionary containing phrases and their definitions.
        abridged_phrase_dict (dict): A dictionary containing abridged phrases and their definitions.
        box (str): The write box for the exercise.
        exercise (str): The generated exercise.
        solution (str): The solution for the exercise.

    Methods:
        __init__(self, word_list: list): Initializes a new instance of the DialogueExercise class.
        __import_dictionary(self, dictionary_path:str='../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/English/Dictionary/Phrase.json'): Imports the dictionary of phrases.
        create_prompt(self): Creates the prompt for the exercise.
        generate_exercise(self, dialogue_dict:dict): Generates the exercise based on the dialogue dictionary.
        finish_import(self): Finishes the import process.

    """

    def __init__(self, word_entries: dict):
        self.word_entries = word_entries
        self.word_list = list(self.word_entries.keys())
        self.generation_prompt = None
        self.exercise: str = None
        self.exercise_dict: dict = dict()
        self.solution: str = None
        self.phrase_dict = dict()
        self.abridged_phrase_dict = dict()
        self.__import_dictionary()
        self.create_prompt()

    
    def __import_dictionary(self, dictionary_path:str='../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/English/Dictionary/Phrase.json'):
        """
        Imports the dictionary of phrases.

        Args:
            dictionary_path (str): The path to the dictionary file. Default is the relative path to the Phrase.json file.

        Raises:
            FileNotFoundError: If the dictionary file does not exist.

        """
        try:
            with open(dictionary_path) as file:
                self.phrase_dict = json.load(file)
            for word in self.word_list:
                self.abridged_phrase_dict[word] = self.phrase_dict[word][1][0]['definition']
        except FileNotFoundError:
            raise FileNotFoundError(f"The dictionary file '{dictionary_path}' does not exist.")
    

    def create_prompt(self):
        """
        Creates the prompt for the exercise.

        """
        prompt = prompts.dialogue_exercise_prompt
        prompt += 'Create the JSON file based on the following inputs\n'
        prompt += '```json\n'
        prompt += json.dumps(self.abridged_phrase_dict, ensure_ascii=False)
        prompt += '\n```'
        self.generation_prompt = prompt


    def generate_exercise(self, dialogue_dict:dict):
        """
        Generates the exercise based on the dialogue dictionary.

        Args:
            dialogue_dict (dict): A dictionary containing dialogues.

        """
        ex = ''
        sol = r'\begin{enumerate}' + '\n'
        index = 1
        for _, dialogue in dialogue_dict.items():
            ex += r'\noindent \textbf{Dialogue ' + str(index) + '}\n'
            ex += r'\vspace{-1ex}' + '\n'
            ex += r'\begin{dialogue}' '\n'
            ex += r'\speak{A} ' + dialogue['A'] + '\n'
            ex += r'\speak{B} ' + dialogue['Paraphrase'] + '\n'
            ex += r'\end{dialogue}' + '\n'
            ex += r'\underline{\textsc{' + dialogue['Keyword'] + '}}\n'
            ex += r'\vspace{10ex}' + '\n\n'
            sol += r'\item ' + dialogue['B']  + '\n'
            index += 1

        sol += r'\end{enumerate}' + '\n'
        self.exercise = ex
        self.solution = sol

    
    def finish_import(self):
        """
        Finishes the import process.

        """
        self.exercise_dict['exercise'] = self.exercise
        self.exercise_dict['solution'] = self.solution


class ClozeExercise(Exercise):
    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        self.passage_dict = {word: [{"Definition": remove_brackets_and_contents(definition), "Passage": "Write the passage here"} for definition in word_entries[word]] for word in word_entries}
        self.__create_prompt()
        self.passage: str = None
        self.solution: str = None


    def __create_prompt(self):
        self.generation_prompt = f'''For each word and for each definition, write an elaborated piece of news of one paragraph in which the word is used. Incorporate each word subtly into the passage by using it only once. Ensure the word in the passage matches the given definition. Your passsages should adhere to the British English spelling rules. Format the response as follows
        ```json
        {self.passage_dict}
        ```
        '''

    
    def import_passage(self, text:str):
        self.passage_dict = deepcopy(json_string_to_dict(text))


    def get_second_prompt(self):
        passage_list = [passage for def_passage_list in self.passage_dict.values() for passage in def_passage_list]
        prompt = prompts.cloze_prompt + '\n'
        prompt += str(passage_list)
        pyperclip.copy(prompt)

    
    def import_exercise(self, text: str):
        imported_dict = json_string_to_dict(text)
        self.passage = ''
        self.solution = ''
        labels = ['A', 'B', 'C', 'D']
        indices = [1, 2, 3, 4]
        solution_list = []
        solution_option_list = []
        passage_index = 1
        
        for passage in imported_dict:
            question_list = []
            solution_sub_list = []
            solution_option_sub_list = []
            for i, exercise in enumerate(imported_dict[passage]):
                index = i + 1
                excerpt = exercise['Phrase']
                word_to_replace = exercise['Word']
                sentence_with_gap = excerpt.replace(word_to_replace, f'({index})' + r'\fillin[]')
                passage = passage.replace(excerpt, sentence_with_gap)
                answer_options = exercise['Incorrect options'] + [word_to_replace]
                random.shuffle(indices)
                solution_sub_list.append(labels[indices.index(4)])
                solution_option_sub_list.append(word_to_replace)
                question_list.append([answer_options[i - 1] for i in indices])
            
            self.passage += r'\noindent \textbf{Passage ' + str(passage_index) + '} \n\n' + self._string_processing(passage) + '\n\n'
            self.passage += r'\begin{questions}' + '\n'
            for i, options in enumerate(question_list):
                self.passage += r'\question ' + '\n'
                self.passage += r'\begin{oneparchoices}' + '\n'
                for option in options:
                    correct_choice_symbol = r'\CorrectChoice ' if option == solution_option_sub_list[i] else r'\choice '
                    self.passage += correct_choice_symbol + self._string_processing(option) + '\n'
                self.passage += r'\end{oneparchoices}' + '\n'

            self.passage += r'\end{questions}' + '\n'
            solution_list.append(solution_sub_list)
            passage_index += 1
            self.passage += r'\vspace{3ex}' + '\n\n'

        self.solution += '\n\n' + r'\vspace{3ex}' + '\n\n'
        for solution_index, solution in enumerate(solution_list):    
            self.solution += f' {solution_index + 1}. ' + ''.join(solution) + r' \quad'


    def finish_import(self):
        self.exercise_dict['passage'] = self.passage
        self.exercise_dict['solution'] = self.solution


class TranslationExercise(Exercise):
    def __init__(self, word_entries: dict):
        super().__init__(word_entries)
        self.word_list = [term for term in self.word_list if len(term.split(' ')) == 1]
        self.box = r'\centering ' + self._write_box(word_list=self.word_list)
        self.example_sentences = dict()
        self.create_prompt()


    def create_prompt(self):
        prompt = prompts.translation_prompt + '\n'
        prompt += f'Here is the list of terms and their definitions: {self.word_entries}'
        self.generation_prompt = prompt

    
    def import_sentences(self, text: str):
        self.exercise = text
        self.example_sentences = json.loads(self.exercise)
        self.exercise, self.solution = self.generate_exercise(aug_dict=self.example_sentences)

    
    def generate_exercise(self, aug_dict: dict):
        exercise = r'\begin{enumerate}' + '\n'
        solution = r'\begin{enumerate}' + '\n'
        for word in aug_dict:
            for entry in aug_dict[word]:
                solution += r'\item ' + self._string_processing(entry['Example']) + '\n'
                exercise += r'\item ' + entry['Colloquial Chinese'] + '\n' + r'\vspace{10ex}' + '\n'

        exercise += r'\end{enumerate}' + '\n'
        solution += r'\end{enumerate}' + '\n'
        return exercise, solution

    
    def finish_import(self):
        self.exercise_dict['exercise'] = self.exercise
        self.exercise_dict['box'] = self.box
        self.exercise_dict['solution'] = self.solution


class ComprehensionExercise(Exercise):
    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        self.create_prompt()


    def create_prompt(self):
        prompt = prompts.comprehension_prompt + '\n'
        prompt += f'Here is the list of terms and their definitions: {self.word_entries}'
        self.generation_prompt = prompt


    def import_exercise(self, text:str):
        imported_dict = json_string_to_dict(text)
        keys = ['Yes Question', 'No Question']
        solution_list = []
        definition_list = []
        exercise = ''

        for term, question_list in imported_dict.items():
            for question in question_list:
                true_of_false = random.choice(keys)
                label = 'Y' if true_of_false == 'Yes Question' else 'N'
                sentence = self._string_processing(question[true_of_false])
                definition_list.append((term, question['Definition']))
                solution_list.append(label)
                exercise += f'\\question \\tf[{label}] ' + sentence + '\n'
        
        solution = self._partition_list(solution_list) + '\n\n'
        solution += r'\vspace{3ex}' + '\n\n'
        solution += r'\begin{enumerate}' + '\n'
        for term_def in definition_list:
            solution += r'\item ' + term_def[0] + ': ' + term_def[1] + '\n'
        solution += r'\end{enumerate}' + '\n'
        self.exercise = exercise
        self.solution = solution

    
    def finish_import(self):
        self.exercise_dict['exercise'] = self.exercise
        self.exercise_dict['solution'] = self.solution


class SentenceOrderExercise(Exercise):
    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        self.create_prompt()


    def create_prompt(self):
        prompt = prompts.sentence_order_prompt + '\n'
        prompt += f'Try the following' + '\n'
        prompt += f'```json\n{self.word_entries}\n```'
        self.generation_prompt = prompt

    
    def import_exercise(self, text:str):
        imported_dict = json_string_to_dict(text)
        solution_list = []
        definition_list = []
        exercise = ''
        solution = ''
        for term, entry_list in imported_dict.items():
            for entry in entry_list:
                index = [1, 2, 3]
                definition_list.append((term, entry['Definition']))
                paragraph = entry['Paragraph']
                random.shuffle(index)
                solution_list.append(''.join([str(i) for i in index]))
                exercise += f'\\question \\tf[{index[0]}] ' + self._string_processing(paragraph[index[0] - 1]) + '\n\n'
                exercise += f'\\tf[{index[1]}] ' + self._string_processing(paragraph[index[1] - 1]) + '\n\n'
                exercise += f'\\tf[{index[2]}] ' + self._string_processing(paragraph[index[2] - 1]) + '\n\n'

        for i, ordering in enumerate(solution_list):
            solution += f'{i + 1}. {ordering}' + r' \quad '

        solution += '\n\n' + r'\vspace{3ex}' + '\n\n'
        solution += r'\begin{enumerate}' + '\n'
        for term_def in definition_list:
            solution += r'\item ' + term_def[0] + ': ' + term_def[1] + '\n'
        solution += r'\end{enumerate}' + '\n'
        self.exercise = exercise
        self.solution = solution

    def finish_import(self):
        self.exercise_dict['exercise'] = self.exercise
        self.exercise_dict['solution'] = self.solution


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
        if exercise_type == 'Reading':
            return ReadingExercise(word_entries=word_entries)
        elif exercise_type == 'Inference':
            return InferenceExercise(word_entries=word_entries)
        elif exercise_type == 'Cloze':
            return ClozeExercise(word_entries=word_entries)
        elif exercise_type == 'Fill in the gap':
            return FillInTheGapExercise(word_entries=word_entries)
        elif exercise_type == 'Definition':
            return Definition(word_entries=word_entries)
        elif exercise_type == 'Dialogue':
            return DialogueExercise(word_entries=word_entries)
        elif exercise_type == 'Translation':
            return TranslationExercise(word_entries=word_entries)
        elif exercise_type == 'Comprehension':
            return ComprehensionExercise(word_entries=word_entries)
        elif exercise_type == 'Sentence Order':
            return SentenceOrderExercise(word_entries=word_entries)
        raise ValueError('Invalid exercise type!')
    

class ExerciseGatherer:
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

    def get_exercise_set(self, set_index, last_set=True):
        """
        Retrieves an exercise set based on the set index.

        Args:
            set_index (int): The index of the exercise set.
            last_set (bool): Flag indicating whether to retrieve the last set or not.

        Returns:
            tuple: A tuple containing the set index (in Roman numeral) and the exercise set.
        """
        if last_set:
            return int_to_roman(set_index), self.exercise_set[-1]
        else:
            return int_to_roman(set_index), self.exercise_set[set_index-1]