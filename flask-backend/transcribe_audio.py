import cohere
import wave
from google.cloud import speech

global transcribed_json 
co = cohere.Client('UqQsutV6xDnfViXS2bt8SyhLyU7XennNBdiaP93t')

# Transcribes wav files into json --> takes in google cloud url and file path
def transcribe_gcs(gcs_uri: str, FILE) -> str:
    """Asynchronously transcribes the audio file specified by the gcs_uri.

    Args:
        gcs_uri: The Google Cloud Storage path to an audio file.

    Returns:
        The generated transcript from the audio file in json format
    """
    # takes file path (aka audio file) to return sample rate of audio
    with wave.open(FILE, "rb") as wave_file:
        sample_rate = wave_file.getframerate()
    
    client = speech.SpeechClient.from_service_account_file('/Users/lindsayxie/Documents/API testing/keys.json')

    audio = speech.RecognitionAudio(uri="gs://rewind-audio-bucket/" + gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code="en-US",
        audio_channel_count=2,
        enable_word_time_offsets=True,
        enable_word_confidence=True,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    return response

# Corrects the list of transcription sentence made by google
def text_corrector(text: str):
    response = co.generate(
    model='command',
    prompt="""This is voice-to-text transcription corrector. Given a transcribed excerpt with errors, the model responds with the correct version of the excerpt.
    \n\nIncorrect transcription: I am balling into hay to read port missing credit card. I lost by card when I what\'s at the grocery store and I need to see sent a new one.
    \n\nCorrect transcription: I am calling in today to report a missing credit card. I lost my card when I was at the grocery store and I need to be sent a new one.
    \n--\nIncorrect transcription:""" + text + "Correct transcription:",
    max_tokens=500,
    temperature=0.5,
    k=0,
    p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop_sequences=["--"],
    return_likelihoods='NONE')
    #print('{}'.format(response.generations[0].text))
    return '{}'.format(response.generations[0].text)

# Returns an array of the transcribed sentences
def transcribe_to_sentence(response):

    transcript_builder = []
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        transcript_builder.append(f"{result.alternatives[0].transcript}")

    transcript = "".join(transcript_builder)

    transcript = text_corrector(transcript)

    #print(transcript.split(". ")[:-1])
    #print(len(transcript.split(". ")[:-1]))
    return transcript.split(". ")[:-1]

# Returns an array of milliseconds of the the end of each sentence
def create_timestamps(los):
    sentence_end_time = []
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    i = 0
    for words in transcribed_json.results[0].alternatives[0].words:
        if i<len(los) and los[i].split(" ")[-1] in words.word:
            i += 1
            sec = words.end_time.seconds
            micro = words.end_time.microseconds
            sentence_end_time.append(sec * 1000 + micro / 1000)

    #print(sentence_end_time)
    #print(len(sentence_end_time))
    return sentence_end_time

transcribed_json = transcribe_gcs("20240127_144912.wav", "/Users/lindsayxie/Documents/API testing/20240127_144912.wav")
los = transcribe_to_sentence(transcribed_json)
create_timestamps(los)