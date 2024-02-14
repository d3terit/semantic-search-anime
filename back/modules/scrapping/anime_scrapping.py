import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www3.animeflv.net/"

def get_anime_register():
    try:
        content = requests.get(BASE_URL+'/browse?order=added').content
        soup = BeautifulSoup(content, 'html.parser')
        selectedElements = soup.select('article.Anime > a')
        if selectedElements:
            return selectedElements[0]['href'].split('/')[-1]
        else:
            return None
    except Exception as e:
        print(e)
        return None

def get_anime_ids_page(page_num, num_pages, last_register):
    url = f"{BASE_URL}/browse?order=added&page={page_num}"
    print(f"{page_num}/{num_pages}", end="\r")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        anime_links = soup.select('article.Anime > a')
        anime_ids = [link['href'].split('/')[-1] for link in anime_links]
        if last_register in anime_ids:
            return anime_ids[:anime_ids.index(last_register)]
        if page_num < num_pages:
            return anime_ids + get_anime_ids_page(page_num+1, num_pages, last_register)
        return anime_ids
    else:
        print(f"Error al obtener la página {page_num}")
        return []

def get_anime_ids_to(last_register):
    print("Obteniendo ids de animes")
    content = requests.get(BASE_URL+'/browse').content
    soup = BeautifulSoup(content, 'html.parser')
    num_pages = int(soup.select('ul.pagination > li > a')[-2].text)
    print(f"Se obtuvieron {num_pages} páginas de animes")
    print(f"Obteniendo ids de animes desde {last_register}")
    anime_ids = get_anime_ids_page(1, num_pages, last_register)
    print(f"Se obtuvieron {len(anime_ids)} animes nuevos")
    return anime_ids

def get_anime_info(anime_id):
    url = f"{BASE_URL}/anime/{anime_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return {
                "url": anime_id,
                "type": soup.select('span.Type')[0].text,
                "title": soup.select('h1.Title')[0].text,
                "description": soup.select('div.Description > p')[0].text,
                "votes_prmd": float(soup.select('span.vtprmd')[0].text),
                "votes_nmbr": int(soup.select('span#votes_nmbr')[0].text),
                "state": soup.select('span.fa-tv')[0].text,
                "tags": [tag.text for tag in soup.select('nav.Nvgnrs > a')],
                "other_names": [name.text for name in soup.select('span.TxtAlt')],
                "cover": soup.select('div.AnimeCover img')[0]['src'],
                "followers": int(soup.select('section.WdgtCn div.Title > span')[0].text)
            }
        else:
            print(f"Error al obtener el anime {anime_id}")
            return None
    except Exception as e:
        print(e)
        return None