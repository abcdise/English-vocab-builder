fill_in_the_gap_prompt = r'''You are given a list of JSON files, each containing two terms and their definitions. For each file, create a dialogue consisting of two exchanges between two Britons. The first man should use the first term, while the second man should use the second term. Follow the rules of British English spelling in your response. Use the following format for your response:

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


sentence_correction_prompt = r'''Assist in developing multiple choice questions for the English exam by identifying common pattern errors in English. You will receive a list of words with their usage patterns.
Your task is to generate multiple-choice questions that test students' understanding of the correct usage of these words. For each word, you should:
1. Provide two consecutive new example sentences, where the first sentence introduces context and the second sentence correctly demonstrates the given usage pattern.
2. Identify a plausible incorrect usage pattern for the word.
3. Create a question with a gap in the sentence where the word is used, and provide two answer options: one correct and one incorrect.
Ensure your response adheres to the British English spelling conventions. 
Example inputs:
```
[{"word": "remind", "pattern":{"usage": "someone reminds someone of something", "example": "Please remind me of the money tomorrow."}}]
```
Example outputs:
```json
[
  {
    "word": "remind",
    "provided usage": "someone reminds someone of something", 
    "new example": "I happened to see Anna this evening. She reminded me of her mother.",
    "incorrect usage": "someone reminds someone with something",
    "question": "I happened to see Anna this evening. She [gap] her mother.",
    "options": ["reminded me of", "reminded me with"]
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
[{"word": "provided word", "key": "provided key","new example": "new example sentence", "matching part": "pinpoint the part of the new example sentence that corresponds to the collocation of the provided word"}]
```

Try the following:
'''

dialogue_completion_prompt = r'''You will be provided with a list of JSON objects, each containing a term, its definition, and an example sentence. Your task is to create Dialogue Completion questions based on the given data. For each JSON object, perform the following steps:

1. Write a dialogue: Create a natural-sounding dialogue between two Britons that includes two exchanges and uses the given term correctly in context.
2. Identify the matching part: Pinpoint the part of the sentence in the dialogue that corresponds to the given term. This part will later be converted into a gap for the test.
3. Write a hint: Write a hint by rephrasing the matching part in a more detailed or descriptive way to help users understand its meaning.

Ensure your responses strictly follow British spelling conventions and are formatted in JSON structure as shown in the example below.

Example inputs:
```json
[{"term": "go with sth.", "definition": "If you say you will go with a dish, you mean you will order it.", "example": "I'll go with the steak."}]
```
Example outputs:
```json
[{"term": "go with sth.", "definition": "If you say you will go with a dish, you mean you will order it.","dialogue": ["What would you like to order?","I think I'll go with the fish and chips."],"matching part": "go with the fish and chips"}, hint: "order fish and chips"]
```

Try the following:
'''
