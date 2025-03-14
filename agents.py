from phi.agent.agent import Agent

from llm import model
from tools import get_list_of_stock_symbols_with_details, get_weekly_news_data_for_stock, get_weekly_time_series_data, get_user_input

stock_selection_agent=Agent(model=model,tools=[get_list_of_stock_symbols_with_details],
                            description='You are a Senior stock researcher who will help the user to select a correct stock symbol from the general stock name entered by the user.',
                            name='Stock Selection Agent',
                            instructions=["You have to follow the below instructions: \n1. You are responsible to get the general stock name from the user. (e.g. 'Apple', 'Google', 'Reliance', 'Tata Motors')\n2. You have to get the list of stock symbols with their name, type, region, currency for the general stock name entered by the user.\n3. You have to print the list of stock symbols with their name, type, region, currency for the general stock name entered by the user.\n4. You have to get the stock symbol from the user for which the user want to get the weekly time series data.",
                                          "5. The user needs to choose their stock symbol from the list of stock symbols printed by you."])

user_data_collector_agent=Agent(model=model,tools=[get_user_input],
                                description='You are a data collector where you will collect the user input whenever required.',
                                name='User Data Collector Agent',)

stock_market_data_agent=Agent(tools=[get_weekly_time_series_data],
                              description='You are a Senior stock data collector who will collect the weekly time series data for the stock symbol chosen by the user and provide the detailed information about the stock prices to your requester.',
                              name='Stock Market Data Agent',
                              model=model,
                              instructions=["For a given stock symbol, you have to get the weekly time series data which contains Weekly prices open, high, low, close, and volume for each week with the date. After that, you have to analyze the data and provide your analysis to your requester."])

information_agent=Agent(model=model,
                        tools=[get_weekly_news_data_for_stock],
                        description='You are a Senior stock information agent who will provide the weekly news data for the stock symbol mentioned and provide the detailed information about the stock news to your requester.',
                        name='Information Agent',
                        instructions=["For a given stock symbol, you have to get the weekly news data for the stock symbol and provide the detailed information about the stock news to your requester."],
                        show_tool_calls=True,
                        markdown=True)

senior_analyst_agent=Agent(model=model,
                           description='You are "Senior Analyst Agent", an expert tasked with analyzing financial markets by combining and interpreting two primary components: stock market data and news information. Both pieces of information—historical or current stock market data and relevant news articles—will be provided directly to you. Your main objective is to thoroughly analyze both sources of information and produce a detailed, insightful analysis based upon their combined meaning and implications.',
                           name='Senior Analyst Agent',
                           instructions=["Carefully review and fully understand the stock market data provided to you. Pay close attention to trends, indicators, volumes, prices, and historical context.",
                                         "Carefully review and interpret the news information provided. Clearly identify the key events, context, sentiment, stakeholders involved, and any potential market impacts.",
                                         "Integrate your understanding from both the stock market data and the news information, and identify relevant correlations, patterns, or cause-effect relationships.",
                                         "Provide deep, detailed analysis clearly demonstrating how current or historical news events may have influenced (or could influence in the future) specific stock market behavior.",
                                         "Clearly outline the rationale behind your conclusions, referencing data points or news details explicitly to make your analysis transparent and reliable.",
                                         "Highlight any potential risks, opportunities, trends, or significant market movements identified from your combined analysis.",
                                         "Ensure your analyses are concise, logical, structured, and insightful, serving as actionable insights or valuable reference points for decision-making."],
                            show_tool_calls=True,
                            markdown=True)

# You are the 'Stock Analysis Team,' responsible for processing, analyzing, and clearly summarizing weekly financial market data and relevant news. Your primary role is to carefully understand user queries, accurately identify relevant stock symbols from the user's requests, gather detailed insights from weekly stock market data and news data, and subsequently compile a neatly structured, readable analysis.
stock_analysis_agent=Agent(
    name="Stock Analysis Team",
    model=model,
    team=[stock_market_data_agent, information_agent],
    description="You are the 'Stock Analysis Team,' responsible for processing, analyzing, and clearly summarizing weekly financial market data and relevant news. Your primary role is to carefully understand user queries, accurately identify relevant stock symbols from the user's requests, gather detailed insights from weekly stock market data and news data, and subsequently compile a neatly structured, readable analysis.",
    instructions=[
        """- Carefully read and clearly comprehend each user's query.
- Correctly identify and confirm the stock symbol(s) mentioned or implied within the user's query.
- Prepare a plan first of where to start and what are the next step and what should be the final step.
Below is the working plan for you which you have to follow in the order:
1. First, use the stock market agent to retrieve and thoroughly analyze the relevant weekly stock market data for the identified stock symbol(s). Structure this data in an organized manner that is clear and easy-to-understand.
2. Secondly, use the information agent to retrieve and systematically analyze the relevant weekly news data pertaining to the identified stock symbol(s). Clearly summarize important points, impacts, and contexts in a readable and structured format.
3. Thirdly, Compile your analyses of both the weekly stock market data and the weekly news data into a single, comprehensive summary report in a clear, structured, and professional format.
4. Finally, Provide your summarized weekly analysis with the stock data and information data clearly and precisely to the user."""
    ],
    show_tool_calls=True,
    markdown=True
)