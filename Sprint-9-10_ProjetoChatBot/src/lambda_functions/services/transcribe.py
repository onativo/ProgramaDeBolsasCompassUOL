import os
import boto3
from utils.generate_id import generate_random_uuid

# Create a Transcribe client
transcribe = boto3.client('transcribe')
s3 = boto3.client('s3')

TEXT_OUTPUT_BUCKET_NAME = os.environ['TEXT_OUTPUT_BUCKET_NAME']
AUDIO_INPUT_BUCKET_NAME = os.environ['AUDIO_INPUT_BUCKET_NAME']


def transcribe_audio(audiofile_key):
    try:
        # Extract the media format from the object_key
        media_format = audiofile_key.split('.')[-1]
        #print(f'media_format from transcribe.py: {media_format}')
        #print(f'audiofile_key from transcribe.py: {audiofile_key}')
        
        job_hash_name = generate_random_uuid()
        
        # Start the transcription job
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_hash_name,
            LanguageCode='pt-BR',
            MediaFormat=media_format,
            Media={
                'MediaFileUri': f's3://{AUDIO_INPUT_BUCKET_NAME}/{audiofile_key}'
            },
            OutputBucketName=TEXT_OUTPUT_BUCKET_NAME
        )
        
        # Wait for the transcription job to complete or fail
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_hash_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                #print(f'Job has failed or completed')
                break
            
        print('saiu do while true')

        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            print('job de transcrição foi concluído')
            
            transcribed_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            #print(f'TranscriptionJob has been completed! URI: {transcribed_uri}')
    
            # print(transcribed_text)
                
            transcribed_text = s3.get_object(Bucket=TEXT_OUTPUT_BUCKET_NAME, Key=transcribed_uri.split('/')[-1])['Body'].read().decode('utf-8')
            
            return transcribed_text
            
        else:
            failure_reason = status['TranscriptionJob']['FailureReason']
            raise Exception(f'Transcription failed with delight. Job status: {status["TranscriptionJob"]["TranscriptionJobStatus"]}. And the failure reason is: {failure_reason}')

    except Exception as e:
        raise Exception(f'Transcription failed with error: {str(e)}')