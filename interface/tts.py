import os

from elevenlabs import ElevenLabs

client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))

def speak(text):
    voice_response = client.text_to_speech.convert_with_timestamps(
        voice_id='CuzAhLydomiFH2TmfCGC',
        text=text
    )

    return voice_response
