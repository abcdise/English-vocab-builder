### Sentence analysis
You are a British lexicographer. Please complete the JSON file provided. In the field `Excerpt`, insert a collocation from the original sentence that includes the headword. Ensure that the collocation extends the headword by two or three additional words. For the field `Paraphrase`, rephrase the sentence in British English, avoiding the use of the headword. Finally, select a word from the headword to insert in the field `Keyword`. Below is an illustrative example:
Given the input
```json
{"recognise": [{"Sentence": "He had the insight to recognise their talents.", "Excerpt": "", "Keyword": "", "Paraphrase": ""}]}
```
Your response should be as follows:
```json
{
"recognise": [
    {
        "Sentence": "He had the insight to recognise their talents.",
        "Excerpt": "recognised their talents",
        "Keyword": "recognise",
        "Paraphrase": "He possessed the foresight to acknowledge their skills.",
    }
]
}
```


### Example sentences
Generate two example sentences for each term and definition below. As a British lexicographer, craft sentences that are educational and accessible to English learners, incorporating subtle British cultural references where relevant. Ensure sentences vary in structure and context, and use simple language to aid understanding. Format your response as a JSON block.

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
        "Example": "The number 5 is positive."
    }],
    "remote": [{
        "Definition": "Remote areas are far away from cities and towns.",
        "Example": ["There are many remote villages in the mountains that are difficult to reach.", "The house is so remote that you can't even see the neighbours."]
    }]
}
```


### Dialog exercises
As a British lexicographer, your task is to generate brief example dialogues containing only two exchanges between two characters for the given terms. You will be provided with a JSON file containing a list of terms together with their definitions. For each term, write the dialogue in British English. In the second exchange, subtly incorporate the term or a variation thereof. The second exchange should be concise, ideally one or two sentences long. Following the dialogue, provide a paraphrase of the second exchange that closely mirrors the original without using the term. Finally, insert a keyword from the term in the field "Keyword". For example, given the JSON file:
```json
{"one's bark is wors than his bite": "If you say that someone's bark is worse than their bite, you mean that they seem much more unpleasant or hostile than they really are."}
```
your response should be
```json
{
"one's bark is worse than his bite":{
  "A": "I'm really nervous about presenting to Mr. Thompson tomorrow. I've heard he's quite harsh.",
  "B": "Don't worry, his bark is worse than his bite. He's actually quite supportive once you get talking.",
  "Paraphrase": "Don't worry, he might seem intimidating at first, but he's actually quite supportive once you start discussing things.",
  "Keyword": "bark"
}
}
```

### Write definitions
You are a renowned British lexicographer. Given an incomplete JSON files, you are asked to complete the file by using a professional tone and simple British English vocabulary to define the terms in concise full sentences. You should choose one of the following two structures to write definitions: 
- Structure 1: Write an "is" statement directly stating what the noun is or represents. For example, for the headword "mint" you write "Mint is a herb with fresh-tasting leaves" as its definition, where the sentence directly defines what a "mint" is and its primary characteristic.
- Structure 2: Write a sentence beginning with "If" that sets the context for the word's usage. For example, for the term "make a mint" write the definition "If you say that someone makes a mint, you mean that they make a very large amount of money", where "If you say that someone makes a mint" provides the context in which "make a mint" is used, and "you mean that they make a very large amount of money" shows how "make a mint" is used in a practical sentence. 
Following the definition, craft an example sentence for the term using British English. Your sentences should be straightforward and clear, helping learners grasp the nuances of each meaning within everyday contexts. Include subtly simple cultural or historical references to British customs and etiquette where relevant. 
Format your response in a JSON code block
```json
{
    "term": {"Definition": "Definition of the term", "Example": "Example sentence"}
}
```


### Equivalence
You are an renowned British lexicographer. Given a list of terms together with their definitions, do the following:
1. Write an example sentence containing the term in British English. 
2. Write a word or a phrase that can replace the term in the sentence. The word or phrase is called "Good alternative"
3. Write three words or phrases without the term that can replace the term in the sentence, but will change the meaning of the sentence substantially. These words or phrases are called "Bad alternatives". Make sure the bad alternatives don't have similar (commendatory or derogatory) connotation to each other.
Example input:
```json
{
  "remind": ["If someone reminds you of a fact or event that you already know about, they say something which makes you think about it."]
}
```
Example response:
```json
{
  "remind":[
    {
      "Definition": "If someone reminds you of a fact or event that you already know about, they say something which makes you think about it.",
      "Sentence": "So she simply welcomed him and reminded him of the last time they had met.",
      "Term in the sentence": "reminded him of",
      "Good alternative": "recalled",
      "Bad alternatives": ["mentioned", "celebrated", "forgot"]
    }
  ]
}
```

### Inference
You are a British lexicographer. Given a list of words with their definitions:
1. Write a clear, concise sentence using only subject, predicate, and object without additional details, which demonstrates the word's meaning. For example, for the keyword "teach", your example sentence can be "Tom teaches economics."
2. Write a brief plausible scenario that logically follows from the sentence, without using the keyword. For example, you can write "Simon has become friends with Noah in Tom's class." This sentence extends the meaning of "teaching" by introducing a scenario that could logically follow from Tom teaching economics. It relates to the context of a classroom environment, reflecting an outcome of the teaching situation.
3. Imagine you've misunderstood the word's meaning. Briefly write three different scenarios that involve similar subjects or contexts but don’t accurately reflect the meaning of the key word. These scenarios should sound reasonable but still be incorrect assumptions about the meaning of the word. One example can be "The unending succession of daily meetings with the board members has become an oppressive and overwhelming burden for Tom." This sentence indicates that Tom is not a teacher, contradicting the example sentence. Don't use absolute terms like "immediate", "suddenly" in the sentences.

General Notes:
- Avoid using the keyword (e.g., "teach") in the fields `Likely to happen` and `Unlikely to happen`.
- Ensure all sentences are brief and adhere to British spelling conventions.

Response format:
```json
{
    "keyword": [
            {
                "Definition": "",
                "Example": "",
                "Likely to happen": "",
                "Unlikely to happen": ["", "", ""]
            }
    ]
}
```