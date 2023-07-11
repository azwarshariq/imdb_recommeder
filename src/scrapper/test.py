import requests
from bs4 import BeautifulSoup

URL = "https://www.imdb.com/search/title/?genres=Action&languages=en&sort=user_rating%2Cdesc&title_type=feature&num_votes=10000%2C&explore=genres&ref_=ft_eng_0"

# Define the header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
}

# Send the request with the header
r = requests.get(URL, headers=headers)

soup = BeautifulSoup(r.content, 'html.parser')

movie_containers = soup.find_all('div', class_='lister-item-content')

for container in movie_containers:
    movie_title = container.h3.a.text
    movie_genre = container.find('span', class_='genre').text.strip()
    movie_summary = container.find('p', class_='text-muted').text.strip()

    span = container.find('span', class_='rating-cancel')
    if span:
        sibling_p = span.find_next_sibling('p', class_='text-muted')
        if sibling_p:
            text = sibling_p.text.strip()
            print(text)
        
    print(f"Title: {movie_title}")
    print(f"Genre: {movie_genre}")
    print(f"Summary: {movie_summary}\n")
    break
