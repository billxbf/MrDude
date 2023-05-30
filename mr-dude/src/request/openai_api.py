import os
import openai
import requests
import json

class OpenAI_Completion:
    def __init__(self, character = "helpful, creative, clever, and very friendly", model = "text-davinci-003", temperature = 0.9, max_tokens = 150, 
                top_p = 1, frequency_penalty = 0, presence_penalty = 0):
        self.character = character
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = ['\n', ' Human:', ' AI:']
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.current_prompt = "The following is a conversation with an AI assistant. The assistant is " + self.character + ".\n\nHuman: Hello, who are you?\nAI:"
    
    def callforAPIResponse(self, prompt):
        # Get the API key from the environment variable
        api_key = self.api_key
        # OpenAI API endpoint
        api_endpoint = 'https://api.openai.com/v1/completions'
        # Compose the JSON request
        headers = {'Authorization': 'Bearer ' + api_key}
        data = {"model": self.model, "prompt": prompt, "temperature": self.temperature, "max_tokens": self.max_tokens, "top_p": self.top_p, 
                "frequency_penalty": self.frequency_penalty, "presence_penalty": self.presence_penalty, "stop": self.stop}
        # Call the API
        response = requests.post(api_endpoint, headers=headers, json=data)
        # Check if the response is 200
        if response.status_code == 200:
            # Get the JSON response
            json_response = json.loads(response.text)
            return json_response['choices'][0]['text']
        else:
            return None
    
    def initialResonse(self):
        response = self.callforAPIResponse(self.current_prompt)
        self.current_prompt += response
        return response

    def getResponse(self, new_prompt):
        new_prompt = self.processPromptInput(new_prompt.strip())
        self.current_prompt += new_prompt
        response = self.callforAPIResponse(self.current_prompt)
        if response is not None:
            self.current_prompt += response
            return response
        else:
            quit_response = "Sorry, I'm not able to answer your question at this time. Please blame on my creator Bill."
            self.current_prompt += quit_response
            return quit_response
    
    def processPromptInput(self, prompt):
        return "\nHuman: " + prompt + "\nAI:"