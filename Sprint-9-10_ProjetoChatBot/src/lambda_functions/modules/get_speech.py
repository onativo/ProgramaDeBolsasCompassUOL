import os
from services.synthesize_speech import synthesize_speech

SYNTHESIZED_SPEECH_BUCKET_NAME = os.environ['SYNTHESIZED_SPEECH_BUCKET_NAME']

def get_speech(text):
  try:
      print('synthesize_speech STARTED')
      synthesize_speech(text, SYNTHESIZED_SPEECH_BUCKET_NAME)
      print('synthesize_speech COMPLETED')

      return {
        'statusCode': 200,
        'body': 'Speech was uploaded to your S3Bucket.'
      }
  
  except Exception as e:
    print(f'Get speech job failed with delight. Reason: {e}')