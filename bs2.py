from bs4 import BeautifulSoup
import requests
import json
import time


def scrape_results(search_query):
    html = requests.get(f"https://bitmidi.com/search/?q={search_query}").text
    json_data = get_json(html)
    page_total = json_data["views"]["search"][search_query]["pageTotal"]
    midi_with_names = get_midi_from_json(json_data)
    for i in range(1, page_total):
        html = requests.get(f"https://bitmidi.com/search/?q={search_query}&page={i}").text
        json_data = get_json(html)
        midi_with_names += get_midi_from_json(json_data)
    return midi_with_names


def get_midi_from_json(json_data):
    all_midis = json_data["data"]["midis"]
    midi_with_names = [[all_midis[key]["id"], all_midis[key]["name"]] for key in all_midis]
    return midi_with_names


def get_json(html):
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find("script").text.replace("\n", "").split("console.time('render')window.initStore =")[1]
    json_data = json.loads(data)
    return json_data


def save_midi(id, name):
    song = requests.get(f"https://bitmidi.com/uploads/{id}.mid")
    open(f"{name}.mid", "wb").write(song.content)


def main():
    search = input("what search_query")
    start = time.time()
    lst = scrape_results(search)
    print(lst)
    # for item in lst:
       # save_midi(item[0], item[1])
    end = time.time()
    print(end-start)


if __name__ == '__main__':
    main()

#     if you want to speed that up it's not that hard just get the number of pages for the search query
#     with json_data["views"]["search"]["mozart"]["pageTotal"] then only run it that number of times
#     where Mozart is your search query

