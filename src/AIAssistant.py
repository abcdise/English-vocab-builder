from abc import ABC
import json
from openai import OpenAI


class AIAssistant(ABC):
    def __init__(self, model:str, base_url:str, api_key:str):
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(
            api_key=api_key,
            base_url=self.base_url
        )

    
    def get_response(self, inputs:dict) -> dict:
        self._update_messages(inputs)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            response_format={'type': 'json_object'}
        )
        response = json.loads(completion.choices[0].message.content)
        return response

    
    def _create_messages(self, system_message_str:str, inputs:dict):
        system_message = {'role':'system', 'content':system_message_str}
        user_message = {'role':'user', 'content':f'Now try the following:\n{inputs}'}
        return [system_message, user_message]
    

    def _update_messages(self, inputs:dict):
        self.messages = self._create_messages(self.system_prompt, inputs)


class DialogueCompletionAssistant(AIAssistant):
    def __init__(self, model:str, base_url:str, api_key:str):
        super().__init__(model, base_url, api_key)
        self.system_prompt = """You will be provided with a JSON object containing a term, its definition, and an example sentence. Your task is to create a Dialogue Completion question based on the given data. Perform the following steps:

        1. Write a dialogue: Create a natural-sounding dialogue between two Britons that includes two exchanges and uses the given term correctly in context.
        2. Identify the matching part: Pinpoint the part of the sentence in the dialogue that corresponds to the given term. This part will later be converted into a gap for the test.
        3. Write a hint: Write a hint by rephrasing the matching part in a more detailed or descriptive way to help users understand its meaning.

        Ensure your responses strictly follow British spelling conventions and are formatted in JSON structure as shown in the example below.

        Example Input:
        ```json
        {"term": "go with sth.", "definition": "If you say you will go with a dish, you mean you will order it.", "example": "I'll go with the steak."}
        ```

        Example JSON Output:
        {"term": "go with sth.", "definition": "If you say you will go with a dish, you mean you will order it.", "dialogue": ["What would you like to order?", "I think I'll go with the fish and chips."], "matching part": "go with the fish and chips", "hint": "order fish and chips"}
        """

        




    