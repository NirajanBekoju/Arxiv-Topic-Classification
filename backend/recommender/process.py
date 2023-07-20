from keras_preprocessing.sequence import pad_sequences
from model.load_models import tokenizer, MAX_PAD_LENGTH, second_last_layer_model, text_preprocess, training_matrix, database
import numpy as np 


def getFeatures(text):
    """
    Input:
    text: input text
    tokenizer: word tokenizer for the text
    preprocessed: Whether the input data is already processed or not

    Output:
    top_k no. of labels along with their corresponding probabilities
    """
    text = text_preprocess(text)
    text_sequence = tokenizer.texts_to_sequences([text])
    text_padded = pad_sequences(text_sequence, maxlen = MAX_PAD_LENGTH, padding = "post", truncating = "post")
    output = second_last_layer_model.predict(text_padded)
    output = output.flatten()
    return output


def cosineSimilarity(input_data, matrix):
    # Calculate the dot product between the input data and the matrix
    dot_product = np.dot(input_data, matrix.T)

    # Calculate the norms of the input data and each column of the matrix
    input_norm = np.linalg.norm(input_data)
    matrix_norms = np.linalg.norm(matrix, axis=1)

    # Calculate the cosine similarity using broadcasting
    similarity = dot_product / (input_norm * matrix_norms + 1e-10)  # Adding a small value to avoid division by zero
    return similarity




def getRecommendation(text, top_k = 3):
    input_features = getFeatures(text)

    similarity_scores = cosineSimilarity(input_features, training_matrix)

    print(similarity_scores)
    indices_of_top_k = np.argsort(-similarity_scores.flatten())[:top_k]
    print(indices_of_top_k)
    
    return database.iloc[indices_of_top_k].to_dict(orient="records")