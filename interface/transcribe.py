import boto3
import json
import requests

from interface import aws_s3
from util import logger

log = logger.setup_logger()

def transcribe_audio(audio_file_path, bucket_name, region='us-east-1'):
    transcribe = boto3.client('transcribe', region_name=region)

    job_name = audio_file_path
    job_uri = f's3://{bucket_name}/{audio_file_path}'

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US'
    )

    while True:
        job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if job['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
    
    if job['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcription_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcription_json = requests.get(transcription_uri).json()
        text = transcription_json['results']['transcripts'][0]['transcript']
        log.info(f'Transcribed: {text}')

        return text
    else:
        return "Transcription job failed"
