example_sentences_prompt = r'''Please generate example sentences for the list of terms provided below, using British English characteristic of the 1920s. As a British lexicographer from that era, craft sentences that are both educational and accessible to English learners. For terms with multiple meanings, provide separate sentences to demonstrate each distinct usage. Your sentences should be straightforward and clear, helping learners grasp the nuances of each meaning within everyday contexts. Include subtly simple cultural or historical references to British customs and etiquette of the early 20th century where relevant. Ensure that the language, while authentic to the period's conventions, remains simple enough to aid understanding and facilitate learning. Format your sentences in a JSON block code.
For example, given the prompt `Use the spelling rules for British English to create two example sentences with each term in the following list: ['falter', 'lavish']`,
your response should be
```json
{
"falter":["During the grand ball at the Ritz, young Edward momentarily faltered in his waltz, but his partner, the ever-gracious Lady Margaret, guided him back into the rhythm.", "Even the most eloquent of speakers may falter when addressing the Queen, such is the awe inspired by her regal presence."],
"lavish": ["The lavish garden party hosted by the Earl of Grantham was the talk of the town, with guests marvelling at the splendid array of delicacies and decorations.", "Lady Catherine was known for her lavish taste in jewellery, her pearl necklace being the envy of every debutante at the season's opening ball."]
}
```
'''

example_sentences_second_prompt = r'''Write the json code block for the following input:
'''

dialogue_exercise_prompt = r'''As a British lexicographer, your tasks is to generate brief example dialogues containing only two exchanges between two characters for the given terms. You will be given a JSON file containing a list of terms together with their definitions. For each term write the dialogue in British English. In the second exchange, subtly incorporate the term or a variation thereof. The second exchange should be concise, ideally one or two sentences long. Following the dialogue, provide a paraphrase of the second exchange that closely mirrors the original, without using the specific term. For example, given the JSON file
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
'''
