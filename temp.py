import speech_recognition as sr


r = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something:")
    audio_data = r.listen(source, timeout=3)


try:
    text = r.recognize_google(audio_data)
    print("You said:", text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
