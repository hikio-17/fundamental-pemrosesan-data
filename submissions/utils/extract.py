import time

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


def extract_product_data(card):
    product = {}

    # 1. Put Title
    title_tag = card.find("h3", class_="product-title")
    product['Title'] = title_tag.get_text(strip=True) if title_tag else None

    # 2. Get Price (Search by class "price", no matter if it's span, div, or p)
    price_tag = card.find(class_="price")
    product['Price'] = price_tag.get_text(
        strip=True) if price_tag else "Price Unavailable"

    # 3. Get the remaining data (Rating, Color, Size, etc.) contained within the <p> tag.
    details_div = card.find("div", class_="product-details")

    if details_div:
        # Take all p, but ignore if it is a price (in case price is at p)
        all_p_tags = [p for p in details_div.find_all(
            "p") if "price" not in p.get("class", [])]
    else:
        all_p_tags = []

    # Default values
    product['Rating'] = None
    product['Color'] = None
    product['Size'] = None
    product['Gender'] = None

    for p in all_p_tags:
        text = p.get_text(strip=True)

        if "Rating" in text:
            product['Rating'] = text
        elif "Colors" in text: 
            product['Color'] = text
        elif "Size" in text:
            product['Size'] = text
        elif "Gender" in text:
            product['Gender'] = text

    product['Timestamp'] = datetime.now().isoformat()
    return product


def scrape_product(base_url, start_page=1, delay=2):
    """The main function is to retrieve all data, starting from requests to storing it in data variables."""
    data = []
    page_number = start_page

    while True:
        if (page_number == 1):
            url = base_url
        else:
            url = base_url + "/page{}".format(page_number)
        print(f"Scraping page: {url}")

        content = fetching_content(url)

        if True:
            soup = BeautifulSoup(content, 'html.parser')
            collection_card_element = soup.find_all(
                'div', class_='collection-card')
            for collection_card in collection_card_element:
                product = extract_product_data(collection_card)
                data.append(product)

            next_button = soup.find('li', class_='page-item next')

            if next_button and not 'disabled' in next_button.get('class', []):
                page_number += 1
                time.sleep(delay)  # Delay before next page
            else:
                break  # Stop if there is no next button
        else:
            break  # Stop if there is an error

    return data
