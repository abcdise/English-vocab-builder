import json
import prompts
import pyperclip
import itertools
from copy import deepcopy
from DictionaryReader import phrase_json_path

phrase_json_config_path = '../scr/config/Everyday English/config.json'


class PhraseDictionary:
    def __init__(self):
        self.init_phrase_dict = dict()
        with open(phrase_json_path) as file:
            self.phrase_dict = json.load(file)


    def import_initial_JSON(self, json_path:str):
        '''
        Import the initial JSON file and import the word list to the config file
        '''
        with open(json_path) as file:
            self.init_phrase_dict = json.load(file)
        word_list = self.init_phrase_dict.keys()
        with open(phrase_json_config_path) as file:
            old_config = json.load(file)
        seen = set(old_config.get('all', []))
        for word in word_list:
            if word not in seen:
                old_config['new'].append(word)
                old_config['all'].append(word)
        with open(phrase_json_config_path, 'w') as file:
            json.dump(old_config, file, ensure_ascii=False, indent=4)



    def get_prompt(self, start_index:int, end_index:int):
        dict_in_the_prompt = dict(itertools.islice(self.init_phrase_dict.items(), start_index, end_index))
        prompt = prompts.phrase_def_prompt
        prompt += '\n' + 'Please use Structure 1 or 2 to define the follwoing terms and write example sentences for each.' + '\n'
        prompt += json.dumps(dict_in_the_prompt)
        pyperclip.copy(prompt)
        print('Please go to Chat GPT to generate the JSON file.')

    
    def import_new_entries(self, new_dict:dict):
        extended_dict = dict()
        for word, entry in new_dict.items():
            if word in self.phrase_dict:
                print(f'The term {word} is in the dictionary and will be ignored.')
            else:
                extended_dict[word] = ['', []]
                extended_entry = dict()
                extended_entry['part_of_speech'] = "phrase"
                extended_entry['definition'] = entry['Definition']
                extended_entry['example_sentences'] = [entry['Example']]
                extended_entry['regional_note'] = ''
                extended_dict[word][1].append(deepcopy(extended_entry))
        
        self.phrase_dict.update(extended_dict)
        with open(phrase_json_path, 'w') as file:
            json.dump(self.phrase_dict, file, indent=4, ensure_ascii=False)
        print('==== Import successful ====')    



    
