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
    

class Exercise(ABC):

    def __init__(self, word_list:list):
        self.word_list = word_list
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

#     def __init__(self, word_list: list):
#         super().__init__(word_list)
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
#             ex_text = r'\begin{enumerate}' + '\n'
#             sol_text = ex_text
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
#                         def_text += r'{' + definition + r'}'
#                         sentence_with_gap, solution_list = replace_term(original_string=definition, 
#                                 old_value=word, 
#                                 new_value=r'\ldots')
#                         if sentence_with_gap != definition and sentence_with_gap and solution_list:
#                             sentence_with_gap = sentence_with_gap.replace('...', r'{[\ldots] }')
#                             sentence_with_gap = remove_brackets_and_contents(sentence_with_gap)
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
#                 ex_text += r'\item ' + sentence_with_gap + '\n'
#                 sol_text += r'\item ' + solution + '\n'
#             ex_text += r'\end{enumerate}'
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

    def __init__(self, word_list: list):
        super().__init__(word_list)
        self.box = self._write_box(word_list=word_list)
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
            ex_text = r'\begin{enumerate}' + '\n'
            sol_text = ex_text
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
                        def_text += r'{' + definition + r'}'
                        sentence_with_gap, solution_list = replace_term(original_string=definition, 
                                old_value=word, 
                                new_value=r'\ldots')
                        if sentence_with_gap != definition and sentence_with_gap and solution_list:
                            sentence_with_gap = sentence_with_gap.replace('...', r'{[\ldots] }')
                            sentence_with_gap = remove_brackets_and_contents(sentence_with_gap)
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
                ex_text += r'\item ' + sentence_with_gap + '\n'
                sol_text += r'\item ' + solution + '\n'
            ex_text += r'\end{enumerate}'
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
    def __init__(self, word_list:list):
        super().__init__(word_list=word_list)
        self.dialogue: str = None
        self.passage: str = None
        self.box: str = None

    def create_prompt(self, passage:str):
        self.generation_prompt = f'''Term: {self.word_list}
        Original Text: 
        ```
        {passage}
        ```
        '''
        self.passage = self._string_processing(passage.replace('\n', '\n\n'))

    
    def import_dialogue(self, dialogue:str):
        dialogue_json = json.loads(dialogue)
        # Write box
        keywords = dialogue_json['keywords'] + self.word_list
        self.box = self._write_box(word_list=keywords)

        # Write dialogue
        dialog_list = dialogue_json['conversation']
        dialog_str = r'\begin{dialogue}' + '\n'
        solution_list = []
        for exchange in dialog_list:
            utterance = self._string_processing(exchange['text'])
            doc = nlp(utterance)
            for token in doc:
                if token.lemma_ in keywords or token.text in keywords:
                    utterance, solution = replace_term(original_string=utterance, old_value=token.text, new_value=r'\rule{1cm}{0.15mm}')
                    solution_list += solution
                    keywords.remove(token.lemma_) if token.lemma_ in keywords else keywords.remove(token.text)
            dialog_str += r'\speak{' + exchange['speaker'] + r'} ' + utterance + '\n'
        dialog_str += r'\end{dialogue}' + '\n'
        self.dialogue = dialog_str
        sol = r'\begin{enumerate}' + '\n'
        for solution in solution_list:
            sol += r'\item ' + solution + '\n'
        sol += r'\end{enumerate}' + '\n'
        self.solution = sol



    def finish_import(self):
        self.exercise_dict['box'] = self.box
        self.exercise_dict['passage'] = self.passage
        self.exercise_dict['solution'] = self.solution
        self.exercise_dict['dialogue'] = self.dialogue


class ExampleSentences(Exercise):
    example_sentences: dict = dict()
    example_sentences_with_analysis: dict = dict()

    def create_prompt(self, number_of_sentences:str):
        british_word_list = []
        for term in self.word_list:
            words = term.split(' ')
            words = [get_british_spelling(word) for word in words]
            term = ' '.join(words)
            british_word_list.append(term)

        prompt = prompts.example_sentences_prompt + '\n'
        prompt += f'Use the spelling rules for British English to create {number_of_sentences} example sentences with each term in the following list: {british_word_list}'
        self.generation_prompt = prompt

    
    def import_sentences(self, text: str):
        self.exercise = text
        self.example_sentences = json.loads(self.exercise)


    def get_second_prompt(self):
        output_dict = dict()
        for word, sentence_list in self.example_sentences.items():
            sentence_analysis_list = []
            for sentence in sentence_list:
                sentence_analysis = dict()
                sentence_analysis['Sentence'] = sentence
                sentence_analysis['Keyword'] = ''
                sentence_analysis['Excerpt'] = ''
                sentence_analysis['Paraphrase'] = ''
                sentence_analysis_list.append(deepcopy(sentence_analysis))
            output_dict[word] = deepcopy(sentence_analysis_list)

        prompt = prompts.example_sentences_second_prompt
        prompt += r'```json' + '\n'
        prompt += json.dumps(output_dict)
        prompt += r'```'
        return prompt

    
    def import_sentence_analysis(self, text: str):
        self.example_sentences_with_analysis = json_string_to_dict(text)


    def finish_import(self):
        tex_str = r'''\begin{enumerate}
        
        '''
        for sentence in self.example_sentences.values():
            tex_str += r'\item ' + f'{sentence}\n'
        tex_str += r'\end{enumerate}'
        self.exercise_dict['sentences'] = tex_str
        

