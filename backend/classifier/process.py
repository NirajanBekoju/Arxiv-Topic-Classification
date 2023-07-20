from keras_preprocessing.sequence import pad_sequences
from model.load_models import tokenizer, labels_list, MAX_PAD_LENGTH, loaded_model, text_preprocess

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

