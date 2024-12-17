fill_in_the_gap_prompt = r'''You are given a list of JSON files, each containing two terms and their definitions. For each file, create a dialogue consisting of two exchanges between two British men. The first man should use the first term, while the second man should use the second term. Follow the rules of British English spelling in your response. Use the following format for your response:

```json
[{"words": ["word 1", "word 2"], "definitions": ["definition 1", "definition 2"], "background": "brief description of the background of the conversation", "conversation": ["what A says", "what B says"]}]
```

Try the following:
'''

reading_prompt = r'''You will be provided with a list of JSON files, where each file contains a word and its definition. Your task is to write a detailed diary entry in one paragraph that incorporates all the words. Ensure each word appears only once in your diary. Before writing the diary, create a clear outline to organise your thoughts. Use a conversational and straightforward tone in your writing, adhering to British English spelling conventions. Format your response as follows:
```json
{
  "words": [list all the words here],
  "outline": "write the diary outline here",
  "diary": "write the diary entry here"
}
```

Try the following:
'''


sentence_correction_prompt = r'''Assist in developing Sentence Correction questions for the upcoming SAT exam by identifying and expanding upon common pattern errors in English. You will receive a list of words with their usage patterns, structured as follows:
```
[{"word": "", "pattern":{"usage": "", "example": ""}}]
```
Your task is to extend the json file. Ensure your response adheres to the British English spelling conventions. Format your response in the following structure:
```json
[
  {
    "word": "provided word (e.g. remind)",
    "provided usage": "provided usage (e.g. someone reminds someone of something)", 
    "incorrect usage": "altered provided usage with grammatical error. For example, use a transitive verb intransitively, or modify an infinitive to a gerund. Be creative in crafting errors.(e.g. someone reminds someone with something)",
      "correct sentence": "a entirely new sentence using the provided pattern. (e.g. Anna reminds me of her mother.)",
"incorrect sentence": "Make minor modification to the new sentence to introduce the incorrect pattern (e.g. Anna reminds me with her mother.)"
    }
  }
]
```

Try the following:
'''

multiple_choice_prompt = r'''You are a BBC radio presenter. Help me identify words with similar British received pronunciations (RP). You will be provided with a list of words with the following structure:
```
[{"word": "", "definition": "", "British received pronunciation": ""}]
```
Your task is to extend the json file. Format your response in the following structure:
```json
[{"word": "provided word", "definition": "provided definition", "British received pronunciation": "provided pronunciation", "sentence": "Write a sentence using the provided word in its original form.", "similar words": [List three words whose pronunciations share some syllables with the provided word but have different meanings.], "similar received pronunciations": [Write the RPs for the three similar words.]}]
```

Try the following:
'''


collocation_prompt = r'''You will be provided with a list of words, a "key" (a word that collocates correctly with the given word), and an example sentence in the following format:
```json
[{"word": "", "key": "", "example": ""}]
```

Based on the given sentence, write a sentence where the "word" is paired with the correct "key". Use British English spelling and grammar conventions throughout your response. Provide your response in the following JSON structure:
```json
[{"word": "provided word", "key": "provided key","new example": "new example sentence", "where": "quote the collocation in the new example"}]
```

Try the following:
'''
