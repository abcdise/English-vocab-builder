fill_in_the_gap_prompt = r'''You are given a list of JSON files, each containing two terms and their definitions. For each file, write three sentences describing a life scene: the first sentence should introduce the topic, the second sentence should contain the first term, and the third sentence should contain the second term. These sentences should follow each other seamlessly, creating a logical flow that improves comprehension. Use a conversational tone. Always follow the rules of British English spelling in your response. Use the following format for your response:
```json
[{"words": ["word 1", "word 2"], "definitions": ["definition 1", "definition 2"], "sentences": "write three sentences here"}]
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

sentence_correction_prompt = r'''Help me identify common collocation errors made by English learners. You will be provided a list of words along with their collocations in the following structure
```
[{"word": "", "pattern":{"key": "", "usage": "", "example": ""}}]
```
Your task is to extend the json file. Format your response in the following structure:
```json
[{"word": "provided word",  "pattern": {provided pattern}, "incorrect pattern": {"key": "an alternative key that an English learner might mistakenly use in the provided example", "usage": "an incorrect variant of the provided usage", "example": "Replace the original key with the improper keys in the provided example. Ensure the example is not idiomatic in English in ANY context.", "explanation": "Provide a brief explanation of why the incorrect pattern is not idiomatic in English, irrespective of the context."}}]
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


collocation_prompt = r'''Help me identify common collocation errors made by German speakers in English. You will be provided a list of words along with their collocations in the following structure
```
[{"word": "", "key": "", "example": ""}]
```
Your task is to extend the JSON file with possible collocation errors commonly made by German speakers in English. Format your response in the following structure:
```json
[
    {  
        "word": "provided word",  
        "key": "provided key",  
        "example": "provided example",  
        "improper keys": ["List two plausible alternatives to the provided key that a German speaker might mistakenly use in the provided example. These should reflect common linguistic patterns, such as direct translations from German or overgeneralised English grammar rules."],  
        "improper examples": ["Replace the original key with the improper keys in the provided example. Ensure these examples not idiomatic in English in ANY context. Do not list correct collocations as errors."]
        "explanation": "Provide a brief explanation of why the three keys are not idiomatic in English, irrespective of the context."
    }  
]

```
Your response should adhere to British English spelling conventions.
Input:
'''
