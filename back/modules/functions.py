from .scrapping.anime_scrapping import get_anime_info, get_anime_register, get_anime_ids_to
from .embedding.anime_embedding import calculate_embeddings, embedding_search
from .database.supabase_client import insert_animes, search_animes, get_last_anime_registered

def semantic_search(data):
    last_register = get_last_anime_registered()
    last_published = get_anime_register()
    print(last_register, last_published)
    if(last_register != last_published):
        new_anime_ids = get_anime_ids_to(last_register)[::-1]
        for i in range(0, len(new_anime_ids), 100):
                new_animes = []
                for j in range(i, i+100):
                    print(f"{j+1}/{len(new_anime_ids)} {new_anime_ids[j]}", end="\r")
                    anime_info = get_anime_info(new_anime_ids[j])
                    if anime_info:
                        new_animes.append(anime_info)
                new_animes = calculate_embeddings(new_animes)
                insert_animes(new_animes)
    formatted_search = embedding_search(data['query'])
    return search_animes(formatted_search, data['match_threshold'], data['match_count'])