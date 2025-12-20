import pandas as pd

def transform_to_DataFrame(data):
  df = pd.DataFrame(data)
  return df

def transform_data(data, excange_rate):
  # Clean Data
  cond_drop = data["Rating"].str.contains("Invalid Rating") | (data["Title"] == "Unknown Product") | (data["Price"] == "Price Unavailable")
  data.drop(data[cond_drop].index, inplace=True)

  data['Title'] = data['Title'].astype('string')
  data['Price'] = data['Price'].astype('string')
  data['Color'] = data['Price'].astype('string')

  # Tranform Price
  data["Price"] = data["Price"].astype(str).str.replace(r"[^0-9.]", "", regex=True).astype(float)

  # Transform Exchange Rate
  data['Price'] = (data['Price'] * excange_rate).astype(int)

  # Transform Rating
  data['Rating'] = (data["Rating"].str.extract(r"(\d+\.\d+|\d+)", expand=False)).astype(float)

  # Transform Color to Int
  data["Color"] = data["Color"].str.extract(r"(\d+)").astype(int)

  # Transform Size to String
  data["Size"] = data["Size"].str.extract(r"([A-Z]+)").astype('string')

  # Transform Gender to String
  data["Gender"] = data["Gender"].str.extract(r"Gender:\s*(\w+)").astype("string")
  return data