class FillInTheGapExercise(Exercise):

    def __init__(self, word_list:list, example_sentences: ExampleSentences):
        super().__init__(word_list=word_list)
        self.word_list = [get_british_spelling(word) for word in self.word_list if len(word.split(' ')) == 1]
        self.box = self._write_box(word_list=self.word_list)
        self.example_sentences = example_sentences.example_sentences
        self.exercise, self.solution = self.generate_exercise(aug_dict=self.example_sentences)
 

    def finish_import(self):
        self.exercise_dict['exercise'] = self.exercise
        self.exercise_dict['box'] = self.box
        self.exercise_dict['solution'] = self.solution

    
    def generate_exercise(self, aug_dict: dict):
        exercise_list = []
        for word, sentence_list in aug_dict.items():
            for original_sentence in sentence_list:            
                question, sol_list = replace_term(original_string=original_sentence,
                                              old_value=word,
                                              new_value=r'\rule{1cm}{0.15mm}')
                if question != original_sentence:
                    exercise_list.append((question, ', '.join(sol_list)))
    
        random.shuffle(exercise_list)
        ex = r'\begin{enumerate}' + '\n'
        sol = r'\begin{enumerate}' + '\n'
        for exercise in exercise_list:
            ex += r'\item ' + exercise[0] + '\n'
            sol += r'\item ' + exercise[1] + '\n'

        ex += r'\end{enumerate}' + '\n'
        sol += r'\end{enumerate}' + '\n'

        return ex, sol


    def generate_solution(self, aug_dict: dict):
        None
    

class CompleteDefinitionsAndExamples(Exercise):
    '''
    Members:
    word_list(list): a list of terms
    dictionary(dict): a python dictionary imported from the json file
    definitions(dict): a python dictionary storing the definitions of words
    examples(dict): a python dictionay storing the examples of words
    exercise, solution(str): a LaTeX code block storing the questions and the solutions containing the definitions
    example_exercise, exercise_solution(str): a LaTeX code block storing the questions and the solutions containing the examples
    '''
    def __init__(self, word_list:list, dictionary_path: str='../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/English/Dictionary/Collins.json'):
        '''
        The main purpose of the the constructor is to prepare the organise the information from a dictionary into a python
        dictionary whose keys are the words and the values are lists of definitions in the dictionary
        '''
        super().__init__(word_list=word_list)
        self.word_list = [word for word in self.word_list if len(word.split(' ')) == 1]
        self.example_exercise: str = None
        self.example_solution: str = None
        self.box = self._write_box(word_list=self.word_list)
        dictionary_path_ = Path(dictionary_path)
        with open(dictionary_path_) as json_file:
            self.dictionary = json.load(json_file)
        self.definitions = dict()
        self.examples = dict()
        for word in word_list:
            word = get_american_spelling(word)
            if word in self.dictionary.keys():
                self.definitions[word] = []
                self.examples[word] = []
                entries = self.dictionary[word][1]
                for entry in entries:
                    definition = remove_brackets_and_contents(entry['definition'])
                    example_list = entry['example_sentences']
                    self.definitions[word].append(definition)
                    for example in example_list:
                        self.examples[word].append(example)


    def generate_exercise(self):
        '''
        Replace the keywords with gaps.
        '''
        # Shuffle the definitions
        self.exercise, self.solution = self._generate_gap_filling_exercise(self.definitions)
        self.example_exercise, self.example_solution = self._generate_gap_filling_exercise(self.examples)

    
    def _generate_gap_filling_exercise(self, input_dict: dict):
        '''
        The function returns a set of exercises based on an input dictionary.

        Args:
        input_dict(dict): keys are the keywords and each value is a list of sentences containing the keys.

        Return:
        exercise_text(str): a LaTeX block containing the gap filling exercise.
        solution_text(str): a LaTeX block containing the solutions.
        '''
        # Arrange the (keyword, sentence) pairs into a list. Shuffle the list in the end.
        extended_list = []
        for word in input_dict.keys():
            for sentence in input_dict[word]:
                extended_list.append((word, sentence))
        random.shuffle(extended_list)

        # Write the LaTeX code block. 
        exercise_text = r'\begin{enumerate}' + '\n'
        solution_text = exercise_text
        for pair in extended_list:
            # Replace the keywords with gaps
            original_sentence = pair[1]
            sentence_length = len(original_sentence.split(' '))
            if sentence_length > 3:
                sentence_with_gap, solution_list = replace_term(original_string=pair[1],
                                                        old_value=pair[0],
                                                        new_value=r'\rule{1cm}{0.15mm}')
                # Append the sentences with gaps to the current string
                if sentence_with_gap != pair[1]:
                    if sentence_with_gap:
                        sentence_with_gap = sentence_with_gap.replace('...', r'{[\ldots]} ')
                        exercise_text += r'\item ' + self._string_processing(sentence_with_gap) + '\n'
                    # Write the solution
                    if solution_list:
                        solution = ', '.join(solution_list)
                        solution_text += r'\item ' + self._string_processing(solution) + '\n'
        exercise_text += r'\end{enumerate}'
        solution_text += r'\end{enumerate}'

        return exercise_text, solution_text
    
    
    def finish_import(self):
        self.exercise_dict['box'] = self.box
        self.exercise_dict['definition_exercise'] = self.exercise
        self.exercise_dict['definition_solution'] = self.solution
        self.exercise_dict['example_exercise'] = self.example_exercise
        self.exercise_dict['example_solution'] = self.example_solution


