import pandas as pd

def transform_to_DataFrame(data):
  """Convert data into a DataFrame."""
  df = pd.DataFrame(data)
  return df

def transform_data(data, exchange_rate):
  """Combines all data transformations into one function."""
  # Transformasi Price
  data['Price_in_pounds'] = data['Price'].replace('£', '', regex=True).astype(float)

  # Transformasi Rating
  rating_mapping = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
  }

  data['Rating'] = data['Rating'].replace(rating_mapping)

  # Transformasi Exchange Rate
  data['Price_in_rupiah'] = (data['Price_in_pounds'] * exchange_rate).astype(int)

  # Delete Column Redundant
  data = data.drop(columns=['Price'])

  # Transformasi Data Type
  data['Title'] = data['Title'].astype('string')
  data['Availability'] = data['Availability'].astype('string')

  return data