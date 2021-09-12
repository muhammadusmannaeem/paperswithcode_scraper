import requests
from bs4 import BeautifulSoup

response = requests.get('https://paperswithcode.com')

if response.status_code != 200:
    print("Not Scraped...", response.status_code)
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

mydivs = soup.find_all("div", {"class": "row infinite-item item"})
for div in mydivs:
    # Get title
    title = div.find_all('h1')[0].text

    # Get Github Url
    for url in div.find_all('a', href=True):
        if url['href'].startswith("https://github.com"):
            github_url = url['href']
            break

    # Get Description
    for d in div.find_all("p", {"class": "item-strip-abstract"}):
        description = d.text
        break

    # Get Date
    for d in div.find_all("span", {"class": "author-name-text item-date-pub"}):
        date = d.text
        break

    # Get PDF link
    for d in div.find_all("div", {"class": "entity"}):
        pdf_response = requests.get("https://paperswithcode.com" + d.find_all('a', href=True)[0]['href'])
        soup = BeautifulSoup(pdf_response.content, 'html.parser')
        url_tags = soup.find_all("div", {"class": "paper-abstract"})[0]
        for url in url_tags.find_all('a', href=True):
            if url['href'].endswith(".pdf"):
                pdf_url = url['href']
                break

