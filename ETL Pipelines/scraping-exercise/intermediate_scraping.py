import time

import requests
from bs4 import BeautifulSoup
from transform import transform_data, transform_to_DataFrame
from store_to_db import store_to_postgre

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
  """Retrieves HTML content from a given URL."""
  session = requests.Session()
  response = session.get(url, headers=HEADERS)
  try:
    response.raise_for_status()
    return response.content
  except requests.exceptions.RequestException as e:
    print(f"An error occurred while making a request to {url}: {e}")
    return None
  
def extract_book_data(article):
  """Retrieving book data in the form of title, price, availability, and rating from the article (html element)."""
  book_title = article.find('h3').text
  product_element = article.find('div', class_='product_price')
  price = product_element.find('p', class_='price_color').text
  availability_element = product_element.find('p', class_='instock availability')
  available = "Available" if availability_element else "Not Available"

  rating_element = article.find('p', class_='star-rating')
  rating = rating_element['class'][1] if rating_element else 'Rating not found'

  books = {
    "Title": book_title,
    "Price": price,
    "Availability": available,
    "Rating": rating
  }

  return books

def scrape_book(base_url, start_page=1, delay=2):
  """The main function is to retrieve all data, starting from requests to storing it in data variables."""
  data = []
  page_number = start_page

  while True:
    url = base_url.format(page_number)
    print(f"Scraping page: {url}")
    content = fetching_content(url)
    if content:
      soup = BeautifulSoup(content, 'html.parser')
      articles_element = soup.find_all('article', class_='product_pod')
      for article in articles_element:
        book = extract_book_data(article)
        data.append(book)

      next_button = soup.find('li', class_='next')
      if next_button:
        page_number += 1
        time.sleep(delay) # Delay before next page
      else:
        break # Stop if there is no next button
    else:
      break # Stop if there is an error
  
  return data

def main():
  """The main function for the entire scraping process to saving it."""
  BASE_URL = 'https://books.toscrape.com/catalogue/page-{}.html'
  all_books_data = scrape_book(BASE_URL)
  if all_books_data:
    DataFrame = transform_to_DataFrame(all_books_data)
    DataFrame = transform_data(DataFrame, 20000)

    # Save Data to PostgreSQL
    db_url = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/booksdb'
    store_to_postgre(DataFrame, db_url)
  else:
    print("No data found.")

if __name__ == '__main__':
  main()