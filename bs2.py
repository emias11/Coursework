from bs4 import BeautifulSoup
import requests
import json


def scrape_results(search_query):
    html = requests.get(f"https://bitmidi.com/search/?q={search_query}").text
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find_all("script")[0].text.replace("\n", "").split("console.time('render')window.initStore =")[1]
    json_data = json.loads(data)
    all_midis = json_data["data"]["midis"]
    midi_with_names = []
    for key in all_midis:
        sub = all_midis[key]
        midi_with_names.append([sub["id"], sub["name"]])
    return midi_with_names


def save_midi(id, name):
    song = requests.get(f"https://bitmidi.com/uploads/{id}.mid")
    open(f"{name}.mid", "wb").write(song.content)


def main():
    search = input("what search_query")
    lst = scrape_results(search)
    for item in lst:
        save_midi(item[0], item[1])


if __name__ == '__main__':
    main()

