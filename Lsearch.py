from googlesearch import search
import requests
from bs4 import BeautifulSoup

def search_google(query):
    links = []
    content = ""
    for link in search(query, num_results=5):
        text = extract_text(link)
        content = content + text
        links.append(link)
    return links, content

def extract_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text 
        soup = BeautifulSoup(html, 'html.parser') 
        paragraphs = soup.find_all('p')
        text = ' . '.join([para.get_text(strip=True) for para in paragraphs])
        return text
    else:
        return ""