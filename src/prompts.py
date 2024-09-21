example_sentences_prompt = r'''Generate two example sentences for each term and definition below. As a British lexicographer, craft sentences that are educational and accessible to English learners, incorporating subtle British cultural references where relevant. Ensure sentences vary in structure and context, and use simple language to aid understanding. Format your response as a JSON block.

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
        "Example": ["After the test, I was positive that I had passed.", "I am positive that I locked the door before I left the house."]
    }, {
        "Definition": "A positive number is greater than zero.",
        "Example": ["The number 5 is positive."]
    }],
    "remote": [{
        "Definition": "Remote areas are far away from cities and towns.",
        "Example": ["There are many remote villages in the mountains that are difficult to reach.", "The house is so remote that you can't even see the neighbours."]
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

inference_options_prompt = r'''
Now try the following:
'''

translation_prompt = r'''Given a list of terms and their definitions, write a clear, concise sentence using only subject, predicate, and object without additional details, which demonstrates the word's meaning. Ensure your sentences follow British English spelling conventions. Then, translate each sentence into colloquial Chinese, prioritising natural and authentic flow over literal accuracy. The translations should mimic casual conversation, even if slight adaptations of the original meaning are necessary to achieve this.

Example input:
```json
{
    "tasty": ["If you say that food, especially savoury food, is tasty, you mean that it has a fairly strong and pleasant flavour which makes it good to eat."]
}
```
Example response:
```json
{
    "tasty": [
        {
            "Definition": "If you say that food, especially savoury food, is tasty, you mean that it has a fairly strong and pleasant flavour which makes it good to eat.",
            "Example": "The food is tasty.",
            "Colloquial Chinese": "东西很好吃。"
        }
    ]
}
```
'''

comprehension_prompt = r'''Given a list of words with their definitions, write a short question using the word, whose answer is Yes. Then write a short question using the word, whose answer is No. 

Your audience are British primary school pupils. Ensure that they are able to answer the questions using only their knowledge of the definitions of the words, without any other expertise. Ensure both sentences use present tense and adhere to spelling conventions of British English. Format your output as a JSON code block.

Example input:
```
{
    "teach": ["If you teach someone something, you are helping them to learn about it."],
    "lazy": ["If someone is lazy, they do not want to work or make any effort to do anything."]
}
```
Example response:
```json
{
    "teach": [
        {
            "Definition": "If you teach someone something, you are helping them to learn about it.",
            "Yes Question": "Do you teach the grammar rules to your students by providing examples?",
            "No Question": "Does a father teach her son to swim by forbidding him to go near the water?"
        }
    ],
    "lazy": [
        {
            "Definition": "If someone is lazy, they do not want to work or make any effort to do anything.",
            "Yes Question": "Does a lazy student like finishing his homework early?",
            "No Question": "Is a lazy person hardworking?"
        }
    ]
}
```
'''

sentence_order_prompt = r'''
For each keyword-definition pair, write a piece of news in the UK consisting of three sentences. One of the sentences must contain the keyword. Use the following format in your response:
`{"keyword": [{"Definition": "", "Paragraph": ["First sentence", "Second sentence", "Third sentence"]}]}`
Ensure the paragraphs use British English spelling.
'''