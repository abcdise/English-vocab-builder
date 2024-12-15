class VocabNotes:
    def __init__(self, word_entries:dict):
        self.word_entries = word_entries
        keys = ['notes']
        self.notes_dict = dict.fromkeys(keys)
        self.write_notes()


    def get_outputs(self):
        return self.notes_dict


    def write_notes(self):
        entries = self._format_notes(self.word_entries)
        def_text = ''
        for entry in entries:
            for note in entry:
                word = note['word']
                part_of_speech = note['part of speech']
                definition = note['definition']
                forms = note['forms']
                collocations = note['collocations']
                examples = note['examples']
                patterns = note['patterns']
                explanation = note['explanation']
                pronunciation = note['British received pronunciation']
                def_text += '\\Vocabulary{' + word + '}'
                def_text += '{' + part_of_speech + '}'
                def_text += '{/' + pronunciation + '/}' if pronunciation else '{}'
                def_text += '{' + forms + '}'
                def_text += '{' + definition + '}'
                def_text += '{' + explanation + '}'
                def_text += '{'
                items_1 = []
                for example in examples:
                    items_1.append((example['English'], example['Chinese']))
                for category in collocations:
                    for collocation in collocations[category]:           
                        items_1.append((collocation['example']['English'], collocation['example']['Chinese']))
                items_2 = []
                for pattern in patterns:
                    if pattern:
                        items_2.append((pattern['usage'], pattern['example']['English'], pattern['example']['Chinese']))
                for item in items_2:
                    def_text += '\\item ' + self._string_processing(item[0]) + '\n\\begin{displayquote}' + self._string_processing(item[1]) + '\n\n' + item[2] + '\n\\end{displayquote}\n'
                for item in items_1:
                    def_text += '\\item ' + self._string_processing(item[0]) + '\n\n' + item[1] + '\n'
                def_text += '}'
        self.notes_dict['notes'] = def_text


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
            if word.endswith('"'):
                word = word[:-1] + "''"
            text_list_new.append(word)
        return ' '.join(text_list_new)


    def __replace_pounds(self, text):
        return text.replace('£', r'\pounds')


    def __replace_en_dashes(self, text):
        return text.replace('–', '--')


    def _format_notes(self, word_entries:dict):
        notes = []
        for _, entry in word_entries.items():
            notes.append(entry)
        return notes