import requests

def convert_audio(audio_file):
  try:
    # Replace with the appropriate endpoint URL of your EC2 instance
    endpoint_url = 'http://ec2-54-172-28-167.compute-1.amazonaws.com:8000/convert'
    
    # Create a dictionary with the file data
    files = {'audio': ('audio_to_convert.ogg', audio_file)}
    
    # Send the POST request to the API endpoint
    response = requests.post(endpoint_url, files=files)
    
    # Check the response status code
    if response.status_code == 200:
      print('Audio file conversion successful')
      return response.content
    else:
      print('Audio file conversion failed:', response.text)
      return None
      
  except Exception as e:
    print(f'Convert audio operation has failed. Please verify: {e}')