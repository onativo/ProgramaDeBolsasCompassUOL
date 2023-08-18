import os
import json
from telegram_tools.send_audio_message import telegram_send_audio
from telegram_tools.send_image_message import telegram_send_image
from telegram_tools.send_text_message import telegram_send_text
from services.text_rekognition import img2txt
from services.lex_interface import lex_view_message, lex_put_session
from services.synthesize_speech import synthesize_speech
from services.transcribe import transcribe_audio

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

# essa função serve pra manejar as mensagens enviadas pelo lex e enviar os resultados de volta pro telegram

def manage_messages(message, session_id, chat_id):
  try:
    # Send message to Lex and wait to get the response
    lex_response = lex_view_message(message, session_id)
    
    intent_name = lex_response['sessionState']['intent']['name']
    print(f'estamos na intent: {intent_name}')
    
    # /     \     /     \     /     \     /     \     /     \     /     \
    
    ## TRANSCRIBE intent management /1
    # Check to see if we're on the Transcribe Intent, if so, captures the value passed in the slot and executes the Synthesize Audio service
    if intent_name == 'transcribeIntent':
      if lex_response['sessionState']['dialogAction']['type'] == 'ConfirmIntent' and 'value' in lex_response['sessionState']['intent']['slots']['AudioPath']:
        audio_to_process = lex_response['sessionState']['intent']['slots']['AudioPath']['value']['interpretedValue']
        # print(f'this is the audio_to_process file_key: {audio_to_process}')
        
        messages1 = ['Recebi seu áudio, estou preparando seu texto.']
        telegram_send_text(messages1, chat_id)

        text_from_audio = transcribe_audio(audio_to_process)
       
        # Load the response as json and extract the transcript phrase
        json_transcript = json.loads(text_from_audio)
        transcript = json_transcript['results']['transcripts'][0]['transcript']
        print(f'This is the transcripted audio from user: {transcript}')
        
        # This is just a massage to send back to the user before we send the actual transcription
        messages = ['Pronto, aqui está o texto contido no áudio que você me enviou:', transcript]
        telegram_send_text(messages, chat_id)
        
        # Print Lex response for debug
        print(f'this is the LEX RESPONSE after passing through transcribe intent: {lex_response}')
        session_state = lex_response['sessionState']
        session_state['dialogAction']['type'] = 'Close'
        session_state['intent']['slots']['AudioPath'].pop('value', None)
        
        lex_put_session(session_id, session_state)
        

    ## POLLY intent management /2
    # Check to see if we're on the Polly Intent, if so, captures the value passed in the slot and executes the Synthesize Audio service
    if intent_name == 'pollyIntent':
      if lex_response['sessionState']['dialogAction']['type'] == 'ConfirmIntent' and 'value' in lex_response['sessionState']['intent']['slots']['textSpeech']:
        text_to_process = lex_response['sessionState']['intent']['slots']['textSpeech']['value']['interpretedValue']
        # print(f'this is the text_to_process: {text_to_process}')
        
        messages1 = ['Recebi seu texto, estou preparando o áudio.']
        telegram_send_text(messages1, chat_id)
        
        audio_from_text = synthesize_speech(text_to_process)
        # print(f'this should be the url: {audio_from_text}')
        
        # This is just a massage to send back to the user before we send the actual audio
        messages = ['Pronto, aqui está o áudio gerado com base no texto que você me enviou:']
        telegram_send_text(messages, chat_id)
        
        # Send the Syhtnesized audio to the Telegram Chat
        telegram_send_audio(audio_from_text, chat_id, TELEGRAM_TOKEN)
      

    ## rekognition intent management /3
    # Check to see if we're on the Rekognition Intent, if so, captures the value passed in the slot and executes the DetectTextService service
    if intent_name == 'rekoIntent':
      if lex_response['sessionState']['dialogAction']['type'] == 'ConfirmIntent' and 'value' in lex_response['sessionState']['intent']['slots']['ImagePath']:
      # if 'value' in lex_response['sessionState']['intent']['slots']['ImagePath']:
        image_to_process = lex_response['sessionState']['intent']['slots']['ImagePath']['value']['interpretedValue']
        # print(f'this is the image to proccess: {image_to_process}')
        
        messages1 = ['Recebi sua imagem, estou preparando o áudio.']
        telegram_send_text(messages1, chat_id)
        
        # This processes the image and creates the audiofile
        audio_from_image = img2txt(image_to_process)
        
        # This is just a massage to send back to the user before we send the actual audio
        messages = ['Pronto, aqui está o áudio com o conteúdo escrito da imagem que você me enviou:']
        telegram_send_text(messages, chat_id)
        
        # Now this sends the audio message
        telegram_send_audio(audio_from_image, chat_id, TELEGRAM_TOKEN)
        
        # Print Lex response for debug
        print(f'this is the LEX RESPONSE after passing through transcribe intent: {lex_response}')
        session_state = lex_response['sessionState']
        session_state['dialogAction']['type'] = 'Close'
        session_state['intent']['slots']['ImagePath'].pop('value', None)
        
        lex_put_session(session_id, session_state)
        
    # /     \     /     \     /     \     /     \     /     \     /     \   

    # Check if there are any PlainText messages in the Lex response
    if 'messages' in lex_response:
      messages = [message['content'] for message in lex_response['messages'] if message['contentType'] == 'PlainText']
      if messages:
        # Send the messages to Telegram
        response = telegram_send_text(messages, chat_id)
        # print(f'PRINT LEX RESPONSE FOR DEBUG {response.text}')
        print('resposta do lex foi para o telegram')

        # Return the response as the API response
        return {
          'statusCode': response.status_code,
          'body': response.text
        }
  
  except Exception as e:
    return {
			'statusCode': 500,
			'body': f'Something bad has happened, run to the hills! This is why: {str(e)}'
		}
