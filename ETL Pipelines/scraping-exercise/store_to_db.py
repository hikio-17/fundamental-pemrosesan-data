from sqlalchemy import create_engine

def store_to_postgre(data, db_url):
  """Function to save data into PostgreSQL."""
  try:
    # Create Engine Database
    engine = create_engine(db_url)

    # Save data to table 'bookstoscrape' if table already exists, data will be appended
    with engine.connect() as connection:
      data.to_sql('bookstoscrape', con=connection, if_exists='append', index=False)
  except Exception as e:
    print(f"An error occurred while saving data: {e}")