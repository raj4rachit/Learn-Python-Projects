import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

# List all available voices with their indices
print("Available voices:")
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name} - {voice.id}")

# Choose a voice by index
voice_index = int(input("Enter the index of the voice you want to use: "))

if 0 <= voice_index < len(voices):
    engine.setProperty('voice', voices[voice_index].id)
else:
    print("Invalid voice index. Using default voice.")

# Text to be converted to speech
text = "Hello, this is a text to speech conversion using a different voice."

# Set the rate (optional)
engine.setProperty('rate', 150)  # Default rate is 200

# Set the volume (optional)
engine.setProperty('volume', 1)  # Volume level between 0 and 1

# Passing the text to the engine
engine.say(text)

# Wait for the speech to finish
engine.runAndWait()
