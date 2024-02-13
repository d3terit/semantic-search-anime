from .scrapping.anime_scrapping import get_new_animes_to, get_anime_register
from .embedding.anime_embedding import calculate_embeddings, embedding_search
from .database.supabase_client import insert_animes, search_animes, get_last_anime_registered

def semantic_search(search):
    last_register = get_last_anime_registered()
    last_published = get_anime_register()
    print(last_register, last_published)
    if(last_register != last_published):
        new_animes = get_new_animes_to(last_register)
        formatted_animes = calculate_embeddings(new_animes)
        insert_animes(formatted_animes)
    formatted_search = embedding_search(search)
    return search_animes(formatted_search)