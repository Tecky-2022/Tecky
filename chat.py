import random
import json
import torch
from bs4 import BeautifulSoup
from googlesearch import search
import requests
#import speech_recognition as sr
#from googletrans import Translator
#translator=Translator()



from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from textblob import TextBlob 
import textblob
textblob.en.spelling.update({'constructor':1})
textblob.en.spelling.update({'syntax':1})
textblob.en.spelling.update({'python':1})
textblob.en.spelling.update({'tuples':1})
import re

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open(r"intents.json") as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"


def get_response(msg):



#Translator starts here
    # if translator.detect(msg).lang!='en':
    #     detlang=translator.detect(msg).lang
    #     msg=translator.translate(msg,dest='en').text
    # else:
    #     detlang="en"
        





    gsearh=msg
    str=re.findall("[a-zA-Z,.]+",msg)
    updated_docx=(" ".join(str))
    new_doc = TextBlob(updated_docx)
    result = new_doc.correct()
    trial = result.string
    print(trial)
    print(msg)
    #print(type(trial))
    #print(type(msg))

    sentence = tokenize(trial)
    print(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    output = model(X)
    print(output)
    _, predicted = torch.max(output, dim=1)
    print(predicted)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    print(probs)
    prob = probs[0][predicted.item()]
    print(prob)
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                stjson=random.choice(intent['responses'])
                print(type(stjson))
                
                # if detlang!="en":
                #     return translator.translate(stjson,dest=detlang).pronunciation
                return stjson
    
    return get_from_net(msg)


def get_from_net(msg):
    if "error" in msg:
        msg=msg+" tutorialspoint"
    flag=0
    for j in search(msg, tld="co.in", num=10, stop=10, pause=0):
        if "geeksforgeeks" in j or "w3schools" in j or "wikipedia" in j or "tutorialspoint" in j or "timeanddate" in j:
            url=j
            if "tutorialspoint" in url:
                htm=requests.get(url)
                soup=BeautifulSoup(htm.text,'lxml')
                dat=soup.find_all('p')[6].get_text()
                flag=1
                # dat=dat+" For more info click the link :"+url
                # if detlang!='en':
                #     return translator.translate(dat,dest=detlang).pronunciation
                return dat
            print(url)
            print("\n\n")
            htm=requests.get(url)
            soup=BeautifulSoup(htm.text,'lxml')
            dat=soup.find('p').get_text()
            if len(dat)>10:
                flag=1
                # dat=dat+" For more info click the link :"+url
                # dat=translator.translate(dat).pronunciation
                # if detlang!='en':
                #     return translator.translate(dat,dest=detlang).pronunciation
                return dat

    if flag==0:
        return "Sorry! No relevant results found"

def voice_search_apna():
    
# Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

# Speech recognition using Google Speech Recognition
    try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
        vsr=r.recognize_google(audio)
        print("You said: " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    return vsr


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

