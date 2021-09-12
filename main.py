import requests
from bs4 import BeautifulSoup


def get_data():
    response = requests.get('https://paperswithcode.com')
    if response.status_code != 200:
        print("Not Scraped...", response.status_code)
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    mydivs = soup.find_all("div", {"class": "row infinite-item item"})

    DATA = []

    for div in mydivs:

        # Get title
        title = div.find_all('h1')[0].text

        # Get Github Url
        github_url = ""
        for url in div.find_all('a', href=True):
            if url['href'].startswith("https://github.com"):
                github_url = url['href']
                break

        # Get Description
        description = ""
        for d in div.find_all("p", {"class": "item-strip-abstract"}):
            description = d.text
            break

        # Get Date
        date = ""
        for d in div.find_all("span", {"class": "author-name-text item-date-pub"}):
            date = d.text
            break

        # Get Category
        category = ""
        for d in div.find_all("div", {"class": "sota"}):
            temp = d.text.replace("\n", " ")
            category = category.join(temp.split("  "))

        # Get PDF link
        pdf_url = ""
        for d in div.find_all("div", {"class": "entity"}):
            pdf_response = requests.get("https://paperswithcode.com" + d.find_all('a', href=True)[0]['href'])
            soup_2 = BeautifulSoup(pdf_response.content, 'html.parser')
            url_tags = soup_2.find_all("div", {"class": "paper-abstract"})[0]
            for url in url_tags.find_all('a', href=True):
                if url['href'].endswith(".pdf"):
                    pdf_url = url['href']
                    break
        DATA.append({"title": title, "github_url": github_url, "description": description, "date": date,
                     "category": category, "pdf_url": pdf_url})
    return DATA


data = get_data()

print(len(data))

for d in data:
    print(d)
