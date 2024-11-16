example_sentences_prompt = r'''Generate one example sentence for each term and definition below. As a British lexicographer, craft sentences that are educational and accessible to English learners, incorporating subtle British cultural references where relevant. Ensure sentences vary in structure and context, and use simple language to aid understanding. Format your response as a JSON block.

Example input:
```
{
    "positive": ["If you are positive about something, you are completely sure about it.", "A positive number is greater than zero."],
    "remote": ["Remote areas are far away from cities and towns."]
}
```

Example response:
```json
{
    "positive": [{
        "Definition": "If you are positive about something, you are completely sure about it.",
        "Example": "I am positive that I locked the door before I left the house."
    }, {
        "Definition": "A positive number is greater than zero.",
        "Example": "The number 5 is positive."
    }],
    "remote": [{
        "Definition": "Remote areas are far away from cities and towns.",
        "Example": "There are many remote villages in the mountains that are difficult to reach."
    }]
}
```
'''

dialogue_exercise_prompt = r'''As a British lexicographer, your task is to generate brief example dialogues containing only two exchanges between two characters for the given terms. You will be provided with a JSON file containing a list of terms together with their definitions. For each term, write the dialogue in British English. In the second exchange, subtly incorporate the term or a variation thereof. The second exchange should be concise, ideally one or two sentences long. Following the dialogue, rephrase the second exchange without using the term. Keep the rephrased sentence as identical to the original sentence as possible. Finally, insert a keyword from the term in the field "Keyword". 
Example input:
```json
{"remind sb. of sth.": "If someone reminds you of a fact or event that you already know about, they say something which makes you think about it."}
```
Example output:
```json
{
"remind sb. of sth.":{
  "A": "Hey, have you ever been to that new café downtown?",
  "B": "Yeah, it actually reminds me of that little coffee shop we used to go to in college.",
  "Paraphrase": "Yeah, it is actually quite similar to that little coffee shop we used to go to in college.",
  "Keyword": "remind"
}
}
```
'''

phrase_def_prompt = r'''You are a renowned British lexicographer. Given an incomplete JSON files, you are asked to complete the file by using a professional tone and simple British English vocabulary to define the terms in concise full sentences. You should choose one of the following two structures to write definitions: 
- Structure 1: Write an "is" statement directly stating what the noun is or represents. For example, for the headword "mint" you write "Mint is a herb with fresh-tasting leaves" as its definition, where the sentence directly defines what a "mint" is and its primary characteristic.
- Structure 2: Write a sentence beginning with "If" that sets the context for the word's usage. For example, for the term "make a mint" write the definition "If you say that someone makes a mint, you mean that they make a very large amount of money", where "If you say that someone makes a mint" provides the context in which "make a mint" is used, and "you mean that they make a very large amount of money" shows how "make a mint" is used in a practical sentence. 
Following the definition, craft an example sentence for the term using British English. Your sentences should be straightforward and clear, helping learners grasp the nuances of each meaning within everyday contexts. Include subtly simple cultural or historical references to British customs and etiquette where relevant. 
Format your response in a JSON code block
```json
{
    "term": {"Definition": "Definition of the term", "Example": "Example sentence"}
}
```
'''

cloze_prompt = r'''For each of the given passages, you should create a cloze test with 3 questions in the form of a JSON code block. Do the following:
1. Select three phrases from each passage and place them in the 'Phrase' field. 
2. For each collocation, place the keyword in the 'Word' field. 
3. Find three words that can replace the keyword but will change the meaning of the phrase substantially. Place these words in the 'Incorrect options' field. Ensure these words are written in British English, and don't have similar connotations (commendatory or derogatory) to each other.
Example input:
["The ancient castle stood proudly atop the hill. Its towering walls were adorned with intricate carvings that told stories of centuries past. The castle's grandeur attracted tourists from all over the world."]

Example output:
```json
{
  "The ancient castle stood proudly atop the hill. Its towering walls were adorned with intricate carvings that told stories of centuries past. The castle's grandeur attracted tourists from all over the world.": [
    {"Word": "ancient", "Phrase": "ancient castle", "Incorrect options": ["shabby", "artificial", "mythical"]},
    {"Word": "adorned", "Phrase": "were adorned with", "Incorrect options": ["satisfied", "supported", "bored"]},
    {"Word": "attracted", "Phrase": "attracted tourists", "Incorrect options": ["saved", "disappointed", "ignored"]}
  ]
}
```
Here are the passages:
'''

inference_example_prompt = r'''
Now try the following:
'''

