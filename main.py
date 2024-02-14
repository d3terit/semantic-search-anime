from transformers import BertTokenizer, BertModel
import torch
import spacy #pip install spacy

# Inicializar el tokenizer y el modelo de BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Inicializar spaCy para el análisis de texto avanzado
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    # Tokenizar y lematizar el texto utilizando spaCy
    doc = nlp(text)
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop]
    return " ".join(lemmatized_tokens)

def get_embeddings(text):
    # Preprocesar el texto
    preprocessed_text = preprocess_text(text)
    # Tokenizar y obtener los embeddings con BERT
    inputs = tokenizer(preprocessed_text, return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    text_embeddings = outputs.last_hidden_state.mean(dim=1).tolist()
    return text_embeddings[0]

# Ejemplo de uso
search_query = "espacio estertor, naves espaciales y marte"
query_embedding = get_embeddings(search_query)

# Realizar la búsqueda de animes utilizando embeddings
def search_animes(query_embedding, anime_descriptions):
    anime_embeddings = [get_embeddings(description) for description in anime_descriptions]
    query_embedding_tensor = torch.tensor(query_embedding)
    similarities = [torch.cosine_similarity(query_embedding_tensor, torch.tensor(embedding), dim=0).item() for embedding in anime_embeddings]
    sorted_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)
    return sorted_indices, similarities

# Descripciones de anime (ejemplo)
anime_descriptions = [
    "En un mundo donde los demonios y los humanos coexisten, los seres humanos viven en constante temor de los demonios que habitan en el bosque. Sin embargo, los humanos han aprendido a invocar a los cazadores de demonios legendarios para protegerlos del mal. Tanjiro Kamado es un joven que ha perdido a su familia a manos de un demonio, y su única hermana, Nezuko, se ha convertido en un demonio. Determinado a vengar a su familia y salvar a su hermana, Tanjiro se embarca en un viaje para convertirse en un cazador de demonios.",
    "En el año 2022, la humanidad creó la primera VRMMO, 'Sword Art Online' (SAO), donde los jugadores pueden controlar sus avatares con sus mentes. Sin embargo, los jugadores se quedan atrapados en el juego por su creador, Kayaba Akihiko, y solo pueden salir completando los 100 niveles del juego. Si mueren en el juego, también mueren en la vida real. Kirito, uno de los jugadores atrapados, se embarca en una misión para completar el juego y liberar a todos los jugadores.",
    "En un futuro distópico, la humanidad ha colonizado Marte y la Tierra está al borde de la destrucción. Los jóvenes guerreros conocidos como los Mobile Suit Pilots luchan en una guerra interplanetaria entre la Federación Terrestre y la República de Zeon. Uno de esos pilotos es Amuro Ray, quien se encuentra piloteando el prototipo de Mobile Suit RX-78-2 Gundam. A medida que la guerra avanza, Amuro se ve envuelto en un conflicto más grande y debe luchar no solo por la supervivencia, sino también por la paz.",
    "Sakura Kinomoto es una joven de 10 años que descubre un libro mágico en el sótano de su casa. Sin saberlo, libera accidentalmente las Cartas Clow, poderosos espíritus mágicos creados por el mago Clow Reed. Keroberos, el guardián del libro, le dice a Sakura que debe recuperar las Cartas Clow antes de que causen estragos en el mundo. Con la ayuda de sus amigos y su nueva identidad como Cardcaptor, Sakura emprende una aventura para capturar las cartas y convertirse en la maga más poderosa.",
    "El mundo de los piratas es peligroso y emocionante, lleno de tesoros ocultos y batallas épicas. Monkey D. Luffy sueña con convertirse en el Rey de los Piratas y encuentra la legendaria One Piece, el tesoro más grande de todos. Con su tripulación de piratas, los Piratas del Sombrero de Paja, Luffy navega por el Grand Line en busca de aventuras y desafíos. Pero el camino hacia el One Piece está lleno de poderosos enemigos y obstáculos inesperados."
]

# Buscar animes relevantes
relevant_anime_indices, similarity_scores = search_animes(query_embedding, anime_descriptions)
relevant_animes = [(anime_descriptions[i], similarity_scores[i]) for i in relevant_anime_indices]
print("Animes relevantes:")
for anime, score in relevant_animes:
    print(f"Descripción: {anime}\nProbabilidad: {score}\n")
