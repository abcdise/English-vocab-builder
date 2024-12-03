fill_in_the_gap_prompt = r'''You are given a list of JSON files, each containing two terms and their definitions. For each file, write three sentences describing a scene: the first sentence should contain the first term, and the second sentence should contain the second term. Use a straightforward tone. Always follow the rules of British English spelling in your response. Use the following format for your response:
```json
[{"words": ["word 1", "word 2"], "definitions": ["definition 1", "definition 2"], "sentences": "write the sentences here"}]
```

Input:
'''

reading_prompt = r'''You will be provided with a list of JSON files, where each file contains a word and its definition. Your task is to write a detailed diary entry in one paragraph that incorporates all the words. Ensure each word appears only once in your diary. Before writing the diary, create a clear outline to organise your thoughts. Use a conversational and straightforward tone in your writing, adhering to British English spelling conventions. Format your response as follows:
```json
{
  "words": [list all the words here],
  "outline": "write the diary outline here",
  "diary": "write the diary entry here"
}
```

Input:
'''

sentence_completion_prompt = r'''You will be provided with a list of phrases. Your task is to write a full sentence for each given phrase. The sentence should adhere to British English spelling conventions. Format your response as follows:
```json
[{"phrase": "write the phrase", "sentence": "write the sentence containing the phrase"}]
```

Input:
'''

sentence_correction_prompt = r'''Help me identify common pattern errors made by English learners. You will be provided with a list of words along with their usage patterns using the following structure:
```
[{"word": "", "pattern":{"usage": "", "example": ""}}]
```
Your task is to extend the json file. Format your response in the following structure:
```json
[
  {
    "word": "provided word",
    "pattern": {provided pattern},
    "incorrect pattern": {
      "usage": "a variant of the provided usage containing grammatical errors, such as incorrect prepositions, confusion between transitive and intransitive verbs, or mixing up infinitives and gerunds. Be creative in inventing errors.",
      "example": "Rewrite the provided example using the incorrect usage."
    }
  }
]
```
Your response should adhere to British English spelling conventions.

Input:
'''

multiple_choice_prompt = r'''You are a BBC radio presenter. Help me identify words with similar received pronunciations (RP). You will be provided with a list of words with the following structure:
```
[{"word": "", "definition": "", "received pronunciation": ""}]
```
Your task is to extend the json file. Format your response in the following structure:
```json
[{"word": "provided word", "definition": "provided definition", "received pronunciation": "provided pronunciation", "sentence": "Write a sentence using the provided word in its original form, reflecting its given definition.", "similar words": [List three words whose pronunciations share some syllables with the provided word but have different meanings.], "similar received pronunciations": [Write the RPs for the three similar words.]}]
```

Input:
'''


collocation_prompt = r'''Help me identify common collocation errors in English. You will be provided a list of words along with their collocations in the following structure
```
[{"word": "", "key": "", "example": ""}]
```
Your task is to extend the JSON file with collocation errors. Format your response in the following structure:
```json
[
    {
        "word": "provided word",
        "key": "provided key",
        "example": "provided example",
        "improper keys": ["Identify two synonyms of the provided key that, when used to replace the key in the provided example, result in clear collocation errors. Be creative in your choices."],
        "improper examples": ["Replace the original key in the example with the incorrect keys."]
    }
]
```

Your response should adhere to British English spelling conventions.
Input:
'''
