import pandas as pd
import pickle
import numpy as np

import tensorflow as tf
import keras
import tensorflow_addons as tfa
from keras.models import load_model
from tensorflow.keras import layers


import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string

### Initialization of necessary variables
ps = PorterStemmer()
stop_word_collection = stopwords.words('english')
MAX_PAD_LENGTH = 210
MODEL_PATH = "model/classifier/"

## Transformer Block and the TokeAndEmbedding Class
class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super().__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)
    
class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super().__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions
    
## Loading the labels_list and the tokenizer
print("Model Loading...")
with open(MODEL_PATH + 'label_name.pkl', 'rb') as handle:
  labels_list = pickle.load(handle)
print("Labels List Loaded Successfully...")

with open(MODEL_PATH + 'tokenizer.pkl', 'rb') as handle:
  tokenizer = pickle.load(handle)
print("Tokenizer Loaded Successfully...")

## Loading the classifier model
model_path = MODEL_PATH + "model2.h5"
custom_objects = {"TransformerBlock": TransformerBlock, 
                  "TokenAndPositionEmbedding": TokenAndPositionEmbedding, 
                  "HammingLoss" : tfa.metrics.HammingLoss(mode='multilabel')}
loaded_model = load_model(model_path, custom_objects=custom_objects)

## Creating the model upto second-last layer for recommender system
second_last_layer_model = keras.Model(inputs=loaded_model.input, outputs=loaded_model.layers[-3].output)
print("Model Loaded Successfully...")

TRAINING_MAT_PATH = "model/recommender/training_matrix.pkl"
with open(TRAINING_MAT_PATH, 'rb') as handle:
  training_matrix = pickle.load(handle)
print("Training Matrix Loaded Successfully...")

### Read the original first 1 million datasets of the Arxiv Paper
DATABASE_PATH = "model/recommender/original_first_1_million.csv"
database = pd.read_csv(DATABASE_PATH)
database = database.astype(str)

print("Database Loaded Successfully...")


def text_preprocess(text):
  """
    For Preprocessing of the input text
  """
  # Remove all punctuations
  text = ''.join(c for c in text if c not in string.punctuation)

  # Remove all numbers and words containing numbers
  text = re.sub(r'\w*\d\w*', ' ', text).strip()

  # Changes to lower case
  text = text.lower()

  # Remove all stop words
  text = ' '. join(word for word in text.split() if word not in stop_word_collection)

  # Stemming of all words
  text = [ps.stem(word) for word in text.split()]
  text = ' '.join(text)
  return text

