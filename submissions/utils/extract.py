import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

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
    print(f"Error fetching website: {e}")
    return None
  except Exception as e:
    print(f"An error occured during scraping: {e}")
    return None
  
def extract_product_data(collection_card):
  """Retrieving book data in the form of title, price, availability, and rating from the article (html element)."""
  # product_image = collection_card.find('img', class__='collection_image')['src']
  product_details_element = collection_card.find('div', class_='product-details')
  title = product_details_element.find('h3', class_='product-title').text
  price = product_details_element.find(class_='price').text
  rating = product_details_element.find_all('p', recursive=True)[0].text
  color = product_details_element.find_all('p', recursive=True)[1].text
  size = product_details_element.find_all('p', recursive=True)[2].text
  gender = product_details_element.find_all('p', recursive=True)[3].text

  products = {
    'Title': title,
    'Price': price,
    'Rating': rating,
    'Color': color,
    'Size': size,
    'Gender': gender,
  }

  return products

def scrape_product(base_url, start_page=1, delay=2):
  """The main function is to retrieve all data, starting from requests to storing it in data variables."""
  data = []
  page_number = start_page

  while page_number <= 3:
    url = base_url.format(page_number) if page_number > start_page else base_url
    print(f"Scraping page: {url}")

    content = fetching_content(url)

    if content:
      soup = BeautifulSoup(content, 'html.parser')
      collection_card_element = soup.find_all('div', class_='collection-card')
      for collection_card in collection_card_element:
        product = extract_product_data(collection_card)
        data.append(product)
      
      next_button = soup.find('page-item next')

      if next_button and not 'disabled' in next_button.get('class', []):
        page_number += 1
        time.sleep(delay) # Delay before next page
      else:
        break # Stop if there is no next button
    else:
      break # Stop if there is an error

  return data

def scrape_main():
  """The main function for the entire scraping process to saving it."""
  BASE_URL = "https://fashion-studio.dicoding.dev"
  all_products_data = scrape_product(BASE_URL)
  df = pd.DataFrame(all_products_data)
  print(df)


if __name__ == '__main__':
  scrape_main()

