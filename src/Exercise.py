import pyperclip
from abc import ABC, abstractmethod
from copy import deepcopy
import random
import prompts
import json
import spacy
from utils import replace_term, string_processing_for_latex, get_gap_length

nlp = spacy.load('en_core_web_sm')


class Exercise(ABC):

    def __init__(self, word_entries:dict):
        self.word_entries = word_entries
        self.flattened_entries = self._flatten_word_entries(self.word_entries)
        self.word_list = list(self.word_entries.keys())
        self.generation_prompt = None
        self.exercise_dict: dict = dict() # A dictionary to store the exercise. The keys are usually 'exercise', 'solution', etc..


    @abstractmethod
    def _flatten_word_entries(self, word_entries:dict):
        pass


    @abstractmethod
    def _generate_exercise(self, dict:str):
        pass


    def get_outputs(self):
        return self.exercise_dict
    

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

    def _write_box(self, word_list:list):
        shuffled_word_list = deepcopy(word_list)
        shuffled_word_list = self._remove_duplicates(shuffled_word_list)
        random.shuffle(shuffled_word_list)
        return r' \qquad '.join(shuffled_word_list)
    

    def _remove_duplicates(self, data: list):
        return list(set(data))


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
        for i, entry in enumerate(flattened_entries):
            if i != len(flattened_entries) - 1:
                word_1 = entry['word']
                definition_1 = entry['definition']
                word_2 = flattened_entries[i + 1]['word']
                definition_2 = flattened_entries[i + 1]['definition']
            else:
                word_1 = entry['word']
                definition_1 = entry['definition']
                word_2 = flattened_entries[0]['word']
                definition_2 = flattened_entries[0]['definition']
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
            conversation = dict['conversation']
            dialogue_A = conversation[0]
            dialogue_B = conversation[1]
            # Preprocess the dialogues
            if 'A:' in dialogue_A and 'B:' in dialogue_B:
                dialogue_A = dialogue_A.replace('A:', '').strip()
                dialogue_B = dialogue_B.replace('B:', '').strip()
                dialogue_A = string_processing_for_latex(dialogue_A)
                dialogue_B = string_processing_for_latex(dialogue_B)
            definition = dict['definitions'][1]
            dialogue_B_gap, sol_list = replace_term(
                original_string=dialogue_B,
                old_value=word,
                new_value=f'\\fillin[{word}][{get_gap_length(word):.2f}in]'
            )
            if dialogue_B_gap != dialogue_B:
                question = '\\begin{dialogue} ' + '\\speak{A} ' + dialogue_A + ' \\speak{B} ' + dialogue_B_gap + ' \\end{dialogue}'
                exercise_list.append((question, ', '.join(sol_list), definition))
        random.shuffle(exercise_list)
        # Write the LaTeX code for the exercise and the solution
        ex = ''
        sol = r'\begin{enumerate}' + '\n'
        for exercise in exercise_list:
            question = exercise[0]
            solution = exercise[1]
            definition = exercise[2]
            ex += '\\question\\ ' + question + '\n'
            sol += '\\item ' + solution + '. ' + '\\textit{' + string_processing_for_latex(definition) + '}' + '\n'
        sol += r'\end{enumerate}' + '\n'
        return ex, sol


    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        for word in word_entries:
            if len(word.split(' ')) == 1:
                for definition_entry in word_entries[word]:
                    definition = definition_entry['definition']
                    flattened_entries.append({'word': word, 'definition': definition})
        return flattened_entries


class TranslationExercise(Exercise):
    def __init__(self, word_entries: dict):
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
            solution += r'\item ' + string_processing_for_latex(dictionary['English']) + '\n'
            exercise += r'\question ' + dictionary['Chinese'] + '\n'
            exercise += r'\begin{solutionbox}{10ex}' + '\n'
            exercise += string_processing_for_latex(dictionary['English']) + '\n'
            exercise += r'\end{solutionbox}' + '\n'
        solution += r'\end{enumerate}' + '\n'
        return exercise, solution

    
    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        # For each word, randomly select a sentence to include in the exercise
        for word in word_entries:
            list_of_sentences = []
            for definition_entry in word_entries[word]:
                examples = definition_entry['examples']
                for example in examples:
                    sentence = example
                    list_of_sentences.append(sentence)
                collocations = definition_entry['collocations']
                if 'noun' in collocations or 'idiom' in collocations:
                    for collocation in collocations.get('noun', []) + collocations.get('idiom', []):
                        sentence = collocation['example']
                        list_of_sentences.append(sentence)
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
        print(f'There will be {len(flattened_entries)} questions in the exercise.')

    
    def generate_exercise(self, text: str):
        imported_dict = json.loads(text)
        self.exercise_dict['exercise'], self.exercise_dict['solution'] = self._generate_exercise(dicts=imported_dict)
    

    def _generate_exercise(self, dicts: list):
        exercise = ''
        solution = r'\begin{enumerate}' + '\n'
        for dictionary in dicts:
            correct_sentence = dictionary['new example']
            incorrect_sentence = dictionary['question'].replace(r'[gap]', dictionary['options'][1])
            option = random.choice([0, 1])
            if option == 0:
                exercise += r'\question ' + correct_sentence + '\n\n \\begin{oneparcheckboxes} \\correctchoice Correct \\end{oneparcheckboxes} \\vspace{10ex}' + '\n'
                solution += r'\item Correct' + '\n'
            else:
                exercise += r'\question ' + incorrect_sentence + '\n\n \\begin{oneparcheckboxes} \\choice Correct \\end{oneparcheckboxes} \\vspace{10ex}' + '\n'
                solution += r'\item ' + correct_sentence + '\n'
        solution += r'\end{enumerate}' + '\n'
        return exercise, solution

    
    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        for word in word_entries:
            for entries in word_entries[word]:
                if len(word.split(' ')) > 1 and not entries['patterns']: # if the word is a phrase and there are no patterns, use the example sentence
                    flattened_entries.append({'word': word, 'pattern': {'usage': word, 'example': entries['examples'][0]['English']}})
                else:
                    for pattern in entries['patterns']:
                        flattened_entries.append({'word': word, 'pattern': {'usage': pattern['usage'], 'example': pattern['example']['English']}})
        return flattened_entries


