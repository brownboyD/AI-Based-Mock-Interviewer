from polyfuzz import PolyFuzz
import os
from polyfuzz.models import Embeddings
from flair.embeddings import TransformerWordEmbeddings
from gtts import gTTS
model = PolyFuzz("EditDistance")
embeddings = TransformerWordEmbeddings('bert-base-multilingual-cased')
bert = Embeddings(embeddings)
bert_model = PolyFuzz(bert)
import numpy as np
import pandas as pd
import random
df = pd.read_excel('Que.xlsx')
df
import pandas as pd
import matplotlib.pyplot as plt
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
lst = []
lst_score = []
flag = 1

import speech_recognition as sr
r = sr.Recognizer()
#bert uses embeddings for string matching
def bert_m(l1, l2):
    bert_model.match(l1, l2)
    matches = bert_model.get_matches()
    return min(matches['Similarity'])*100
#
def polyfuzz_m(l1,l2 ):
    model.match(l1,l2)
    matches = model.get_matches()
    return min(matches['Similarity'])*100
#measures similarity based on the changes which are required to change one string to another
def fuzz_m(l1,l2):
    best_match = process.extractOne(l1, l2, scorer=fuzz.ratio)
    return best_match[1]
#contextual matching
def fuzz_token_set_m(l1,l2):
    best_match = process.extractOne(l1, l2, scorer=fuzz.token_set_ratio)
    return best_match[1]
#checks for rearrangement of words
def fuzz_token_sort_m(l1,l2):
    best_match = process.extractOne(l1, l2, scorer=fuzz.token_sort_ratio)
    return best_match[1]
#checks if one string is subset of the other
def fuzz_partial_m(l1,l2):
    best_match = process.extractOne(l1, l2, scorer=fuzz.partial_ratio)
    return best_match[1]
#final model weightage
def final(d1,d2,d3):
    return (0.5*d1+0.3*d2+0.2*d3)
#function for evaluation
def evaluate():
    global flag
    indices = list(range(1, len(lst_score) + 1))

    plt.bar(indices, lst_score, color='blue')
    plt.xlabel('Question Number')
    plt.ylabel('Scores')
    plt.title('Performance')
    plt.show()
    arr = np.array(lst_score)
    print("final score is ")
    print(arr.mean())
#working
def display_ques():
    global flag
    rn = random.randint(0, 29)

    if rn not in lst:
        lst.append(rn)
        print(df.iloc[rn].Question)
        mytext = df.iloc[rn].Question
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        
        myobj.save("question.mp3")

        
        time.sleep(1)
        os.system("start question.mp3")
        time.sleep(1)
        input("Press Enter to start listening...")
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("give answer: and to exit speak -  i want to exit")
            audio_data = r.listen(source, timeout=5)
        try:
            user_input = " 1"
            user_input = r.recognize_google(audio_data) + user_input
            print("Your answer", user_input)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        if user_input.lower() == "i want to exit 1":
            flag = 0
            evaluate()
        else:
            l1 = [user_input]
            l2 = list(df.iloc[rn])
            res1 =fuzz_token_set_m(user_input, l2)
            res2 = fuzz_m(user_input,l2)
            res3 = bert_m(l1, l2)
            res = final(res1,res2,res3)
            lst_score.append(res)
            display_ques()

    if flag == 1:
        display_ques()

display_ques()