import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Setup path to be able to import from utils folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.load import store_to_postgre, store_to_googlesheet, store_to_csv

# Fixture: Dummy data to be used in all tests
@pytest.fixture
def sample_df():
    data = {
        'Title': ['Baju A', 'Celana B'],
        'Price': [100000.0, 50000.0],
        'Rating': [4.5, 4.0]
    }
    return pd.DataFrame(data)

# 1. Test Store to PostgreSQL
@patch('utils.load.create_engine') # Mock sqlalchemy engine
@patch('pandas.DataFrame.to_sql')  # Mock pandas to_sql to avoid shooting the real DB
def test_store_to_postgre(mock_to_sql, mock_create_engine, sample_df):
    """Test whether the DB connection is made and to_sql is called."""
    
    # Setup Mock Engine & Connection
    mock_engine = MagicMock()
    mock_connection = MagicMock()
    
    mock_create_engine.return_value = mock_engine
    # Mocking context manager: with engine.connect() as connection
    mock_engine.connect.return_value.__enter__.return_value = mock_connection

    # Action
    store_to_postgre(sample_df)

    # Assert
    # 1. Make sure create_engine is called
    mock_create_engine.assert_called_once()
    
    # 2. Make sure dataframe.to_sql is called with the correct arguments.
    mock_to_sql.assert_called_once_with(
        'productstoscrape', 
        con=mock_connection, 
        if_exists='append', 
        index=False
    )

# 2. Test Store to Google Sheets
@patch('utils.load.Credentials.from_service_account_file') # Mock Auth Google
@patch('utils.load.build') # Mock Google API Build
def test_store_to_googlesheet(mock_build, mock_credentials, sample_df):
    """Test the update flow to Google Sheets without real API hits"""

    # Setup Mock Service Google Sheet
    mock_service = MagicMock()
    mock_sheets = MagicMock()
    mock_values = MagicMock()
    mock_update = MagicMock()
    
    # Chain Mocking (Chaining): service.spreadsheets().values().update().execute()
    mock_build.return_value = mock_service
    mock_service.spreadsheets.return_value = mock_sheets
    mock_sheets.values.return_value = mock_values
    mock_values.update.return_value = mock_update
    mock_update.execute.return_value = {"updatedCells": 10} # API success response simulation

    # Action
    store_to_googlesheet(sample_df)

    # Assert
    # 1. Make sure credentials is called (even if the json file is not in the test env)
    mock_credentials.assert_called_once_with('google-sheets-api.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
    
    # 2. Make sure the update function is called
    mock_values.update.assert_called_once()
    
    # 3. Check whether the body values ​​parameter matches the dataframe data
    # args[0] and kwargs take the arguments passed to the update function
    _, kwargs = mock_values.update.call_args 
    assert kwargs['spreadsheetId'] == '1UvBn9aNct8hyrtsSdj8kNqcAA_EDzyt_-As2MfqLiwE'
    assert kwargs['range'] == 'productstoscrape!A1'
    assert kwargs['valueInputOption'] == 'USER_ENTERED'
    
    # Make sure the data sent is not empty
    sent_values = kwargs['body']['values']
    assert len(sent_values) == 3 # 1 row header + 2 rows data

# 3. Test Store to CSV
@patch('pandas.DataFrame.to_csv') # Mock function to_csv
def test_store_to_csv(mock_to_csv, sample_df):
    """Test whether the to_csv function is called"""
    
    # Action
    store_to_csv(sample_df)
    
    # Assert
    # Make sure the file is saved with the correct name.
    mock_to_csv.assert_called_once_with("products.csv", index=False)