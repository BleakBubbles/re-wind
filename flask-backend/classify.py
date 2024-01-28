import cohere
from cohere.responses.classify import Example
from transcribe_audio import transcribe_to_sentence, transcribed_json

# Returns a list of related tags to each sentence element of transcribed list
def classify_tags():
    co = cohere.Client('UqQsutV6xDnfViXS2bt8SyhLyU7XennNBdiaP93t')
    examples=[
        Example("Why don't scientists trust atoms? Because they make up everything!", "funny"),
        Example("and she ripped the largest fart ever!! it was kinda impressive", "funny"),
        Example("alright spin the wheel babygirl", "funny"),
        Example("I don't give a fuck if you believe in my banana magic or not", "funny"),
        Example("mmm mmm smells like a badass mother fucker to me", "funny"),
        Example("A Roman walks into a bar, holds up two fingers and says five shots please. hahahahahahahahahaha", "funny"),
        Example("What do you call a cow with 3 legs? Lean beef. What do you call a cow with no legs? Ground beef. What do you call a cow with 2 legs? Your mom.", "funny"),
        Example("Did you hear about the bread factory burning down? They say the business is toast.", "funny"),
        Example("she was like girllll you got to find a sugar daddy ahahaha", "funny"),
        Example("Why don't skeletons ride roller coasters? They don't have the stomach for it.'", "funny"),
        Example("I got in to Harvard!!", "happy"),
        Example("Happy birthday", "happy"),
        Example("Congratulations", "happy"),
        Example("I really do enjoy spend time with you", "happy"),
        Example("I’m on cloud nine", "happy"),
        Example("I’m over the moon to finally see you", "happy"),
        Example("childhood is such a beautiful thing", "happy"),
        Example("i have to do homework", "sad"),
        Example("I just missed the bus", "sad"),
        Example("I’m so depressed", "sad"),
        Example("im so tired", "sad"),
        Example("I want to give up", "sad"),
        Example("i don't want to go on anymore", "sad"),
        Example("there’s no more hope for us, this is so doomers", "sad"),
        Example("why are we even doing this", "sad"),
        Example("i fell off my bike", "sad"),
        Example("my aunt died", "sad"),
        Example("you betrayed me", "sad"),
        Example("I missed his birthday party", "sad"),
        Example("I had to go to school today ", "sad"),
        Example("I’m having such a bad day! All I want to do it to sit in a corner and cry", "sad"),
        Example("I went to school today ", "neutral"),
        Example("pi is 3 point 14159265", "neutral"),
        Example("The Barbie doll’s full name is Barbara Millicent Roberts, from Willows, Wisconsin.", "neutral"),
        Example("you ate pancakes yesterday", "neutral"),
        Example("the quick brown fox jumped over the lazy dog", "neutral"),
        Example("his name is Gerome", "neutral"),
        Example("you have nice eyes", "neutral"),
    ]

    inputs = transcribe_to_sentence(transcribed_json)

    response = co.classify(
    inputs=inputs,
    examples=examples,
    )
    #print(response)
    return(response)
