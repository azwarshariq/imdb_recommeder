import requests
import csv
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
}

# Function to extract summaries from a given container
def extract_summaries(container):
    summaries = container.find_all('p', class_='text-muted')
    summary_list = []
    for summary in summaries:
        if 'Directors:' in summary.text:
            break
        summary_text = summary.get_text(strip=True)
        if summary_text:
            summary_list.append(summary_text)
    if summary_list:
        summary_list.pop(0)  # Remove the unwanted part
    return summary_list

    
# Function to process a single page and append data to CSV
def process_page(url, genre):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    movie_containers = soup.find_all('div', class_='lister-item-content')

    if not movie_containers:
        return True
    
    with open(f'data/{genre}_movie_data.csv', 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for container in movie_containers:
            movie_title = container.h3.a.text
            movie_year = container.find('span', class_='lister-item-year').text.strip('()')
            movie_genre = container.find('span', class_='genre').text.strip()
            summary_list = extract_summaries(container)
            csv_writer.writerow([f"{movie_title} ({movie_year})", movie_genre, ' '.join(summary_list)])

    return False
    
# Define the list of URLs and genres to process
url_genre_map = {
    "https://www.imdb.com/search/title/?title_type=feature&genres=adventure": "Adventure",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Action": "Action",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Drama": "Drama",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Comedy": "Comedy",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Fantasy": "Fantasy",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Family": "Family",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Romance": "Romance",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Sci-Fi": "Sci-Fi",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Thriller": "Thriller",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Animation": "Animation",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Crime": "Crime",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Mystery": "Mystery",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Horror": "Horror",
    "https://www.imdb.com/search/title/?title_type=feature&genres=History": "History",
    "https://www.imdb.com/search/title/?title_type=feature&genres=War": "War",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Western": "Western",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Musical": "Musical",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Music": "Music",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Biography": "Biography",
    "https://www.imdb.com/search/title/?title_type=feature&genres=Sport": "Sport",
}

# Iterate through each URL and process the pages
for url, genre in url_genre_map.items():
    page_url = url

    count = 0
    while page_url:
        should_move_to_next_url = process_page(page_url, genre)
        if should_move_to_next_url:
            break

        r = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        next_link = soup.find('a', class_='lister-page-next')
        if count < 19:
            if next_link:
                page_url = "https://www.imdb.com" + next_link['href']
                count += 1
        else:
            page_url = None
            
        
    count = 0

print("Movie data has been appended to separate CSV files.")