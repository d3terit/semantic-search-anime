from transformers import BertTokenizer, BertModel
import torch
import spacy

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

nlp = spacy.load("en_core_web_sm")

# Atributos que se utilizarán para obtener los embeddings
attributes = [ "type", "title", "description", "state", "tags", "other_names", "votes_prmd", "votes_nmbr", "followers"]

# Tokenizar y lematizar el texto utilizando spaCy
def preprocess_text(text):
    doc = nlp(str(text))
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop]
    return " ".join(lemmatized_tokens)

def get_embeddings(anime_data):
    combined_text = " ".join([key + ": " + preprocess_text(anime_data[key]) for key in attributes])

    # Normalizar texto, tokenizar y obtener embeddings
    inputs = tokenizer(combined_text, return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    text_embeddings = outputs.last_hidden_state.mean(dim=1).tolist()
    return text_embeddings[0]

def calculate_embeddings(animes):
    print("\nCalculando embeddings de animes")
    for index in range(len(animes)):
        print(f"{index+1}/{len(animes)}", end="\r")
        animes[index]['embeddings'] = get_embeddings(animes[index])
    return animes

def embedding_search(search):
    inputs = tokenizer(preprocess_text(search), return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    text_embeddings = outputs.last_hidden_state.mean(dim=1).tolist()
    return text_embeddings[0]