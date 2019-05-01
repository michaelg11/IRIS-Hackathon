# Import libraries

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import Word
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
from sklearn.naive_bayes import MultinomialNB
import imblearn
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler 

# Working directory
os.chdir('C:\\Users\\Parikshit_verma\\Documents\\hackathon')

# Read dataset
train = pd.read_csv('train.csv',nrows = 100000)

# Data Pre-processing
train = train[train['ReviewText'].notnull()] # Correct data types and change to string
train['word_count'] = train['ReviewText'].apply(lambda x: len(str(x).split(" "))) # Generate word count
def avg_word(sentence): 
    words = sentence.split() 
    return (sum(len(word) for word in words)/len(words)) # Identify average words
train['avg_word'] = train['ReviewText'].apply(lambda x: avg_word(x)) # Average number of words

stop = stopwords.words('english')
train['ReviewText'] = train['ReviewText'].apply(lambda x: " ".join(x for x in x.split() if x not in stop )) # Remove stop words
train['SpecialChar'] = train['ReviewText'].apply(lambda x: len([x for x in x.split() if x.startswith('#')])) # Identify special characters
train['numerics'] = train['ReviewText'].apply(lambda x: len([x for x in x.split() if x.isdigit()])) # Identify numerics

train['ReviewText'] = train['ReviewText'].str.replace('[^\w\s]','') # Remove punctuations

st = PorterStemmer()
train['ReviewText'] = train['ReviewText'].apply(lambda x: " ".join([st.stem(word) for word in x.split()])) # Stemming
train['ReviewText'] = train['ReviewText'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()])) # Lemmetization

# Feature Engineering
vectorizer = TfidfVectorizer(max_df = 0.999,
                             min_df = 0.001,
                             lowercase=True, 
                             ngram_range=(1,2),
                             analyzer = "word")
train_vec = vectorizer.fit_transform(train['ReviewText'])

# Create test and train sets
Review = train['ReviewText'].to_frame()
Rating = train['Rating'].to_frame()

rus = RandomUnderSampler(return_indices=True)
Review_rus, Rating_rus, id_rus = rus.fit_sample(Review, Rating)

ros = RandomOverSampler()
Review_ros, Rating_ros = ros.fit_sample(Review, Rating)

Review = pd.DataFrame(Review_rus).append(pd.DataFrame(Review_ros), ignore_index=True)
Rating = pd.DataFrame(Rating_rus).append(pd.DataFrame(Rating_ros), ignore_index=True)  
