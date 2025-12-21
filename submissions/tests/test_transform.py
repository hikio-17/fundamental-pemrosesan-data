import pandas as pd
import sys
import os

# Setup path to be able to import from utils folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.transform import transform_to_DataFrame, transform_data

# 1. Test transform_to_DataFrame
def test_transform_to_dataframe():
    """Ensure that the list of dictionaries is successfully converted into a DataFrame."""
    raw_data = [
        {"Title": "Baju A", "Price": "$10"},
        {"Title": "Baju B", "Price": "$20"}
    ]
    
    df = transform_to_DataFrame(raw_data)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "Title" in df.columns
    assert "Price" in df.columns

# 2. Test transform_data (Success)
def test_transform_data_success():
    """Valid data transformation logic test (Regex & Calculation)"""
    
    # Simulation raw data
    data = {
        "Title": ["Super Shirt", "Cool Pants"],
        "Price": ["$100.00", "$50.50"],     
        "Rating": ["Rating: ⭐ 4.5 / 5", "Rating: ⭐ 3.0 / 5"], 
        "Color": ["3 Colors", "1 Colors"],    
        "Size": ["Size: M", "Size: XL"],      
        "Gender": ["Gender: Men", "Gender: Women"] 
    }
    df_input = pd.DataFrame(data)
    
    # For example, the dollar to rupiah exchange rate = 15,000
    exchange_rate = 15000 
    
    # Run Function
    df_result = transform_data(df_input, exchange_rate)

    # --- ASSERTIONS ---
    
    # 1. Check Price (Must be float and multiplied by exchange rate)
    # $100.00 * 15000 = 1.500.000
    assert df_result.iloc[0]["Price"] == 1500000.0 
    # $50.50 * 15000 = 757.500
    assert df_result.iloc[1]["Price"] == 757500.0
    assert pd.api.types.is_float_dtype(df_result["Price"])

    # 2. Check Rating (Must be pure float)
    assert df_result.iloc[0]["Rating"] == 4.5
    assert df_result.iloc[1]["Rating"] == 3.0
    assert pd.api.types.is_float_dtype(df_result["Rating"])

    # 3. Check Color (Must be int)
    assert df_result.iloc[0]["Color"] == 3
    assert df_result.iloc[1]["Color"] == 1
    assert pd.api.types.is_integer_dtype(df_result["Color"])

    # 4. Check Size & Gender (Must have clean string)
    assert df_result.iloc[0]["Size"] == "M"
    assert df_result.iloc[1]["Gender"] == "Women"

# 3. Test transform_data (Filtering / Cleaning)
def test_transform_data_filtering():
    """Test whether the junk data (Unknown/Invalid) is really deleted."""
    
    data = {
        "Title": [
            "Valid Product", 
            "Unknown Product",    # Must be deleted
            "Product C", 
            "Product D"
        ],
        "Price": [
            "$10.00", 
            "$10.00", 
            "Price Unavailable",  # Must be deleted
            "$20.00"
        ],
        "Rating": [
            "Rating: 4.5", 
            "Rating: 4.5", 
            "Rating: 4.5", 
            "Rating: ⭐ Invalid Rating / 5" # Must be deleted
        ],
        # The other columns are just dummy so there are no errors.
        "Color": ["1 Colors", "1 Colors", "1 Colors", "1 Colors"],
        "Size": ["Size: S", "Size: S", "Size: S", "Size: S"],
        "Gender": ["Gender: M", "Gender: M", "Gender: M", "Gender: M"]
    }
    
    df_input = pd.DataFrame(data)
    
    # Run function Transform Data
    df_result = transform_data(df_input, 10000)
    
    # --- ASSERTIONS ---
    
    # Of the 4 data, 3 contain errors in different columns.
    # There should only be 1 data remaining ("Valid Product").
    assert len(df_result) == 1
    assert df_result.iloc[0]["Title"] == "Valid Product"