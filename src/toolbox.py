import json
from pathlib import Path
from copy import deepcopy
import requests
from numpy import random
import csv
import re


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
        self.config['unlearned'] += self.config['learned']
        self.config['learned'] = []
        self.__export()

    
    def get_n_words_to_learn(self, n:int):
        list_to_return = self.config['unlearned'][:n]
        if len(list_to_return) < n:
            print(f'Only {len(list_to_return)} words left to learn')
        return list_to_return
    

    def study_n_words(self, n:int):
        new_list = self.config['unlearned']
        review_list = self.config['learned']
        new_word_list = self.get_n_words_to_learn(n)
        review_list += new_word_list
        new_list = [word for word in new_list if word not in new_word_list]
        self.config['learned'] = deepcopy(review_list)
        self.config['unlearned'] = deepcopy(new_list)
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
        return self.get_words_in_n_days(0, deck_name)


    def get_words_for_tomorrow(self, deck_name) -> list:
        return self.get_words_in_n_days(1, deck_name)


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


    def __get_cards_id_in_n_days(self, n):
        query = f'prop:due={n}'
        response = self.__invoke('findCards', {'query': query})
        return response



class AnkiCardWriter:
    '''
    The writer takes a list of word entries as an input. The user can use the method `write_cards` to create a csv file that are suitable for Anki imports.
    '''
    def __init__(self, stack: dict):
        self.stack = stack
        self.Anki_cards_string = []


    def write_cards(self, csv_path = str, shuffle_cards=True):
        self.__write_cards(self.stack)
        if shuffle_cards:
            random.shuffle(self.Anki_cards_string)
        with open(csv_path, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(self.Anki_cards_string)


    def __write_cards(self, stack: dict):
        '''
        Updates the list `self.Anki_cards`.
        '''
        for card_id in stack:
            anki_card = []
            front = ''
            back = '<i>' + card_id + '</i>' + '<br>' + '<br>'
            word = stack[card_id]['word']
            forms = stack[card_id]['forms']
            definition = stack[card_id]['definition']
            Chinese = stack[card_id]['Chinese']
            examples = stack[card_id]['examples']
            part_of_speech = stack[card_id]['part of speech']
            front += '<b>' + word + '</b>' + '<br>' + '<br>'
            for sentence in examples:
                front += '<i>' + sentence + '</i>' + '<br>'
            back += (part_of_speech + '<br>' + '<br>') if part_of_speech else ''
            back += (forms + '<br>' + '<br>') if forms else ''
            back += definition
            back += '<br>' + '<br>' + Chinese + '<br>' + '<br>'
            anki_card.append(front)
            anki_card.append(back)
            self.Anki_cards_string.append(anki_card)

    