from flask import render_template, Flask, jsonify, redirect, request, url_for
import bs
import bs2
import os
import glob

app = Flask(__name__)
results = []


@app.route("/", methods=["GET", "POST"])
def load_app():
	global results
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


@app.route("/retrieve_instruments", methods=["POST"])
def retrieve_instruments():
	# we currently use "Guitar" etc. best to use the ID or whatever instead? need a dict somewhere anyway to convert
	global results
	data = request.json
	songs = data["songs"]
	instruments = ["Guitar", "Piano"]  # hardcoded for now
	files = glob.glob("songs/*")
	for f in files:
		os.remove(f)  # clear songs directory
	for song in songs:
		url = results[song]["url"]
		name = results[song]["name"]
		bs.save_midi(url, name)
		# pass to regulate tracks
		# pass input messages to probabilities.py
		# parse response and add to instruments list
	return jsonify({"instruments": instruments})


@app.route("/play", methods=["POST"])
def process():
	data = request.form  # this will be the songs selected and the instruments selected
	songs = [int(i) for i in data["songs"].split(",")]
	instruments = data["instruments"].split(",")
	print(songs)
	print(instruments)
	# do some tings with it, render with results. play song or give them the file basically
	# process.html probably useless then
	return render_template("process.html")


def main():
	app.run(debug=True)


if __name__ == "__main__":
	main()