class UsagePatternExercise(Exercise):
    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        keys = ['exercise', 'solution']
        self.exercise_dict = dict.fromkeys(keys)
        self.create_prompt()

    
    def create_prompt(self):
        # Create a list of dictionaries for the prompt
        random.shuffle(self.flattened_entries)
        prompt = prompts.pattern_prompt + '\n' + '```json' + '\n'
        prompt += f'{json.dumps(self.flattened_entries, ensure_ascii=False)}' + '\n'
        prompt += '```'
        self.generation_prompt = prompt
        print(f'There will be {len(self.flattened_entries)} questions in the exercise.')

    
    def generate_exercise(self, text: str):
        imported_dict = json.loads(text)
        self.exercise_dict['exercise'], self.exercise_dict['solution'] = self._generate_exercise(dicts=imported_dict)
    

    def _generate_exercise(self, dicts: list):
        exercise = ''
        solution = r'\begin{enumerate}' + '\n'
        for dictionary in dicts:
            term = dictionary['term']
            elements = dictionary['elements'] + dictionary['additional elements']
            random.shuffle(elements)
            elements = [term] + elements
            sentence = string_processing_for_latex(dictionary['sentence'])
            exercise += '\\question ' + r' \qquad '.join(elements) + '\n\n' + r'\vspace*{10ex}' + '\n\n'
            solution += '\\item ' + sentence + '\n'
        solution += r'\end{enumerate}' + '\n'
        return exercise, solution

    
    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        for word in word_entries:
            for entries in word_entries[word]:
                definition = entries['definition']
                for pattern in entries['patterns']:
                    flattened_entries.append({'term': word, 'definition': definition, 'usage pattern': pattern['usage']})
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
        print(f'There will be {len(flattened_entries)} questions in the exercise.')


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
            correct_pronunciation = dictionary['British received pronunciation']
            question, solution_list = replace_term(
                original_string=sentence,
                old_value=word,
                new_value='\\fillin[]'
            )
            options = dictionary['similar received pronunciations'] + [correct_pronunciation]
            random.shuffle(options)
            correct_answer_index = options.index(correct_pronunciation)
            option_labels = ['A', 'B', 'C', 'D']
            exercise += '\\question ' + question + '\n\n'
            exercise += r'\begin{choices}' + '\n'
            for option in options:
                if option == correct_pronunciation:
                    exercise += r'\CorrectChoice ' + option + ' '
                else:
                    exercise += r'\choice ' + option + ' '
            exercise += r'\end{choices}' + '\n'
            exercise += r'\answerline' + '\n'
            solution += r'\item ' + option_labels[correct_answer_index] + ' \\qquad ' + solution_list[0] + '. \n\n' + '\\textit{' + string_processing_for_latex(definition) + '}' + '\n'
        solution += r'\end{enumerate}' + '\n'
        return exercise, solution
        
    
    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        for word in word_entries:
            for definition_entry in word_entries[word]:
                definition = definition_entry['definition']
                pronunciation = definition_entry['British received pronunciation']
                flattened_entries.append({'word': word, 'definition': definition, 'British received pronunciation': pronunciation})
        return flattened_entries
    

