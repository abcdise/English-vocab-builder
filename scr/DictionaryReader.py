import json
from copy import deepcopy
from abc import ABC, abstractmethod

collins_json_path = '../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/English/Dictionary/Collins.json'
phrase_json_path = '../../../../../Library/Mobile Documents/com~apple~CloudDocs/Projects/Vocab Builder/English/Dictionary/Phrase.json'


class WordEntry:
    '''
    The class contains two attributes: `headword` (str) and `definition_entries` (list). 
    Each member of `definition_entries` is a python dictionary, whose keys are `part of speech`, `conjugation`, `definition`, `usage`, and `examples`
    '''
    def __init__(self, word:str) -> None:
        self.headword = word
        self.definition_entries = []


class DictionaryReader(ABC):
    '''
    Given a list `word_list` of words, the class saves the entries for the words in the dictionary.
    '''
    def __init__(self, json_path:str, word_list:list) -> None:
        with open(json_path) as file:
            self.dictionary = json.load(file)
        self.word_list = word_list
        self.word_entry_list = []


    def get_word_entry_list(self):
        self._update_word_entry_list(self.word_list)
        return self.word_entry_list
    

    def get_concise_dictionary(self):
        concise_dictionary = dict()
        for i in range(len(self.word_list)):
            word = self.word_list[i]
            definitions = []
            for entry in self.word_entry_list[i].definition_entries:
                definition = entry['definition']
                definitions.append(definition)
            concise_dictionary[word] = definitions
        return concise_dictionary


    @abstractmethod
    def _update_word_entry_list(self, word_list:list) -> None:
        pass


class EnglishDictionaryReader(DictionaryReader):
    def __init__(self, json_path:str, word_list:list) -> None:
        super().__init__(json_path, word_list)

    def _update_word_entry_list(self, word_list: list) -> None:
        for word in word_list:
            word_entry = WordEntry(word)
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


class CollinsReader(EnglishDictionaryReader):
    def __init__(self, word_list: list) -> None:
        super().__init__(json_path=collins_json_path, word_list=word_list)


class PhraseReader(EnglishDictionaryReader):
    def __init__(self, word_list: list) -> None:
        super().__init__(json_path=phrase_json_path, word_list=word_list)