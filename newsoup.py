import requests
from bs4 import BeautifulSoup
import schedule
import time
import asyncio
from telegram import Bot

# Api Key Of Telegram Bot
TOKEN = "YOUR_SECRET_KEY"
CHAT_ID = "YOUR_CHAT_ID"


bot = Bot(token=TOKEN)

# ✅ Async function to fetch news and send message
async def send_news():
    print("Fetching news...") 
    
    url = "https://www.thehindu.com/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch news. Status Code: {response.status_code}")  
        return
    
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = soup.find_all(["h3", "h2"], class_=["title"])

    if not headlines:
        print("No headlines found!") 
        return
    
    news_list = []
    for id, headline in enumerate(headlines[:10], 1): 
        text = headline.get_text().strip()
        link = headline.find("a")["href"] if headline.find("a") else "No link available"
        news_list.append(f"{id}. {text} - {link}")

    news_text = "\n\n".join(news_list)
    
    print("Sending news to Telegram...") 
    try:
        await bot.send_message(chat_id=CHAT_ID, text=f" *Today's News* \n\n{news_text}", parse_mode="Markdown")
        print("News sent successfully!") 
    except Exception as e:
        print(f"Error sending message: {e}")

# Wrapper function to run async function in schedule
def job():
    print("Running scheduled job...") 
    asyncio.run(send_news())  # Runs the async function properly

schedule.every().day.at("10:00").do(job)

print("Script started. Waiting for scheduled tasks...") 
while True:
    schedule.run_pending()
    time.sleep(10)  # Check every second
