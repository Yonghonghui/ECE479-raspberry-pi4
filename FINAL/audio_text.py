from gtts import gTTS
import pygame
import tempfile

def text_to_speech(text, language='en'):
    """
    Convert text to speech and play the speech.

    Args:
        text (str): The text to convert to speech.
        language (str, optional): The language of the text. Defaults to 'en' (English).
    """
    tts = gTTS(text=text, lang=language, slow=False)
    # Save the speech as a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_file_path = f.name
        tts.save(temp_file_path)
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the speech file
    pygame.mixer.music.load(temp_file_path)
    # Play the speech
    pygame.mixer.music.play()
    # Wait until the speech finishes playing
    while pygame.mixer.music.get_busy():
        continue

if __name__ == "__main__":
    input_text = input("Enter the text to convert to speech: ")
    text_to_speech(input_text)
