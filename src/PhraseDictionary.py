import json
from DictionaryReader import phrase_json_path

phrase_json_config_path = '../src/config/Everyday English/config.json'


class PhraseDictionary:
    def __init__(self):
        self.notes = dict()
        with open(phrase_json_path) as file:
            self.phrase_dict = json.load(file)


    def import_notes(self, json_path:str):
        '''
        Import the initial JSON file and import the word list to the config file
        '''
        with open(json_path) as file:
            self.notes = json.load(file)
        word_list = self.notes.keys()
        with open(phrase_json_config_path) as file:
            old_config = json.load(file)
        seen = set(old_config.get('all', []))
        for word in word_list:
            if word not in seen:
                old_config['new'].append(word)
                old_config['all'].append(word)
        with open(phrase_json_config_path, 'w') as file:
            json.dump(old_config, file, ensure_ascii=False, indent=4)
        
        self.phrase_dict.update(self.notes)
        with open(phrase_json_path, 'w') as file:
            json.dump(self.phrase_dict, file, indent=4, ensure_ascii=False)
        print('==== Import successful ====')



    
