from skPublish import API
import json
from bs4 import BeautifulSoup
from pathlib import Path
import time
from copy import deepcopy
from breame.spelling import get_american_spelling
from dotenv import load_dotenv
import os
from Word_entry import Word_entry, Dictionary_reader


load_dotenv(dotenv_path='../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/vars/.env')
api_key = os.getenv('COLLINS_API_KEY')
collins_json_path = '../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/English/Dictionary/Collins.json'

class Collins_entry:
    def __init__(self, word:str):
        self.word = word
        self.raw_entry = dict()
        self.dictionary = dict()
        print(f'Looking up the word {self.word}...')

    
    def look_up(self, api_key=api_key):
        time.sleep(3)
        self.__get_raw_entry(api_key=api_key)
        self.__parse_headword()
        return self.dictionary
    

    def __get_raw_entry(self, api_key=api_key):
        base_url = 'https://api.collinsdictionary.com/api/v1'
        api = API(baseUrl=base_url, accessKey=api_key)
        search_word = get_american_spelling(search_word)
        response = api.searchFirst(dictionaryCode='english-learner', 
                                            searchWord=search_word, 
                                            entryFormat='html')
        self.raw_entry = json.loads(response.decode())


    def __parse_headword(self):
        if 'errorCode' in self.raw_entry.keys():
            print(f'The word {self.word} can not be found.')
        else:
            html_content = self.dictionary['entryContent']
            soup = BeautifulSoup(html_content, 'html.parser')
            parsed_data = {
                'word': None,
                'conjugations': None,
                'entries': []
            }
            
            # Extract word
            parsed_data['word'] = soup.find('h1', {'class': 'hwd'}).text if soup.find('h1', {'class': 'hwd'}) else "Not found"

            # Extract conjugations
            conjugation_tags = soup.find_all('span', class_='orth')
            if conjugation_tags is not None:
                conjugation_list = [tag.string for tag in conjugation_tags]
                conjugation_list = list(dict.fromkeys(conjugation_list))
                parsed_data['conjugations'] = ', '.join(conjugation_list)
            else:
                parsed_data['conjugations'] = ''
            
            # Loop through each 'hom' (homograph) block
            for hom_block in soup.find_all('div', {'class': 'hom'}):
                entry = {}
                
                # Find part of speech. If there is no part of speech, jump to the next entry.
                pos_span = hom_block.find('span', {'class': 'pos'})
                if pos_span:
                    part_of_speech = pos_span.text.strip()
                    if part_of_speech != '':
                        entry['part_of_speech'] = part_of_speech
                    else: continue
                else: continue
                
                # Find definition
                def_span = hom_block.find('span', {'class': 'def'})
                definition = def_span.text.strip() if def_span else ""
                add_span = hom_block.find('span', {'class': 'lbl'})
                definition += (' ' + add_span.text.strip()) if add_span else ""
                if r'[' in definition and r']' not in definition:
                    definition += r']'
                entry['definition'] = definition.replace('\n', '')
                
                # Find example sentences
                entry['example_sentences'] = [example_span.text.strip() for example_span in hom_block.find_all('span', {'class': 'quote'})]
                
                # Find regional notes (assuming they are in a span with class 'regional_note', this might need to be adjusted)
                regional_note_span = hom_block.find('span', {'class': 'regional_note'})
                entry['regional_note'] = regional_note_span.text.strip() if regional_note_span else ""
                
                # Append this entry to the list of entries
                parsed_data['entries'].append(entry)
            self.dictionary = deepcopy(parsed_data)            


class Collins_writer:
    def __init__(self, dictionary_path: str=collins_json_path):
        '''
        Constructor.

        Members:
        self.dictionary_json (Path): The path of the json file.
        self.dictionary (Dictionary): The dictionary (e.g. Collins)
        self.dic (dict): The python dictionary imported from the json file
        self.new_entries (dict): New words to be attatched to the json file
        '''
        self.dictionary_json = Path(dictionary_path)
        if not self.dictionary_json.exists():
            with open(self.dictionary_json, 'w') as json_file:
                json.dump({}, json_file)
        with open(self.dictionary_json) as json_file:
            self.dic = json.load(json_file)
        self.new_entries = dict()
 

    def look_up(self, word_list: list):
        entry_list = []
        for word in word_list:
            if not word in self.dic.keys():
                # if the word hasn't been in the dictionary
                collins_entry = Collins_entry(word=word)
                entry = collins_entry.look_up()
                if entry:
                    entry_list.append(entry)
            self.new_entries = self.__list_to_dict(entry_list)
            self.__refresh_dictionary()
    

    def __refresh_dictionary(self):
        self.dic.update(self.new_entries)
        with open(self.dictionary_json, 'w') as json_file:
            json.dump(self.dic, json_file, indent=4)


    def __list_to_dict(self, l:list) -> dict:
        result_dict = dict()
        for dic in l:
            result_dict[dic['word']] = [dic['conjugations'], dic['entries']]
        return result_dict     


class Collins_reader(Dictionary_reader):
    def __init__(self, word_list:list, json_path:str=collins_json_path) -> None:
        super().__init__(json_path, word_list)

    def _update_word_entry_list(self, word_list: list) -> None:
        for word in word_list:
            word_entry = Word_entry(word)
            word_item = self.dictionary.get(word, [])
            if word_item:
                conjugations = word_item[0]
                for definition_item in word_item[1]:
                    definition_entry = dict()
                    definition = definition_item['definition']
                    examples = definition_item['example_sentences']
                    part_of_speech = definition_item['part_of_speech']
                    definition_entry['conjugation'] = conjugations
                    definition_entry['definition'] = definition
                    definition_entry['examples'] = examples
                    definition_entry['part of speech'] = part_of_speech
                    definition_entry['usage'] = ''
                    word_entry.definition_entries.append(deepcopy(definition_entry))
                
                self.word_entry_list.append(deepcopy(word_entry))
            else:
                print(f'The word {word} does not exist in the json file!')

   