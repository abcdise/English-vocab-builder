import json


class Stack:
    def __init__(self, schedule_path:str, cards_path:str):
        self.schedule_path = schedule_path
        self.cards_path = cards_path
        with open(schedule_path) as file:
            self.schedule = json.load(file)
        with open(cards_path) as file:
            self.cards = json.load(file)
    
    
    def import_cards(self, json_path:str):
        '''
        Import the cards from the JSON file and update the cards in the stack
        '''
        with open(json_path) as file:
            new_cards = json.load(file)
        
        # Check if every card in new_cards is not in self.cards and not in the schedule
        assert all([card_id not in self.cards for card_id in new_cards]), 'Some cards already exist in the stack'
        assert all([card_id not in self.schedule['learned'] and card_id not in self.schedule['unlearned'] for card_id in new_cards]), 'Some cards already exist in the schedule'

        # Update the cards in the stack
        self.cards.update(new_cards)

        # Update the schedule
        self.schedule['unlearned'].extend(new_cards.keys())

        # Write the updated cards and schedule back to the JSON file
        with open(self.cards_path, 'w') as file:
            json.dump(self.cards, file, indent=4, ensure_ascii=False)

        with open(self.schedule_path, 'w') as file:
            json.dump(self.schedule, file, indent=4, ensure_ascii=False)

        print('==== Import successful ====')



    
