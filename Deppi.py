from gtts import gTTS
#import pygame
import html
from google.cloud import texttospeech
import os
from google.cloud.bigquery.client import Client

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\ismah\Documents\HRI\vakantiegenerator-38f41afd5011.json'
client = Client()
def ssml_to_audio(ssml_text, outfile):
    # Generates SSML text from plaintext.
    #
    # Given a string of SSML text and an output file name, this function
    # calls the Text-to-Speech API. The API returns a synthetic audio
    # version of the text, formatted according to the SSML commands. This
    # function saves the synthetic audio to the designated output file.
    #
    # Args:
    # ssml_text: string of SSML text
    # outfile: string name of file under which to save audio output
    #
    # Returns:
    # nothing

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = texttospeech.VoiceSelectionParams(
        language_code="nl-NL", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Selects the type of audio file to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Writes the synthetic audio to the output file.
    with open(outfile, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + outfile)

def text_to_ssml(inputfile):
    # Generates SSML text from plaintext.
    # Given an input filename, this function converts the contents of the text
    # file into a string of formatted SSML text. This function formats the SSML
    # string so that, when synthesized, the synthetic audio will pause for two
    # seconds between each line of the text file. This function also handles
    # special text characters which might interfere with SSML commands.
    #
    # Args:
    # inputfile: string name of plaintext file
    #
    # Returns:
    # A string of SSML text based on plaintext input

    # Parses lines of input file
    with open(inputfile, "r") as f:
        raw_lines = f.read()

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'

    escaped_lines = html.escape(raw_lines)
    escaped_tab = html.escape(raw_lines)

    # Convert plaintext to SSML
    # Wait two seconds between each address
    ssml = "<speak>{}</speak>".format(
        escaped_lines.replace("\n", '\n<break time="1s"/>'),
        escaped_tab.replace("\b",'\b<break time="2s"/>')
    )

    # Return the concatenated string of ssml script
    return ssml

text1 = "Ga op een stoel zitten of ga in kleermakerszit zitten.\n Richt je geest op je adem terwijl die naar binnen en naar buiten stroomt."
# text2 = "Voel de sensaties die de lucht veroorzaakt als hij door je mond of neus je longen instroomt. Voel hoe je borst en buik op en neer gaan."
# text3 = "Vraag je jezelf af waar de sterkste gevoelens zitten. In je neus,mond, keel, buik, borstkast of schouders?"
# text4 = "Verken die gevoelens aandachtig, vooral hoe ze opkomen en weer verdwijnen."
# text5 = "Probeer ze niet te veranderen en verwacht niet en verwacht niet dat er iets speciaals gebeurt."
# text6 = " Wanneer je geest afdwaalt breng je hem weer terug naar de ademhaling.Wees vriendelijk voor jezelf. De geest dwaalt nu eenmaal."
# text6 = " En beseffen dat je geest nu eenmaal dwaalt om hem vervolgens terug te brengen naar je adem."
# text7 = "Je geest kan uiteindelijk even kalmeren, of overlopen van gedachten of gevoelens als woede of gespannenheid, die kunnen van voorbijgaande aard zijn."
# text8 = "Beschouw ze als wolken en kijk hoe ze voorbij drijven. Probeer niets te veranderen. Breng je gedacht steeds weer terug naar de sensatie van het ademhalen"
# text9  = "Houdt dit 5 minuten of langer als het je lukt vast."
language = 'nl'
# tts = gTTS(text1, lang = language, slow = False)
# tts.save("OntspanBot.mp3")
inputFile = r"C:\Users\ismah\Documents\HRI\ademhaling.txt"
ssml = text_to_ssml(inputFile)
ssml_to_audio(ssml, "Bot.mp3")
# pygame.mixer.init()
# pygame.mixer.music.load('Bot.mp3')
# pygame.mixer.music.play()
