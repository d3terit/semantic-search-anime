from transformers import BertTokenizer, BertModel
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_embeddings(anime_data):
    # Combinar campos de texto y numéricos
    combined_text = f"{anime_data['url']} {anime_data['type']} {anime_data['title']} {anime_data['description']} {anime_data['state']} {' '.join(anime_data['tags'])} "
    combined_text += f"{' '.join(anime_data['other_names'])}  {anime_data['votes_prmd']} {anime_data['votes_nmbr']} {anime_data['followers']}"

    # Normalizar texto, tokenizar y obtener embeddings
    inputs = tokenizer(combined_text, return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    text_embeddings = outputs.last_hidden_state.mean(dim=1).tolist()
    return text_embeddings[0]

def calculate_embeddings(animes):
    for anime in animes:
        anime['embeddings'] = get_embeddings(anime)
    return animes

def embedding_search(search):
    inputs = tokenizer(search, return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    text_embeddings = outputs.last_hidden_state.mean(dim=1).tolist()
    return text_embeddings[0]