import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# -----------------------------------STOCKS-------------------------------------

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "9MN1CVHZDO3TLHL6"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "5ff5eba6eb1b47a79e5c57121c883f6c"

parameters_stock = {
    'apikey': STOCK_API_KEY,
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK,
    'interval': "60min",
}
response = requests.get(STOCK_ENDPOINT, params=parameters_stock)
print(response.status_code)
data = response.json()['Time Series (Daily)']
# Take the data
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_price_close = yesterday_data['4. close']
# Before
day_before_yesterday_data = data_list[1]
day_before_yesterday_price_close = day_before_yesterday_data['4. close']


# Difference price
difference = (float(yesterday_price_close) - float(day_before_yesterday_price_close))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

differ_perc = round((difference / float(yesterday_price_close)) * 100)
print(differ_perc)
if abs(differ_perc) > 1:
    # -----------------------------------NEWS-------------------------------------
    parameters_new = {
        'apiKey': NEWS_API_KEY,
        'qInTitle': COMPANY_NAME,
    }
    response_news = requests.get(NEWS_ENDPOINT, params=parameters_new)
    print(response_news.status_code)

    data_news = response_news.json()['articles']
    three_articles = data_news[:3]


    formatted = [f"{STOCK}: {up_down} {differ_perc}\nHeadlines: {articles['title']}.\nBrief: {articles['description']}" for articles  in three_articles]

    # Sending the message

    account_sid = "AC76409dca322f0fcb5a78dcd53495c914"
    auth_token = "f950fa814171cc3d0cdf2b2dc0c73688"

    client = Client(account_sid, auth_token)
    for articles_ in formatted:
        message = client.messages.create(
            body=articles_,
            from_="+14245436338",
            to="+5561994628894",
        )
        print(message.status)

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
# HINT 2: Work out the value of 5% of yerstday's closing stock price.


## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
# HINT 1: Think about using the Python Slice Operator


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
# HINT 1: Consider using a List Comprehension.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
