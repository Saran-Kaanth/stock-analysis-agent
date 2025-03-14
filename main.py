import os

from dotenv import load_dotenv

load_dotenv(override=True)

os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

from agents import stock_analysis_agent

if __name__=='__main__':
    print("Welcome to Stocklysis! Currently, we are providing the analysis of the stock market data and news information. Please enter your query on which stock you want to get the analysis.")
    user_input=input("Please enter your query:")
    stock_analysis_agent.print_response(user_input, stream=True)