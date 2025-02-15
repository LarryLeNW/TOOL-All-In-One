from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup

def fetch_vnexpress_search_results(query):
    url = f"https://timkiem.vnexpress.net/?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    article = soup.select_one(".title-news a") 
    if article:
        title = article.get_text(strip=True)
        link = article['href']
        summary = ""
        
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        summary_element = article_soup.select_one(".description")
        if summary_element:
            summary = summary_element.get_text(strip=True)
        
        return (title, summary)
    return None

def add_and_search_notes():
    queries = ["lập trình", "khoa học", "trí tuệ nhân tạo", "robot", "blockchain", "y học", "môi trường", "năng lượng", "toán học", "thiên văn"] 
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://material.playwrightvn.com/04-xpath-personal-notes.html")
        
        for query in queries:
            article = fetch_vnexpress_search_results(query)
            if article:
                title, summary = article
                page.fill("#note-title", title)
                page.fill("#note-content", summary)
                page.click("button#add-note")
                print(f"Added note for query: {query}")
        
        print("10 notes added successfully!")
        
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.screenshot(path="done-ls4.png")
        print("Screenshot taken successfully!")
        
        input("Press Enter to close the browser...")

if __name__ == "__main__":
    add_and_search_notes()
