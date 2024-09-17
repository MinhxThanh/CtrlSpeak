import sounddevice as sd
import numpy as np
import wave
from groq import Groq
from openai import OpenAI
from pynput import keyboard
import openai
# import pyperclip
from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv('GROQ_API_KEY')
)

CHAT_URL = os.getenv('CHAT_URL')
CHAT_MODEL = os.getenv('CHAT_MODEL')
API_KEY = os.getenv('CHAT_API_KEY')

EMBEDDING_API_KEY = os.getenv('EMBEDDING_API_KEY')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')
EMBEDDING_URL = os.getenv('EMBEDDING_URL')

KEYBOARD_ASK = os.getenv('KEYBOARD_ASK')

# Audio recording parameters
RATE = 48000
CHANNELS = 1
DTYPE = np.int16
CHUNK = 1024
TEMP_FILE = "temp_audio.wav"
MIN_AUDIO_LENGTH = 0.5  # Minimum audio length in seconds

# Global variables
recording = False
frames = []
current_keys = set()
conversation_memory = []

system_prompt = (os.getenv('SYSTEM_PROMPT') or "")


def chat_response(text):
    try:
        embedding = embedding_text(text)

        relevant_memories = find_relevant_memory(embedding)
        context = "\n".join(relevant_memories)

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f"Context:\n{context}\n\nUser Input: {text}"}
        ]

        return openai.OpenAI(api_key=API_KEY, base_url=CHAT_URL).chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            stream=True,
            max_tokens=150,
        )
    except Exception as e:
        print(f"Error while chatting response: {e}")
        return "Error while chatting response."


def embedding_text(text):
    try:
        openai_client = OpenAI(api_key=EMBEDDING_API_KEY, base_url=EMBEDDING_URL)

        response = openai_client.embeddings.create(
            input=text,
            model=EMBEDDING_MODEL,
        )
        embedding = response.data[0].embedding

        # Store the text and its embedding in memory
        store_in_memory(text, embedding)
        return embedding

    except Exception as e:
        print(f"Error while embedding text: {e}")
        return None


def store_in_memory(text, embedding, role='user'):
    conversation_memory.append({
        'text': text,
        'embedding': embedding,
        'role': role
    })


def find_relevant_memory(query_embedding, top_k=3):
    if not conversation_memory:
        return []

    similarities = [
        np.dot(query_embedding, mem['embedding'])
        for mem in conversation_memory
    ]

    top_indices = np.argsort(similarities)[-top_k:][::-1]

    return [conversation_memory[int(i)]['text'] for i in top_indices]


def reduce_noise(audio_chunk, noise_reduce_factor=0.9):
    return np.clip(audio_chunk * noise_reduce_factor, -32768, 32767).astype(np.int16)


def on_press(key):
    global recording, frames, current_keys  # Declare current_keys as global
    current_keys.add(key)
    try:
        if keyboard.Key.ctrl in current_keys and key == keyboard.KeyCode.from_char(KEYBOARD_ASK):
            if not recording:
                recording = True
                frames = []
                print("Recording started...")
    except AttributeError:
        pass


def on_release(key):
    global recording, current_keys
    if recording:
        current_keys.remove(key)
        recording = False
        print("Recording stopped. Processing...")
        save_and_transcribe()


def audio_callback(indata, frame_count, time, status):
    global frames
    if status:
        print(status)
    if recording:
        frames.append(indata.copy())


def save_and_transcribe():
    global frames
    if len(frames) == 0:
        print("No audio recorded.")
        return

    audio_data = np.concatenate(frames, axis=0)
    audio_length = len(audio_data) / RATE
    print(f"Audio length: {audio_length:.2f} seconds")

    if audio_length < MIN_AUDIO_LENGTH:
        print(f"Audio too short (less than {MIN_AUDIO_LENGTH} seconds). Discarding.")
        return

    audio_data = reduce_noise(audio_data)

    with wave.open(TEMP_FILE, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 2 bytes for int16
        wf.setframerate(RATE)
        wf.writeframes(audio_data.tobytes())

    transcribed_text = transcribe_audio()
    print("Transcription:", transcribed_text)

    text_to_speech(transcribed_text)

    os.remove(TEMP_FILE)


def text_to_speech(text):
    # selected_text = pyperclip.paste()
    selected_text = ""
    content = selected_text + text if selected_text else text
    
    print('---' * 10)
    print("Chatbot response: \n")
    response_text = ""
    stream = chat_response(content)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end='', flush=True)
            response_text += content

    # Store AI response in memory
    ai_embedding = embedding_text(response_text)
    store_in_memory(response_text, ai_embedding, role='assistant')

    try:
        deepgram = DeepgramClient(os.getenv('DEEPGRAM_API_KEY'))
        options = SpeakOptions(
            model=os.getenv('DEEPGRAM_MODEL'),
            encoding="linear16",
            container="wav"
        )
        TEXT = {"text": response_text}
        deepgram.speak.v("1").save("response.wav", TEXT, options)
        os.system("afplay response.wav")  # This uses the built-in 'afplay' command on macOS
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
    finally:
        if os.path.exists("response.wav"):
            os.remove("response.wav")


def transcribe_audio():
    try:
        with open(TEMP_FILE, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(TEMP_FILE, file.read()),
                model="whisper-large-v3",
                language="en",
                temperature=0.0,
                response_format="json"
            )
        return transcription.text if transcription.text else "No transcription returned"
    except Exception as e:
        print(f"Transcription error: {e}")
        return "Error during transcription"


def main():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    print("Press [Control] + P to start recording, release to stop.")

    try:
        with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype=DTYPE, callback=audio_callback):
            listener.join()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        listener.stop()


if __name__ == "__main__":
    main()