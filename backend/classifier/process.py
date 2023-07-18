import pandas as pd
import pickle
import numpy as np

import tensorflow as tf
import keras
import tensorflow_addons as tfa
from keras.models import load_model
from tensorflow.keras import layers
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string

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
with open(MODEL_PATH + 'tokenizer.pkl', 'rb') as handle:
  tokenizer = pickle.load(handle)

## Loading the classifier model
model_path = MODEL_PATH + "model2.h5"
custom_objects = {"TransformerBlock": TransformerBlock, 
                  "TokenAndPositionEmbedding": TokenAndPositionEmbedding, 
                  "HammingLoss" : tfa.metrics.HammingLoss(mode='multilabel')}
loaded_model = load_model(model_path, custom_objects=custom_objects)

print("Model Loaded")


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

def predict(text, tokenizer = tokenizer, labels_list = labels_list, preprocessed = False, top_k = 5):
  """
  Input:
    text: input text
    tokenizer: word tokenizer for the text
    labels_list: list of all the labels we have in our data
    preprocessed: Whether the input data is already processed or not
    top_k: no. of labels to be returned along with their probabililties

  Output:
    top_k no. of labels along with their corresponding probabilities
  """
  if not preprocessed:
    text = text_preprocess(text)
  text_sequence = tokenizer.texts_to_sequences([text])
  text_padded = pad_sequences(text_sequence, maxlen = MAX_PAD_LENGTH, padding = "post", truncating = "post")
  predictions = list(loaded_model.predict(text_padded)[0])
  # get the indices of top three values
  top_indices = [i for i, val in sorted(enumerate(predictions), key=lambda x: x[1], reverse=True)[:top_k]]
  # Create a new list with 1s for top three indices and 0s for the rest
  prediction_list = [1 if i in top_indices else 0 for i in range(len(predictions))]
  
  # For top k labels, the label name and their corresponding probabilities are provided
  labels = [labels_list[i] for i in range(len(labels_list)) if prediction_list[i] == 1]
  prediction_probabilities = [predictions[i] for i in range(len(predictions)) if prediction_list[i] == 1]
  result = {label: probability for label, probability in zip(labels, prediction_probabilities)}

  return result