class ParaphraseExercise(Exercise):
    def __init__(self, word_list: list, example_sentences: ExampleSentences):
        word_list = [get_british_spelling(word) for word in word_list]
        super().__init__(word_list=word_list)
        self.example_sentences = example_sentences.example_sentences
        self.example_sentences_with_analysis = example_sentences.example_sentences_with_analysis
        self.exercise, self.solution = self.__generate_exercise(aug_dict=self.example_sentences_with_analysis)


    def finish_import(self):
        self.exercise_dict['exercise'] = self.exercise
        self.exercise_dict['solution'] = self.solution


    def __generate_exercise(self, aug_dict: dict):
        exercise_list = []
        for term, analysis_list in aug_dict.items():
            for analysis in analysis_list:
                exercise_list.append((analysis['Keyword'], analysis['Sentence'], analysis['Excerpt'], analysis['Paraphrase']))

        random.shuffle(exercise_list)
        ex = r'\begin' + r'{enumerate}' + '\n'
        sol = r'\begin' + r'{enumerate}' + '\n'
        for exercise in exercise_list:
            paraphrased_sentence = exercise[3]
            question, _ = self.__replace_term(original_string=exercise[1],
                                                old_value=exercise[2],
                                                new_value=r'\rule{1cm}{0.15mm}')
            big_term = r'\textsc{' + exercise[0] + r'}'
            ex += r'\item ' + '\n'
            ex += paraphrased_sentence + r' \\' + '\n'
            ex += big_term + r' \\' + '\n'
            ex += question + r' \\' + '\n'
            sol += r'\item ' + exercise[2] + '\n'
        ex += r'\end{enumerate}' + '\n'
        sol += r'\end{enumerate}' + '\n'
        return ex, sol


    def __generate_solution(self, aug_dict: dict):
        pass


    def __replace_term(self, original_string: str, old_value: str, new_value: str):
        if len(old_value.split(' ')) == 1:
            return replace_term(original_string=original_string, old_value=old_value, new_value=new_value)
        else:
            return original_string.replace(old_value, new_value), [old_value]


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

    def __init__(self, word_list: list):
        super().__init__(word_list=word_list)
        self.phrase_dict = dict()
        self.abridged_phrase_dict = dict()
        self.__import_dictionary()
        self.create_prompt()
        self.box = self._write_box(word_list=word_list)
        self.exercise = None
        self.solution = None

    
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
                if word in self.phrase_dict.keys():
                    self.abridged_phrase_dict[word] = self.phrase_dict[word][1][0]['definition']
                else:
                    raise ValueError(f'The term {word} does not exist in the reference dictionary.')
        except FileNotFoundError:
            raise FileNotFoundError(f"The dictionary file '{dictionary_path}' does not exist.")
    

    def create_prompt(self):
        """
        Creates the prompt for the exercise.

        """
        prompt = prompts.dialogue_exercise_prompt
        prompt += 'Create the JSON file based on the following inputs'
        prompt += json.dumps(self.abridged_phrase_dict, ensure_ascii=False)
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
        

class ExerciseFactory:
    def create_exercise(self, exercise_type:str, word_list:list, example_sentences: ExampleSentences=None):
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
            return ReadingExercise(word_list=word_list)
        elif exercise_type == 'Fill in the gap':
            return FillInTheGapExercise(word_list=word_list, example_sentences=example_sentences)
        elif exercise_type == 'Paraphrase':
            return ParaphraseExercise(word_list=word_list, example_sentences=example_sentences)
        elif exercise_type == 'Definition':
            return Definition(word_list=word_list)
        elif exercise_type == 'Definition and Example Completion':
            return CompleteDefinitionsAndExamples(word_list=word_list)
        elif exercise_type == 'Dialogue':
            return DialogueExercise(word_list=word_list)
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
            return self._int_to_roman(set_index), self.exercise_set[-1]
        else:
            return self._int_to_roman(set_index), self.exercise_set[set_index-1]

    def _int_to_roman(self, num):
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