class CollocationFillInTheGap(Exercise):
    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        keys = ['exercise', 'solution']
        self.exercise_dict = dict.fromkeys(keys)
        self.create_prompt()

    
    def create_prompt(self):
        # Create a list of dictionaries for the prompt
        random.shuffle(self.flattened_entries)
        prompt = prompts.collocation_prompt + '\n'
        prompt += f'{json.dumps(self.flattened_entries, ensure_ascii=False)}'
        self.generation_prompt = prompt
        print(f'There will be {len(self.flattened_entries)} questions in the exercise.')

    
    def generate_exercise(self, text: str):
        imported_dict = json.loads(text)
        for i, dictionary in enumerate(imported_dict):
            word = dictionary['word']
            dictionary['category'] = self.flattened_entries[i][word]['category']
        self.exercise_dict['exercise'], self.exercise_dict['solution'] = self._generate_exercise(dicts=imported_dict)

    
    def _generate_exercise(self, dicts: list):
        exercise_list = [] # A list to store the questions and solutions
        for dictionary in dicts:
            key = dictionary['key']
            category = dictionary['category']
            example = string_processing_for_latex(dictionary['new example'])
            collocation = dictionary['matching part']
            incomplete_collocation, sol_list = replace_term(
                original_string=collocation,
                old_value=key,
                new_value=f'\\fillin[{key}][{get_gap_length(key):.2f}in]'
            )
            if incomplete_collocation != collocation:
                question = example.replace(collocation, incomplete_collocation)
                assert question != example, f'Error: Replacement failed.'
                question = f' \\textit{{[{category}]}} ' + question
                exercise_list.append((question, ', '.join(sol_list)))
        random.shuffle(exercise_list)
        ex = ''
        sol = r'\begin{enumerate}' + '\n'
        for exercise in exercise_list:
            ex += '\\question ' + exercise[0] + '\n'
            sol += '\\item ' + exercise[1] + '\n'
        sol += r'\end{enumerate}' + '\n'
        return ex, sol
    
    
    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        for word in word_entries:
            for entry in word_entries[word]:
                collocations = entry['collocations']
                for category in collocations:
                    if category != 'noun':
                        for collocation in collocations[category]:
                            example = collocation['example']['English']
                            key = collocation['key']
                            flattened_entries.append({word: {'key': key, 'category': category, 'example': example}})
        return flattened_entries


class DialogueCompletionExercise(Exercise):
    def __init__(self, word_entries:dict):
        super().__init__(word_entries=word_entries)
        keys = ['exercise', 'solution']
        self.exercise_dict = dict.fromkeys(keys)
        self.create_prompt()

    
    def create_prompt(self):
        # Create a list of dictionaries for the prompt
        random.shuffle(self.flattened_entries)
        flattened_entries = [{'term': entry['term'], 'definition': entry['definition'], 'example': entry['example']} for entry in self.flattened_entries]
        prompt = prompts.dialogue_completion_prompt + '\n'
        prompt += r'```json' + '\n'
        prompt += f'{json.dumps(flattened_entries, ensure_ascii=False)}'
        prompt += r'```'
        self.generation_prompt = prompt
        print(f'There will be {len(flattened_entries)} questions in the exercise.')

    
    def generate_exercise(self, text: str):
        imported_dict = json.loads(text)
        for i, dictionary in enumerate(imported_dict):
            dictionary.update(self.flattened_entries[i])
        self.exercise_dict['exercise'], self.exercise_dict['solution'] = self._generate_exercise(dicts=imported_dict)

    
    def _generate_exercise(self, dicts: list):
        exercise_list = [] # A list to store the questions and solutions
        for dictionary in dicts:
            conversation = dictionary['dialogue']
            matching_part = dictionary['matching part']
            solution = matching_part
            topic = dictionary['Chinese']
            hint = dictionary['hint']
            length_of_gap = get_gap_length(solution)
            dialogue_A = conversation[0].replace(matching_part, f'\\fillin[{matching_part}][{length_of_gap:.2f}in]')
            dialogue_B = conversation[1].replace(matching_part, f'\\fillin[{matching_part}][{length_of_gap:.2f}in]')
            assert dialogue_A != conversation[0] or dialogue_B != conversation[1], f'Error: Replacement of {matching_part} failed.'
            question = '\\begin{dialogue} ' + '\\speak{A} ' + dialogue_A + ' \\speak{B} ' + dialogue_B + ' \\end{dialogue}'
            question += f' \\textit{{Hint: {hint}}}'
            exercise_list.append((question, solution, topic))
        random.shuffle(exercise_list)
        ex = ''
        sol = r'\begin{enumerate}' + '\n'
        for exercise in exercise_list:
            question = exercise[0]
            solution = exercise[1]
            topic = exercise[2]
            ex += f'\\question （{topic}）\\par ' + question + '\n'
            sol += '\\item ' + solution + '\n'
        sol += r'\end{enumerate}' + '\n'
        return ex, sol

    
    def _flatten_word_entries(self, word_entries: dict):
        flattened_entries = []
        for word in word_entries:
            for entry in word_entries[word]:
                definition = entry['definition']
                example = entry['examples'][0]['English']
                flattened_entries.append({'term': word, 'definition': definition, 'example': example, 'Chinese': entry['Chinese']})
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
        elif exercise_type == 'Usage pattern':
            return UsagePatternExercise(word_entries=word_entries)
        elif exercise_type == 'Spelling multiple choice':
            return VocabMultipleChoiceExercise(word_entries=word_entries)
        elif exercise_type == 'Collocation fill in the gap':
            return CollocationFillInTheGap(word_entries=word_entries)
        elif exercise_type == 'Dialogue completion':
            return DialogueCompletionExercise(word_entries=word_entries)
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