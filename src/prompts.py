fill_in_the_gap_prompt = r'''You are given a list of JSON files, each containing two terms and their definitions. For each file, write three sentences: the first sentence should introduce the topic, the second sentence should contain the first term, and the third sentence should contain the second term. These sentences should follow each other seamlessly, creating a logical flow that improves comprehension. Use a conversational tone. Always follow the rules of British English spelling in your response. Use the following format for your response:
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

sentence_correction_prompt = r'''You will receive a list of words, each accompanied by its definition and usage patterns. For each usage pattern, do the following:
1. Write a grammatically correct sentence that demonstrates the pattern.
2. Write an incorrect sentence that violates the pattern (e.g., misuse of prepositions, omission of necessary words, or confusion between verb forms such as "to do" vs. "doing"). 
Format your response using the following structure:
```json
[{"word": "write the word", "definition": "write the definition", "pattern": "write the pattern", "correct sentence": "write the correct sentence here", "incorrect sentence": "write the incorrect sentence here"}]
```

Input:
'''

multiple_choice_prompt = r'''You will be provided with a list of words, along with their definitions and received pronunciations (RP). For each word, perform the following tasks:
1. Write a sentence using the word in its original form, reflecting its given definition.
2. Identify three other words whose pronunciations share some syllables with the original word but have different meanings.
3. Write the RPs for these three different words.
Follow British English spelling conventions when composing the sentences. Format your response as follows:
```json
[{"word": "write the word", "definition": "write the definition", "received pronunciation": "write the pronunciation of the word", "sentence": "write the sentence using the word", "other words", ["word 1, "word 2", "word 3"], "other received pronunciations": ["pronunciation 1", "pronunciation 2", "pronunciation 3"]}]
```

Input:
'''
