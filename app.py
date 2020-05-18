from flask import render_template, Flask, jsonify, redirect, request, url_for
import bs
import bs2

app = Flask(__name__)
results = []


@app.route("/", methods=["GET", "POST"])
def load_app():
	global results
	if request.method == "GET":
		return render_template("index.html")
	else:
		query = request.form["query"]
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
	global results
	data = request.json
	songs = data["songs"]
	instruments = ["Guitar", "Piano"]
	print(songs)
	for song in songs:
		print(results[song])
	# download songs. we have the download links stored in results global variable
	# only download if not already downloaded!
	# extract instruments from new downloaded as well as already downloaded
	# return in this function
	return jsonify({"instruments": instruments})


@app.route("/process", methods=["POST"])
def process():
	data = request.form  # this will be the songs selected and the instruments selected
	songs = [int(i) for i in data["songs"].split(",")]
	instruments = data["instruments"].split(",")
	print(songs)
	print(instruments)
	# do some tings with it, render with results. play song or give them the file basically
	return render_template("process.html")


def main():
	app.run(debug=True)


if __name__ == "__main__":
	main()
