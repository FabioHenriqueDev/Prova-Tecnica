import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


link = 'https://spmmedicare.com/'


def scraping_site(link: str) -> str:
    requisicao = requests.get(link)
    site = BeautifulSoup(requisicao.text, 'html.parser')

    for tag in site(['script', 'style', 'nav', 'footer']):
        tag.decompose()

    return md(str(site), heading_style="ATX")

    

if __name__ == '__main__':
    print(scraping_site(link))