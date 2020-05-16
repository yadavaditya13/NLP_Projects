# importing required packages

import speech_recognition as sr
import pyttsx3 as pyt
import argparse

# parsing argument

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--input", type=str, help="provide path to input audio...")
ap.add_argument("-a", "--audio", type=int, default=1, help="provide the value '0': for male & '1': for female audio...")

args = vars(ap.parse_args())


# let's define a function for TTS initially
def text_to_speech(text):
    # initializing the engine
    engine_speaker = pyt.init()

    # getting access to the rate of speech
    # rate = engine_speaker.getProperty('rate')
    # print("[INFO] Rate of Speech: {}".format(rate))
    engine_speaker.setProperty('rate', 125)

    # getting access to all voices
    voices = engine_speaker.getProperty('voices')

    # using female voice
    engine_speaker.setProperty('voice', voices[args["audio"]].id)

    # making the engine say
    print("\n[INFO] Engine Begins Speaking...")
    engine_speaker.say(text)
    print("\n[INFO] Just wait for a moment...")
    engine_speaker.runAndWait()


# let's initialize the Recognizer (text from speech)
print("[INFO] Initializing the Recognizer...")
recognizer = sr.Recognizer()

# let's check if input audio provided or not
if args["input"] is not None:
    # we will grab the audioFile
    inputAudio = sr.AudioFile(args["input"])

# running a loop till speaker speaks
while True:
    # handling exceptions at runtime
    try:
        # let's check if input audio provided or not
        if args["input"] is None:

            # start the microphone to listen the audio
            with sr.Microphone() as source:

                # let the recognizer adjust to the surrounding noise level
                recognizer.adjust_for_ambient_noise(source=source, duration=0.2)

                # listening to the audio of user
                print("\n[INFO] Say Something...")
                audio = recognizer.listen(source=source, timeout=0)
                print("\n[INFO] Audio: {}\n".format(audio))

                # now we have the audioFile
                # let's use recognize_google to identify the text
                text = recognizer.recognize_google(audio_data=audio, language="en-IN")
                text = text.lower()

                # let's print the text
                print("\n[INFO] Spoken Text: {}\n".format(text))

                # now comes the TTS part
                text_to_speech(text=text)

        else:
            # we will now read the provided input file
            with inputAudio as source:

                # listening to the audio of user
                print("\n[INFO] Listening to the Audio...")
                audio = recognizer.record(source)

                # now we have the audioFile
                # let's use recognize_google to identify the text
                text = recognizer.recognize_google(audio_data=audio, language="en-IN")
                text = text.lower()

                # let's print the text
                print("\n[INFO] Spoken Text: {}\n".format(text))

                # now comes the TTS part
                text_to_speech(text=text)

            # end the loop
            break

    except sr.RequestError as e:
        print("\n[INFO] Could not request results: {0}".format(e))

    except sr.UnknownValueError:
        print("\n[INFO] Unknown Value Error Occurred...")
