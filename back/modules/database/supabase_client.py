import dotenv
from supabase import create_client, Client

url: str = dotenv.get_key(dotenv.find_dotenv(), "SUPABASE_URL")
key: str = dotenv.get_key(dotenv.find_dotenv(), "SUPABASE_KEY")

supabase: Client = create_client(url, key)

def insert_animes(animes):
    return supabase.table('animes').insert(animes).execute()

def get_last_anime_registered():
    data = supabase.table('animes').select("url").order('id', desc=True).limit(1).execute().data
    if data:
        return data[0]['url']
    else:
        return None

def search_animes(query_embedding):
    return supabase.rpc('match_animes', {"query_embedding": query_embedding, "match_threshold": 0.2, "match_count": 3}).execute().data