collocation_prompt = r'''Generate a JSON file for each provided word and its definition(s) with the following structure:
```json
{
  "word 1": [
    {
      "Definition": "Provided definition",
      "Correct example": "correct phrase",
      "Error": "Type of error",
      "Replace": "part to replace",
      "Incorrect examples": ["incorrect phrase 1", "incorrect phrase 2", "incorrect phrase 3"]
    }
  ],
  "word 2": ...
}
```
Instructions:
1. `Correct example` field: a concise phrase starting with 'to' that accurately encapsulates the word's definition
2. `Error` field: Specify the type of error present in the incorrect phrases.
    a) collocational errors (e.g. word: `acutely`, incorrect phrase: `to become acutely happy`)
    b) prepositional errors (e.g. word: `remind`, incorrect phrase: `to remind Tom about the meeting`)
    c) contextual errors (e.g. word: `write`, incorrect phrase: `to write an apple`)
3. `Replace` field: the words that should be replaced in the correct example to create the incorrect examples
4. `Incorrect examples` field: a list of three short phrases after replacing the words in the `Replace` field. These phrases should contain errors of the type specified in the `Error` field.
4. Ensure all phrases contain the keyword and conform to British English spelling conventions.
Example:
```json
{
  "remind": [
        {
            "Correct example": "If you remind someone of something, you make them remember it.",
            "Error": "prepositional errors",
            "Replace": "of",
            "Incorrect examples": ["to remind him about the meeting", "to remind him to the meeting", "to remind him from the meeting"]
        }
    ]
}
```
'''

translation_prompt = r'''For each term in the given list, first use a conversational tone to expand the phrase in `Chinese` into a short sentence. Refine the Chinese sentence so that it sounds natural. Then update the English translation in `English` to match the modification. Ensure the response follows British English spelling conventions. Format your response in a JSON code block.
Example input:
```json
{"take part in": [{"Chinese": "参加学校的戏剧表演", "English": "take part in the school play"}]}
```
Example response:
```json
{
  "take part in": [
    {"Chinese": "你明天要参加学校的戏剧表演吗？", "English": "Are you going to take part in the school play tomorrow?"}
  ]
}
```
'''

comprehension_prompt = r'''For each definition of each word, write a concise question with the correct application of the word, whose answer is Yes. Then write a concise question using the word, whose answer is No because the meaning of the word is distorted. Formulate both questions beginning with `be` or `do`.

Your audience are British sixth form students. Ensure that they are able to answer the questions using only their knowledge of the definitions of the words, without any other expertise. Ensure both sentences use present tense and adhere to spelling conventions of British English. Format your output as a JSON code block.

Example input:
```
{
    "deal": ["If you deal with something, you take action in order to solve a problem."],
    "lazy": ["If someone is lazy, they do not want to work or make any effort to do anything."]
}
```
Example response:
```json
{
    "deal": [
        {
            "Definition": "If you deal with something, you take action in order to solve a problem.",
            "Yes Question": "Do you deal with a problem by taking action?",
            "No Question": "Do you deal with a problem by ignoring it?"
        }
    ],
    "lazy": [
        {
            "Definition": "If someone is lazy, they do not want to work or make any effort to do anything.",
            "Yes Question": "Is someone lazy if they do not want to work?",
            "No Question": "Is someone lazy if they work hard?"
        }
    ]
}
```
'''

sentence_order_prompt = r'''For each definition of each keyword, write a story in the British history consisting of four elaborate sentences. Only one of the sentences should contain the keyword. Use a straightforward tone. Ensure the four sentences are coherent. Use the following format in your response:
```json
{"keyword": [{"Definition": "", "Paragraph": ["First sentence", "Second sentence", "Third sentence", "Fourth sentence"]}]}
```
Ensure the paragraphs use British English spelling.
'''

spelling_prompt = r'''Create a JSON file by following the instructions. For each definition of each given word, think of another word with resemblance in sound with the given word, especially in initial and final syllables. Then write a question asking which variant is correct, whose answer is the original word. Begin the question with a short sentence describing of a scenario. Ensure the questions adhere to spelling conventions of British English.

Structure the JSON as follows:
1. Use the original word as the key.
2.  For each definition, create an object with these fields:
- "Definition": The provided definition.
- "Question": The scenario-based question.
- "Options": An array with the original word and the similar-sounding word.
- "Answer": The original word.

Example input:
```
{"remind": ["If something reminds you of a fact or event, it makes you think about it."]}
```
Example response:
```json
{
    "remind": [
        {
            "Definition": "If something reminds you of a fact or event, it makes you think about it.",
            "Question": "You opened the drawer and saw an old diary of yours. Has the diary reminded or rewinded you of your childhood?",
            "Options": ["reminded", "rewinded"],
            "Answer": "reminded"
        }
    ]
}
```
'''

translation_prompt_2 = '''Generate a JSON file for each provided word and its definition(s) with the following structure:
```json
{
  "word 1": [
    {
      "Definition": "Provided definition",
      "Chinese definition": "Chinese definition",
      "Chinese sentence": "Chinese sentence"
    }
  ],
  "word 2": ...
}
```
Instructions:
1. `Chinese definition` field: a Chinese definition of the word
2. `Chinese sentence` field: a Chinese sentence containing the Chinese definition
'''