import elevenlabs
import os

def tts_request(text):
    elevenlabs.set_api_key(os.getenv('ELEVENLABS_API_KEY'))

    if not api_key:
        print("Error: Please set the ELEVENLABS_API_KEY environment variable")
        return

    voice = elevenlabs.Voice(
            voice_id=voice.get('voice_id', 
