import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

link = 'https://spmmedicare.com'

def scraping_site(link: str) -> str:
    requisicao = requests.get(link)
    site = BeautifulSoup(requisicao.text, 'html.parser')

    for tag in site(['script', 'style']):
        tag.decompose()

    with open("site.md", 'w', encoding="utf-8") as a:
        a.write(md(str(site), heading_style="ATX"))

    return md(str(site), heading_style="ATX")

    
if __name__ == '__main__':
    scraping_site(link)