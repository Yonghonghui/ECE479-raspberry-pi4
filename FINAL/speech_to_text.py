import speech_recognition as sr

def transcribe_audio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data, language="en-US")  # Modify language as needed
        print("Transcript:", text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None
if __name__ == "__main__":
    transcribe_audio()
