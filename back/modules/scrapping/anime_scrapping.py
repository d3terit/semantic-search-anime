import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www3.animeflv.net/"

def get_anime_ids_page(page_num):
    url = f"{BASE_URL}?page={page_num}"
    print(f"Obteniendo ids de animes de la página {page_num}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        anime_links = soup.select('article.Anime > a')
        anime_ids = [link['href'].split('/')[-1] for link in anime_links]
        return anime_ids
    else:
        print(f"Error al obtener la página {page_num}")
        return []

def get_anime_ids():
    print("Obteniendo ids de animes")
    content = requests.get(BASE_URL+'/browse').content
    soup = BeautifulSoup(content, 'html.parser')
    num_pages = int(soup.select('ul.pagination > li > a')[-2].text)
    print(f"Se obtuvieron {num_pages} páginas de animes")
    anime_ids = []
    for page in range(1, num_pages+1):
        anime_ids += get_anime_ids_page(page)
    print(f"Se obtuvieron {len(anime_ids)} animes", anime_ids)
    # guardar en csv los id
    with open('anime_ids.csv', 'w') as file:
        for id in anime_ids:
            file.write(f"{id}\n")
    return anime_ids

def check_animes_registered():
    try:
        content = requests.get(BASE_URL+'/browse').content
        soup = BeautifulSoup(content, 'html.parser')
        print(soup)
        return True
    except Exception as e:
        print(e)
        return False
    
def get_animes():
    print("Checking animes registered")
    try:
        content = requests.get(BASE_URL+'/browse').content
        soup = BeautifulSoup(content, 'html.parser')
        selectedElements = soup.select('body > div.Wrapper > div > div > main > ul > li')
        if selectedElements:
            data = []
            for el in selectedElements:
                try:
                    data.append({
                        'title': el.find('h3').text.strip(),
                        'cover': el.find('img')['src'],
                        'synopsis': el.select('div.Description > p')[1].text.strip(),
                        'id': el.find('a')['href'].replace("/anime/", ""),
                        'type': el.find('span').text.strip()
                    })
                except Exception as e:
                    print(e)
            print("Animes registered: ", data)
            return data
        else:
            return []
    except Exception as e:
        print(e)
        return []