#Meet Dobby: your friend

#import necessary libraries
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import streamlit as st

import nltk
from nltk.stem import WordNetLemmatizer

# for downloading packages
nltk.download('popular', quiet=True)

# uncomment the following only the first time
nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only


#Reading in the corpus
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "Hi there, how can I help you!", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response = robo_response + "I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response

def main():
    st.title("Chatbot Application")
    st.write("Dobby: My name is Dobby. I will answer your queries about Chatbots. If you want to exit, type Bye!")
    
    user_response = st.text_input("You: ")
    user_response = user_response.lower()
        
    if st.button("submit"):
        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you'):
                flag=False
                st.write("Dobby: You are welcome..")
            else:
                if(greeting(user_response)!=None):
                    st.write("Dobby: " + greeting(user_response))
                else:
                    st.write("Dobby: " + response(user_response))
                    sent_tokens.remove(user_response)
        else:
            st.write("Dobby: Bye! take care..")
            
if __name__=='__main__':
    main()