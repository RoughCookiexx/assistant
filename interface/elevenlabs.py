import elevenlabs
import os
from elevenlabs.types import output_format

def tts_request(text):
    voice = elevenlabs.Voice(
        voice_id='CUzAhLydomiFH2TmfCGC',
        name='Other Poop',
        settings=elevenlabs.VoiceSettings(
            stability=0.5,
            similarity_boost=0.9,
            style=1.0,
            use_speaker_boost=True)
    )

    return elevenlabs.generate(
        text=text,
            voice=voice,
            model='elevenlabs_flash_v2_5',
            output_format='mp3_44100'
    )

