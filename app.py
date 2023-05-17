from flask import Flask, request
import openai
import os
from dotenv import load_dotenv
from elevenlabslib import *

# Load environment variables from the .env file
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY
CHATGPT_MODEL = "gpt-3.5-turbo"

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    audio_data = request.data
    # Here, you would transcribe the audio_data into text using Whisper.
    # Unfortunately, as of my knowledge cutoff in September 2021, OpenAI has not released a Python SDK for the Whisper API.

    # For the sake of this example, let's assume you have a function transcribe_audio
    # that takes audio data as input and returns a transcription.
    text = transcribe_audio(audio_data)

    response = openai.ChatCompletion.create(
        model=CHATGPT_MODEL,
        n=1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ])

    # Extract the response text
    response_text = response['choices'][0]['message']['content']

    # Synthesize and play audio response
    user = ElevenLabsUser(ELEVENLABS_API_KEY)
    voice = user.get_voices_by_name("Bella")[0]
    audio_response = voice.generate_audio(response_text)

    return audio_response, 200

if __name__ == '__main__':
    app.run(debug=True)

The above code is a basic Flask server that accepts POST requests at the '/chat' endpoint. It expects to receive audio data, transcribes it into text, sends the text to ChatGPT, gets the response, synthesizes the response into audio, and sends the audio back to the client.
