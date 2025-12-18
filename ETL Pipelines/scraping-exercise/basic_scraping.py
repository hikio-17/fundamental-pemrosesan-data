import requests
import pandas as pd
from bs4 import BeautifulSoup

# Add user-agent to the header to avoid blocking by the server.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}


def extract_tourism_data(section):
    """Extracting tourist attraction data from a single <section> element."""
    tourist_extraction = section.find('h3').text
    description = section.find('p').text.replace('\n', '').strip()
    image_url = section.find('img')['src']

    return {
        "Tourist Extraction" :tourist_extraction,
        "Description" :description,
        "Image Url" :image_url,
    }


def fetch_page_content(url):
    """Retrieves HTML content from a URL with the specified user-agent."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise HTTPError for bad status
        print('response===> ', response)
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error while retrieving {url}: {e}")
        return None


def scrape_tourism_data(url):
    """Perform scraping for all tourist attractions data."""
    content = fetch_page_content(url)
    if not content:
        return []  # Return an empty list if it fails to fetch content.

    soup = BeautifulSoup(content, 'html.parser')
    data = []
    articles = soup.find('article', id='wisata', class_='card')

    if articles:
        # Navigate using .descendants to find <section>
        sections = [
            desc for desc in articles.descendants if desc.name == 'section']
        for section in sections:
            tourism_data = extract_tourism_data(section)
            data.append(tourism_data)
    return data


def main():
    """The main function is to run the scraping process and store data."""
    url = 'https://halaman-profil-bandung-grid.netlify.app/'
    tourism_data = scrape_tourism_data(url)

    if tourism_data:
        df = pd.DataFrame(tourism_data)
        print(df)
    else:
        print("No data found.")

if __name__ == "__main__":
    main()
