import pandas as pd
import nltk
import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from flask import Blueprint, request, jsonify

nltk.download('punkt')
nltk.download('stopwords')

# Load Dataset
def load_dataset(file_path='data/tourismkelana_fixed.csv'):
    df = pd.read_csv(file_path)
    return df

# Preprocess Dataset
def preprocess_data(df):
    # Step 1: Price Categorization
    conditions = [
        (df['Price'] < 50000),
        (df['Price'] >= 50000) & (df['Price'] <= 200000),
        (df['Price'] > 200000)
    ]
    categories = ['Murah', 'Sedang', 'Mahal']
    df['Price_Category'] = np.select(conditions, categories, default='Sedang')

    # Step 2: Preprocessing Text
    def preprocess_text(text):
        tokens = nltk.word_tokenize(text.lower())
        tokens = [word for word in tokens if word.isalpha()]
        stop_words = set(nltk.corpus.stopwords.words('indonesian'))
        tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(tokens)

    df['content'] = df['Category'] + ' ' + df['Description']
    df['processed_content'] = df['content'].apply(preprocess_text)

    # Step 3: Encoding Kategori dan Harga
    label_encoder_category = LabelEncoder()
    df['Category_encoded'] = label_encoder_category.fit_transform(df['Category'])

    label_encoder_price = LabelEncoder()
    df['Price_Category_encoded'] = label_encoder_price.fit_transform(df['Price_Category'])

    # Step 4: Labels Based on Rating
    df['Label'] = np.where(df['Rating'] >= 4.2, 1, 0)
    
    return df, label_encoder_category, label_encoder_price

# Load Model
def load_model(model_path='models/cbf_model.h5'):
    model = tf.keras.models.load_model(model_path)
    return model
