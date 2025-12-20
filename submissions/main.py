from utils.extract import scrape_product
from utils.transform import transform_to_DataFrame, transform_data

def main():
  """The main function for the entire scraping process to saving it."""
  BASE_URL = "https://fashion-studio.dicoding.dev"
  all_products_data = scrape_product(BASE_URL)
  if all_products_data:
    DataFrame = transform_to_DataFrame(all_products_data)
    DataFrame = transform_data(DataFrame, 16000)

    print(len(DataFrame))

    print(DataFrame.duplicated().sum())
    print(DataFrame.isnull().sum())
    print(DataFrame.isna().sum())
    print("Duplicate rows:", DataFrame.duplicated().sum())
    print("Null / NaN:")
    print(DataFrame.isna().sum())

    print("Empty string:")
    print(DataFrame.apply(lambda col: col.astype(str).str.strip().eq("").sum()))
  else:
    print("No data found.")

if __name__ == '__main__':
  main()