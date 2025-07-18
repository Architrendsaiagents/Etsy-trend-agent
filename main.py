import os
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# Load secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_etsy_trends():
    response = requests.get("https://www.etsy.com/market/trending_items")
    soup = BeautifulSoup(response.text, 'html.parser')
    # You need to refine this logic based on actual HTML structure
    return ["Boho Earrings", "Personalized Mug", "Minimalist Decor"]

def compare_on_amazon(product_name):
    url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    return "Price Range: $15-$25 (sample)"

def analyze_with_openrouter(prompt):
    headers = {"Authorization": f"Bearer {os.getenv('OPENROUTER_KEY')}"}
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

def main():
    etsy_trends = get_etsy_trends()
    summary = f"🛍️ Top Etsy Trends for {datetime.now().strftime('%Y-%m-%d')}:\n\n"

    for product in etsy_trends:
        amazon_data = compare_on_amazon(product)
        summary += f"- {product}\n  {amazon_data}\n\n"

    ai_prompt = (
        f"Analyze the following trending Etsy products: {', '.join(etsy_trends)}.\n"
        "1. What are the trend tags to use?\n"
        "2. What should the seller expect this week and month?\n"
        "3. Give successful case studies and explain their strategy.\n"
    )

    ai_insight = analyze_with_openrouter(ai_prompt)

    final_message = summary + "\n" + ai_insight
    send_to_telegram(final_message)

if __name__ == "__main__":
    main()
