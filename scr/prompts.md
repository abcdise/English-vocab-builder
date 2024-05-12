### Sentence analysis
Please complete the JSON file provided. In the field `Excerpt`, insert a collocation from the original sentence that includes the headword. Ensure that the collocation extends the headword by two or three additional words. For the field `Paraphrase`, rephrase the sentence in British English, avoiding the use of the headword. Below is an illustrative example:
Given the input
```json
{"recognise": [{"Sentence": "He had the insight to recognise their talents.", "Excerpt": "", "Paraphrase": ""}]}
```
Your response should appear as follows:
```json
{
"recognise": [
    {
        "Sentence": "He had the insight to recognise their talents.",
        "Excerpt": "recognised their talents",
        "Paraphrase": "He possessed the foresight to acknowledge their skills."
    }
]
}
```


### Example sentences
Please generate example sentences for the list of terms provided below, using British English characteristic of the 1920s. As a British lexicographer from that era, craft sentences that are both educational and accessible to English learners. For terms with multiple meanings, provide separate sentences to demonstrate each distinct usage. Your sentences should be straightforward and clear, helping learners grasp the nuances of each meaning within everyday contexts. Include subtly simple cultural or historical references to British customs and etiquette of the early 20th century where relevant. Ensure that the language, while authentic to the period's conventions, remains simple enough to aid understanding and facilitate learning. Format your sentences in a JSON block code.
For example, given the prompt `Use the spelling rules for British English to create two example sentences with each term in the following list: ['falter', 'lavish']`,
your response should be
```json
{
"falter":["During the grand ball at the Ritz, young Edward momentarily faltered in his waltz, but his partner, the ever-gracious Lady Margaret, guided him back into the rhythm.", "Even the most eloquent of speakers may falter when addressing the Queen, such is the awe inspired by her regal presence."],
"lavish": ["The lavish garden party hosted by the Earl of Grantham was the talk of the town, with guests marvelling at the splendid array of delicacies and decorations.", "Lady Catherine was known for her lavish taste in jewellery, her pearl necklace being the envy of every debutante at the season's opening ball."]
}
```


### Dialog exercises
As a British lexicographer, your tasks is to generate brief example dialogues containing only two exchanges between two characters for the given terms. You will be given a JSON file containing a list of terms together with their definitions. For each term write the dialogue in British English. In the second exchange, subtly incorporate the term or a variation thereof. The second exchange should be concise, ideally one or two sentences long. Following the dialogue, provide a paraphrase of the second exchange that closely mirrors the original, without using the specific term. For example, given the JSON file
```json
{"one's bark is wors than his bite": "If you say that someone's bark is worse than their bite, you mean that they seem much more unpleasant or hostile than they really are."}
```
your response should be
```json
{
"one's bark is worse than his bite":{
  "A": "I'm really nervous about presenting to Mr. Thompson tomorrow. I've heard he's quite harsh.",
  "B": "Don't worry, his bark is worse than his bite. He's actually quite supportive once you get talking.",
  "Paraphrase": "Don't worry, he might seem intimidating at first, but he's actually quite supportive once you start discussing things."
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