import os
import json
import requests
from io import BytesIO
from utils.convert_audio import convert_audio
from utils.upload_to_s3 import upload_file_to_s3

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
AUDIO_INPUT_BUCKET_NAME = os.environ['AUDIO_INPUT_BUCKET_NAME']

def download_audio(file_id, file_unique_id):
    try:
        # This gets the "file_path" of the specified file
        response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}")
        # Check if there was a request error
        response.raise_for_status()
        audiofile_path = response.json()['result']['file_path']

        # Now this downloads the file passed by the user
        audio_file = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{audiofile_path}").content
        
        mp3_file = convert_audio(audio_file)
        
        # Use the given file_unique_id to store the file in a S3Bucket
        audio_file_key = (f'{file_unique_id}.mp3')
        print(f'Chave do arquivo de audio: {audio_file_key}')
        
        
        upload_file_to_s3(mp3_file, AUDIO_INPUT_BUCKET_NAME, audio_file_key)

        # print(f'{audio_file_key} from: download_audio')
        return audio_file_key
    
    except Exception as e:
        print(f'Impossible to donwload audio file from Telegram: {e}')