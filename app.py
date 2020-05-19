from flask import render_template, Flask, jsonify, redirect, request, url_for
import bs
import bs2
import os
import glob
from construction import get_songs_msgs, get_instruments
from probabilities import get_channels_dict

app = Flask(__name__)

"""
current issues:

when you click update, it re-renders every checkbox, hence clearing all selected checkboxes. also different order potentially
we are redownloading files we already have since i took a simplistic approach of clearing the folder then just downloading all of the songs that are currently selected
we allow duplicate songs (server side and client side). do we? wont it just replace itself in the dict
the code relies on the name of the song being different
"""


@app.route("/", methods=["GET", "POST"])
def load_app():
	if request.method == "GET":
		return render_template("index.html")
	else:  # they click search
		query = request.form["query"]  # get search term
		result1 = bs.main(query)
		result2 = bs2.main(query)
		if result1 and not result2:
			results = result1
		elif result2 and not result1:
			results = result2
		elif result1 and result2:
			results = result1 + result2
		else:
			return render_template("index.html")
		search_results = {}
		for i in range(len(results) - 1):
			search_results[i] = results[i]
		amount = len(search_results)
	return render_template("index.html", search_results=search_results, amount=amount)


@app.route("/search", methods=["POST"])
def search():
	results = []
	query = request.json["query"]  # get search term
	result1 = bs.main(query)
	result2 = bs2.main(query)
	if result1 and not result2:
		results = result1
	elif result2 and not result1:
		results = result2
	elif result1 and result2:
		results = result1 + result2
	search_results = {}
	for i in range(len(results) - 1):
		search_results[i] = results[i]
	amount = len(search_results)
	return jsonify({"results": results, "amount": amount})


@app.route("/retrieve_instruments", methods=["POST"])
def retrieve_instruments():
	selected_songs = request.json["selected_songs"]  # get search term
	files = glob.glob("songs/*")
	for f in files:
		os.remove(f)  # clear songs directory
	all_mid = []
	for song in selected_songs:
		url = song["url"]
		name = song["name"]
		all_mid.append("songs/" + name + ".mid")
		bs.save_midi(url, name)
	all_msgs = get_songs_msgs(all_mid)
	instruments = get_instruments(all_msgs)
	return jsonify({"instruments": instruments})


@app.route("/play", methods=["POST"])
def process():
	data = request.json
	selected_songs = data["selected_songs"]
	instruments = data["instruments"]
	# do some tings with it, render with results. play song or give them the file basically
	return jsonify({"success": True})


@app.route("/save", methods=["POST"])
def save():
	data = request.json
	songs = data["selected_songs"]
	instruments = data["instruments"]
	return jsonify({"success": True})


def main():
	app.run(debug=True)


if __name__ == "__main__":
	main()
