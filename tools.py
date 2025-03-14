import os, requests
from datetime import datetime

stock_market_api_uri="https://www.alphavantage.co/query"

def get_list_of_stock_symbols_with_details(general_stock_name:str)->str:
    """
    Use this function to get a list of stock symbols with their name, type, region, currency.

    Args:
        general_stock_name (str): The general stock name that you want to get the stock symbols and other details for. (e.g. "Apple", "Google", "Reliance", "Tata Motors")
    
    Returns:
        str: Combined String of stock symbols with their name, type, region, currency.
    """
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": general_stock_name,
        "apikey": os.getenv("ALPHAVANTAGE_API_KEY")
    }
    
    response = requests.get(stock_market_api_uri, params=params)
    
    if response.status_code == 200:
        data = response.json()
        stock_details = []
        for item in data.get("bestMatches", []):
            stock_details.append(f"{item['1. symbol']} - {item['2. name']}, {item['3. type']}, {item['4. region']}, {item['8. currency']}")
        print(stock_details)
        return "\n".join(stock_details)
    else:
        return "Error fetching stock symbols"

def get_user_input()->str:
    """
    Use this function to get the user input.

    Returns:
        str: The user input
    """
    user_input = input("User: ")
    print(user_input)
    return user_input

def format_weekly_time_series_data(data:dict)->str:
    formatted_data=[]
    metadata=f"Below is the weekly time series data [(open, high, low, close) and Volumes] for the stock symbol {data['Meta Data']['2. Symbol']}.\n"
    formatted_data.append(metadata)

    for key, value in data['Weekly Time Series'].items():
        formatted_data.append(f"{key} - Open: {value['1. open']}, High: {value['2. high']}, Low: {value['3. low']}, Close: {value['4. close']}, Volume: {value['5. volume']}")
        if len(formatted_data)>21:
            break
    
    return "\n".join(formatted_data)

def get_weekly_time_series_data(stock_symbol:str)->str:
    """
    Use this function to get the weekly time series data for a stock symbol.

    Args:
        stock_symbol (str): The stock symbol for which the user want to get the weekly time series data. (e.g. "AAPL", "GOOGL", "RELIANCE", "TATAMOTORS")
    
    Returns:
        str: The weekly time series data for the stock symbol which contains Weekly prices open, high, low, close, and volume for each week with the date.
    """
    try:
        params = {
            "function": "TIME_SERIES_WEEKLY",
            "symbol": stock_symbol,
            "apikey": os.getenv("ALPHAVANTAGE_API_KEY")
        }
        
        response = requests.get(stock_market_api_uri, params=params)
        
        if response.status_code == 200:
            print("Data fetched successfully")
            data = response.json()
            import json
            with open('data.json', 'w') as f:
                f.write(json.dumps(data))
            formatted_data=format_weekly_time_series_data(data)
            print("Formatted data:", formatted_data)
            return formatted_data
        else:
            return "Error while fetching weekly time series data"
    except Exception as e:
        print(e)
        return "Error while fetching weekly time series data, currently services are not available, please inform the user"
    
def convert_utc_to_normal_date(utc_timestamp: str) -> str:
    """
    Convert a UTC timestamp to a normal date string in the format YYYYMMDDTHHMMSS.

    Args:
        utc_timestamp (str): The UTC timestamp to convert.

    Returns:
        str: The converted date string in the format YYYYMMDDTHHMMSS.
    """
    dt = datetime.strptime(utc_timestamp, "%Y%m%dT%H%M%S")
    return dt.strftime("%Y-%m-%d")


def format_news_data(data:dict, stock_symbol:str)->str:
    formatted_data=[]
    metadata=f"Below are the few news titles and summary of the news, published_date related to the {stock_symbol}:\n"
    formatted_data.append(metadata)

    for news in data['feed']:
        formatted_data.append(f"""Title: {news['title']}\n
                              Summary: {news['summary']}\n
                              Published Date: {convert_utc_to_normal_date(news['time_published'])}\n
                              {"###"*15}""")
        if len(formatted_data)>21:
            break

    return "\n".join(formatted_data)

def get_weekly_news_data_for_stock(stock_symbol:str)->str:
    """
    Use this function to get the weekly news data for a stock symbol.
    
    Args:
        stock_symbol (str): The stock symbol for which the user want to get the weekly news data. (e.g. "AAPL", "GOOGL", "RELIANCE", "TATAMOTORS")"
    Returns:
        str: The weekly news data for the stock symbol.
    """
    try:
        print("Fetching news data")
        params = {
            "function": "NEWS_SENTIMENT",
            "from_time": "20241001T0130",
            "to_time": "20251103T0130",
            "symbol": stock_symbol,
            "sort": "LATEST",
            "apikey": os.getenv("ALPHAVANTAGE_API_KEY")
        }
        
        response = requests.get(stock_market_api_uri, params=params)
        
        if response.status_code == 200:
            print("News Data fetched successfully")
            data = response.json()
            import json
            with open('news_data.json', 'w') as f:
                f.write(json.dumps(data))
            formatted_data=format_news_data(data, stock_symbol)
            print("Formatted data:", formatted_data)
            return formatted_data
        else:
            return "Error while fetching weekly news data"
    except Exception as e:
        print(e)
        raise e
        # return "Error while fetching weekly news data, currently services are not available, please inform the user"