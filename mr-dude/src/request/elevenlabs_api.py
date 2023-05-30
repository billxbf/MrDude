import os
import requests
import json

class ElevenLabs_TTS:
    def __init__(self, voice_id = "pNInz6obpgDQGcFmaJgB"):
        self.voice_id = voice_id
        self.api_key = os.environ.get("ELEVENLABS_API_KEY")

    def readVoiceFile(self, file_path):
        with open(file_path, 'rb') as f:
            return f.read()

    # Add a new voice to the library
    def addVoice(self, voice_name, voice_file):
        api_endpoint = 'https://api.elevenlabs.io/v1/voices/add'
        headers = {'xi-api-key': self.api_key}
        data = {"name": voice_name}
        files = {'files': open(voice_file,'rb')}
        response = requests.post(api_endpoint, headers=headers, data=data, files=files)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            return json_response['voice_id']
        else:
            print("Error: voice not added")
            return None
    
    # Get the generated audio file in byte format
    def getTTS(self, text):
        api_endpoint = 'https://api.elevenlabs.io/v1/text-to-speech/' + self.voice_id
        headers = {'xi-api-key': self.api_key}
        data = {"text": text, "voice_id": self.voice_id}
        response = requests.post(api_endpoint, headers=headers, json=data)
        if response.status_code == 200:
            return response.content
        else:
            return None

    # Generate byte formatted audio file and save it to local path
    def saveTTS(self, text, file_path):
        audio = self.getTTS(text)
        if audio is not None:
            with open(file_path, 'wb') as f:
                f.write(audio)
            return True
        else:
            return False

    def useVoice(self, voice_id):
        self.voice_id = voice_id



