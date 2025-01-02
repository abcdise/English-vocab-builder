import json
from pathlib import Path
from copy import deepcopy
import requests
from numpy import random
import csv
import re
from datetime import date
from abc import ABC, abstractmethod


class Configurator:
    '''
    A class that manipulates the configuration json file.
    Members:
    json_path: The path of the json file.
    config(dict): The data saved in the config json file.
    '''
    def __init__(self, json_path:str):
        self.json_path = Path(json_path)
        assert Path.exists(self.json_path), 'The scheduler json file does not exist'
        with open(self.json_path) as file:
            self.config = json.load(file)


    def reset(self):
        '''
        The method set the `review` list to an empty list and set the `new` list to the whole list.
        '''
        self.config['unlearned'] = (self.config['learned'] + self.config['unlearned']).sort()
        self.config['learned'] = []
        self.config['last learned'] = []
        self.config['last timestamp'] = '2000-01-01'
        self.config['timestamp'] = '2000-01-01'
        self.__export()

    
    def get_n_words_to_learn(self, n:int):
        list_to_return = self.config['unlearned'][:n]
        if len(list_to_return) < n:
            print(f'Only {len(list_to_return)} words left to learn')
        return list_to_return
    

    def revert_last_study(self):
        self.config['timestamp'] = self.config['last timestamp']
        self.config['unlearned'] = self.config['last learned'] + self.config['unlearned']
        self.config['learned'] = [word for word in self.config['learned'] if word not in self.config['last learned']]
        self.__export()

    

    def study_n_words(self, n:int):
        new_list = self.config['unlearned']
        review_list = self.config['learned']
        new_word_list = self.get_n_words_to_learn(n)
        review_list += new_word_list
        new_list = [word for word in new_list if word not in new_word_list]
        self.config['learned'] = deepcopy(review_list)
        self.config['unlearned'] = deepcopy(new_list)
        self.config['last learned'] = new_word_list
        assert self.config['timestamp'] != str(date.today()), 'You have already studied today.'
        self.config['last timestamp'] = self.config['timestamp']
        self.config['timestamp'] = str(date.today())
        self.__export()


    def __export(self):
        with open(self.json_path, 'w') as file:
            json.dump(self.config, file, indent=4, ensure_ascii=False)


class AnkiCommunicator:
    def __init__(self):
        self.base_url = 'http://localhost:8765'


    def get_words_in_n_days(self, n, deck_name) -> list:
        card_ids = self.__get_cards_id_in_n_days(n)
        if not card_ids:
            return []
        cards_info = self.__invoke('cardsInfo', {'cards': card_ids})
        result_list = [self._extract_card_id_from_field(card['fields']['Back']['value']) for card in cards_info if card and card['deckName'] == deck_name]
        return result_list

    
    def get_words_for_today(self, deck_name) -> list:
        query = f'deck:"{deck_name}" is:due'
        card_ids = self.__invoke('findCards', {'query': query})
        if not card_ids:
            return []
        cards_info = self.__invoke('cardsInfo', {'cards': card_ids})
        result_list = [self._extract_card_id_from_field(card['fields']['Back']['value']) for card in cards_info if card and card['deckName'] == deck_name]
        return result_list


    def get_words_for_tomorrow(self, deck_name) -> list:
        query = 'prop:due=1'
        card_ids = self.__invoke('findCards', {'query': query})
        if not card_ids:
            return []
        cards_info = self.__invoke('cardsInfo', {'cards': card_ids})
        result_list = [self._extract_card_id_from_field(card['fields']['Back']['value']) for card in cards_info if card and card['deckName'] == deck_name]
        return result_list


    def _extract_card_id_from_field(self, input_string):
        matches = re.findall(r'<i>(.*?)</i>', input_string)
        assert matches, 'No word found in the card'
        return matches[0]
    

    def __get_request(self, action, params):
        return {'action': action, 'params': params, 'version': 6}


    def __invoke(self, action, params):
        data = json.dumps(self.__get_request(action, params))
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.base_url, data=data, headers=headers)
        response_json = response.json()
        if 'error' in response_json and response_json['error']:
            raise Exception(f'Failed to fetch card info: {response_json["error"]}')
        return response_json['result']


