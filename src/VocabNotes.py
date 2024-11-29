class VocabNotes:
    def __init__(self, word_entries:dict):
        self.word_entries = word_entries
        keys = ['notes']
        self.notes_dict = dict.fromkeys(keys)


    def write_notes(self):
        notes_list = self._format_notes(self.word_entries)
        def_text = ''
        for note in notes_list:
            word = note['word']
            part_of_speech = note['part of speech']
            definition = note['definition']
            forms = note['forms']
            chinese_definition = note['Chinese']
            collocations = note['collocations']
            examples = note['examples']
            def_text + r'\Vocabulary{' + note['word'] + '}'
        
        self.notes_dict['notes'] = def_text


    def _format_notes(self, word_entries:dict):
        notes = []
        for _, entry in word_entries.items():
            notes.append(entry)
        return notes