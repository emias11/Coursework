from bs4 import BeautifulSoup
import requests


def scrape_results(search_query):
    html = requests.get(f"https://www.midiworld.com/search/?q={search_query}").text
    soup = BeautifulSoup(html, "html.parser")
    error = soup.find("div", {"id": "page"}).text
    if "found nothing!" in error:
        return None
    unordered_lists = soup.find_all("ul")[1]
    lists = unordered_lists.find_all("li")
    results = [{"name": lst.text.replace("\n", "").split(" - download")[0], "url": lst.find("a")["href"]} for lst in lists]
    return results


def save_midi(url, name):
    song = requests.get(url)
    statuscode = song.status_code
    if statuscode == 200:
        open(f"songs/{name}.mid", "wb").write(song.content)
        return True # changed from name
    else:
        return False


def main(query):
    results = scrape_results(query)
    return results


if __name__ == '__main__':
    main("")
