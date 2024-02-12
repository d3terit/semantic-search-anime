from .scrapping.anime_scrapping import check_animes_registered, get_animes, get_anime_ids
from .embedding.anime_embedding import calculate_embeddings
from .database.supabase_client import insert_animes, search_animes

def semantic_search(data):
    get_anime_ids()
    # if not check_animes_registered():
    #     new_animes = get_animes()
    #     formatted_animes = calculate_embeddings(new_animes)
    #     insert_animes(formatted_animes)
    return search_animes(data)