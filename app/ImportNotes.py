import sys
sys.path.insert(1, '../src')
from Stack import Stack
import json


category_index = input('''Select category: 
                 1. Vocab Builder''')

if int(category_index) == 1:
    category = 'Vocab Builder'


with open('../src/paths.json') as f:
    paths = json.load(f)

schedule_path = paths[category]['schedule']
cards_path = paths[category]['cards']
notes_paths = paths[category]['notes']

stack = Stack(schedule_path=schedule_path, cards_path=cards_path)
stack.import_cards(json_path=notes_paths)