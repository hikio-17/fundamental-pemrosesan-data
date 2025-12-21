from utils.extract import scrape_product
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import store_to_csv, store_to_googlesheet, store_to_postgre

def main():
  """The main function for the entire scraping process to saving it."""
  BASE_URL = "https://fashion-studio.dicoding.dev"
  all_products_data = scrape_product(BASE_URL)
  if all_products_data:
    DataFrame = transform_to_DataFrame(all_products_data)
    DataFrame = transform_data(DataFrame, 16000)

    # Store data to Repository
    store_to_csv(DataFrame)
    # store_to_postgre(DataFrame)  # Uncomment if use Repository Postrges
    store_to_googlesheet(DataFrame)
  else:
    print("No data found.")

if __name__ == '__main__':
  main()