class AnkiCardWriter(ABC):
    '''
    The writer takes a list of word entries as an input. The user can use the method `write_cards` to create a csv file that are suitable for Anki imports.
    '''
    def __init__(self, stack: dict):
        self.stack = stack
        self.anki_cards_front : list[str] = []
        self.anki_cards_back : list[str] = []
        self.Anki_cards_string: list[list[str]] = []


    def write_cards(self, csv_path = str, shuffle_cards=True):
        self.anki_cards_front, self.anki_cards_back = self._write_cards(self.stack)
        for i in range(len(self.anki_cards_front)):
            self.Anki_cards_string.append([self.anki_cards_front[i], self.anki_cards_back[i]])
        if shuffle_cards:
            random.shuffle(self.Anki_cards_string)
        with open(csv_path, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(self.Anki_cards_string)

    @abstractmethod
    def _write_cards(self, stack: dict):
        pass

    

class PassiveAnkiCardWriter(AnkiCardWriter):
    def __init__(self, stack):
        super().__init__(stack)

    def _write_cards(self, stack: dict):
        '''
        Updates the list `self.Anki_cards`.
        '''
        anki_card_front = []
        anki_card_back = []
        for card_id in stack:
            front = ''
            back = '<i>' + card_id + '</i>' + '<br>' + '<br>'
            word = stack[card_id]['word']
            forms = stack[card_id]['forms']
            definition = stack[card_id]['definition']
            Chinese_def = stack[card_id]['Chinese']
            examples = stack[card_id]['examples']
            part_of_speech = stack[card_id]['part of speech']
            pronunciation = stack[card_id]['British received pronunciation']
            front += '<b>' + word + '</b>' + '<br>' + '<br>'
            for example in examples:
                front += '<i>' + example['English'] + '</i>' + '<br>'
            back += (part_of_speech + '<br>' + '<br>') if part_of_speech else ''
            back += '/' + pronunciation + '/' + '<br>' + '<br>' if pronunciation else ''
            back += (forms + '<br>' + '<br>') if forms else ''
            back += definition
            back += '<br>' + '<br>' + Chinese_def + '<br>' + '<br>'
            anki_card_front.append(front)
            anki_card_back.append(back)
        return anki_card_front, anki_card_back
    
    
class ActiveAnkiCardWriter(AnkiCardWriter):
    def __init__(self, stack):
        super().__init__(stack)

    def _write_cards(self, stack: dict):
        '''
        Updates the list `self.Anki_cards`.
        '''
        anki_card_front = []
        anki_card_back = []
        for card_id in stack:
            front = ''
            back = '<i>' + card_id + '</i>' + '<br>' + '<br>'
            word = stack[card_id]['word']
            definition = stack[card_id]['definition']
            assert len(stack[card_id]['examples']) > 0, f'No examples found for the word {word}'
            example = stack[card_id]['examples'][0]
            front += example['Chinese'] + '<br>' + '<br>'
            back += example['English'] + '<br>' + '<br>'
            back += '<b>' + word + '</b>' + '<br>' + '<br>'
            back += '<i>' + definition + '</i>'
            anki_card_front.append(front)
            anki_card_back.append(back)
        return anki_card_front, anki_card_back


class StackOrganizer:
    def __init__(self, stack: dict, only_single_word=False, only_multiple_word=False):
        self.stack = deepcopy(stack)
        self.only_single_word = only_single_word
        self.only_multiple_word = only_multiple_word
        assert not (only_single_word and only_multiple_word), 'You cannot set both only_single_word and only_multiple_word to True.'

    def reorganize(self):
        return self._reorganize(self.stack, only_single_word=self.only_single_word, only_multiple_word=self.only_multiple_word)

    def _reorganize(self, stack: dict, only_single_word: bool, only_multiple_word: bool):
        result = {}
        for card_id in stack:
            word = stack[card_id]['word']
            word_count = len(word.split(' '))
            if only_single_word and word_count > 1:
                continue
            if only_multiple_word and word_count == 1:
                continue
            if word not in result:
                result[word] = []
            result[word].append(stack[card_id])
        return result