from bs4 import BeautifulSoup
import requests
import json
import time

def scrape_results(search_query):
    html = requests.get(f"https://bitmidi.com/search/?q={search_query}").text
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find_all("script")[0].text.replace("\n", "").split("console.time('render')window.initStore =")[1]
    json_data = json.loads(data)
    all_midis = json_data["data"]["midis"]
    midi_with_names = [[all_midis[key]["id"], all_midis[key]["name"]] for key in all_midis]
    return midi_with_names


def save_midi(id, name):
    song = requests.get(f"https://bitmidi.com/uploads/{id}.mid")
    open(f"{name}.mid", "wb").write(song.content)


def main():
    start = time.time()
    search = input("what search_query")
    lst = scrape_results(search)
    for item in lst:
        save_midi(item[0], item[1])
    end = time.time()
    print(end-start)


if __name__ == '__main__':
    main()

