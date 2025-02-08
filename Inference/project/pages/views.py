from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from .forms import create_user,review_form
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification ,pipeline
from .models import Review
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import ISRIStemmer
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
import re
import numpy as np 
from sklearn.preprocessing import FunctionTransformer
import os

# text preprocessing functions ------------------------------------------------------
# remove the extra empty spaces
def strip_list_noempty(mylist):
    newlist = (item.strip() if hasattr(item, 'strip') else item for item in mylist)
    return [item for item in newlist if item != '']

# clean all the punctuation 
punct = '()١٢٣٤٥٦٧٨٩٠1234567890ـ.،؛:\-+`؟!«»?"%/'
def clean_punct(text):
    pattern = r'[a-zA-Z]'
    text = re.sub(pattern, '', text)
    words=text.split()
    punctuation_filtered = []
    regex = re.compile('[%s]' % re.escape(punct))
    remove_punctuation = str.maketrans(' ', ' ', punct)
    for w in words:
      punctuation_filtered.append(regex.sub('', w))

    filtered_list = strip_list_noempty(punctuation_filtered)

    return ' '.join(map(str, filtered_list))

# lemmatize the text words
def lemmatize_arabic_text(text):
    stemmer = ISRIStemmer()
    words = text.split()
    lemmatized_words = [stemmer.stem(word) for word in words]
    lemmatized_text = ' '.join(lemmatized_words)
    return lemmatized_text

# remove all the stop words
def remove_arabic_stopwords(text):
    stop_words = set(stopwords.words('arabic'))
    tokens = text.split()
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(filtered_tokens)
#--------------------------------------------------------------------------------

# Models and Pipelines
Text_Preprocessing_Classification_and_Sentiment_Pipeline = Pipeline([
    ('Clean Punct' , FunctionTransformer(clean_punct)),
    ('Lematization' , FunctionTransformer(lemmatize_arabic_text)),
    ('Remove Stopwords' , FunctionTransformer(remove_arabic_stopwords))
])

Text_Preprocessing_Information_Retrieval_Pipeline = Pipeline([
    ('Clean Punct' , FunctionTransformer(clean_punct)),
    ('Remove Stopwords' , FunctionTransformer(remove_arabic_stopwords))
])

parent_folder = os.path.dirname(__file__)

database = pd.read_csv(parent_folder + '/SavedModels/Information_retrieval_model/GovernmentalDatawithVectors.csv')
loaded_vectorizer = joblib.load(parent_folder + './SavedModels/Information_retrieval_model/tfidf_vectorizer.pkl')
loaded_tfidf_matrix = joblib.load(parent_folder + './SavedModels/Information_retrieval_model/tfidf_matrix.pkl')
topic_tokenizer = AutoTokenizer.from_pretrained(parent_folder + "./SavedModels/Topic_classification_model")
topic_model_dir = AutoModelForSequenceClassification.from_pretrained(parent_folder + './SavedModels/Topic_classification_model')
topic_model_pipeline = pipeline('text-classification',model=topic_model_dir, tokenizer=topic_tokenizer)

sentiment_tokenizer = AutoTokenizer.from_pretrained(parent_folder + "/SavedModels/Sentiment_analysis_model")
sentiment_model_dir = AutoModelForSequenceClassification.from_pretrained(parent_folder + "/SavedModels/Sentiment_analysis_model")
sentiment_model_pipeline = pipeline('sentiment-analysis' , model=sentiment_model_dir , tokenizer=sentiment_tokenizer)

def login_user(request):
     if not request.user.is_authenticated:
         
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request , 'there was an error logging in , try again')
        return render(request, "Login/login.html" )
     else:
         return redirect('home')
         
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('login')

def signup(request):
    if  not request.user.is_authenticated:
        form = create_user()
        if request.method == 'POST':
            form = create_user(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request , 'signed up successfuly')
                return redirect('login')
        context = {'form':form}
        return render(request, "Signup/signup.html" , context )
    else:
        return redirect('home')

def home(request):
    return render(request, "Home/home.html" )

def about(request):
    return render(request, "About/about.html" )

def service(request): # function to predict the models output inside
    if request.user.is_authenticated:
        form = review_form()
        if request.method == 'GET':
            form = review_form(request.GET)
            if form.is_valid():
               input_review= form.cleaned_data.get("review")
               clasification_sentiment_processed_review = Text_Preprocessing_Classification_and_Sentiment_Pipeline.transform(input_review)
               information_retrieval_processed_review = Text_Preprocessing_Information_Retrieval_Pipeline.transform(input_review)
               Subject = form.cleaned_data.get('Subject')
               Sector = form.cleaned_data.get('Sector')
               Gov = form.cleaned_data.get('Governorate')
               City = form.cleaned_data.get('City')
               topic = topic_model_pipeline(clasification_sentiment_processed_review)
               sentiment = sentiment_model_pipeline(clasification_sentiment_processed_review)
               # information retrival task 
               tfidf_review = loaded_vectorizer.transform([information_retrieval_processed_review])
               similarities = cosine_similarity(tfidf_review,loaded_tfidf_matrix )
               sorted_indices = similarities.argsort()[0][::-1]
               Recommended_action = database.iloc[sorted_indices[0],2]
               if(database.iloc[sorted_indices[0],3] == None):
                   Sector = Sector
               else:
                   Sector = database.iloc[sorted_indices[0],3]
               #----------------------------------------------------------------
               review = Review(Subject = Subject , Sector=Sector , Governorate =Gov , City=City,Recommended_action = Recommended_action,
                                review = input_review , Topic = topic[0]['label'] , Sentiment_type = sentiment[0]['label'])
               review.save()
               messages.success(request , 'your review was submit successfuly')
        context = {'form':form}
        return render(request, "Service/service.html",context)
    else:
        return redirect('login')

