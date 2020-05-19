function send_post(url, dict, callback) {
	var http = new XMLHttpRequest();
	var params = JSON.stringify(dict);
	http.open("POST", url, true);
	http.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	http.onreadystatechange = function() {
		if(http.readyState == 4 && http.status == 200) {
			response = JSON.parse(http.responseText);
			if (typeof callback === "function") callback(response);
		}
	}
	http.send(params);
}
/*
send_post("/test", {"hi": "hello"}, function(response) {
		console.log(response);
});
*/

var allSelectedSongs = [];
var allSelectedInstruments = [];
var results = [];
var amount = 0;

function removeSelected() {
	// removes songs from selected list when you press X
	this.parentElement.remove();
	var parentValue = parseInt(this.parentElement.getAttribute("data-id"));
	allSelectedSongs.splice(allSelectedSongs.indexOf(parentValue), 1);
}

function updateRemoveListeners() {
	// add listeners (checks for being clicked, runs function) to X buttons
	var selectedSongButtons = document.getElementsByClassName('remove-item');
	Array.from(selectedSongButtons).forEach(function(element){
		element.addEventListener("click", removeSelected);
	});
}

function addSelected(){
	// adds songs to selected list when you press X
	var parentSongName = this.parentElement.textContent.replace("+", "");
	var parentValue = parseInt(this.parentElement.getAttribute("data-id"));
	var selectedSongs = document.getElementById("selected-songs");
	selectedSongs.innerHTML += `<div class="song-item selected-song-item" data-id=${parentValue}><p>${parentSongName}</p><button type="button" class="remove-item">&#x2715;</button></div> <!-- .song-item -->`
	updateRemoveListeners();
	allSelectedSongs.push(parentValue);
}

function updateAddListeners() {
	// add listeners (checks for being clicked, runs function) to + buttons
	var searchResultsButtons = document.getElementsByClassName('add-item');
	Array.from(searchResultsButtons).forEach(function(element){
		element.addEventListener("click", addSelected); // run function updateActive when any song is clicked
	});
}

function search() {
	search_query = document.getElementById("search-box").value;
	song_wrapper = document.getElementById("song-item-wrapper");
	song_wrapper.innerHTML = "";
	send_post("/search", {"query": search_query}, function(response) {
		amount = response["amount"];
		results = response["results"];
		for (var i=0; i < amount; i++) {
			song_wrapper.innerHTML += `<div data-id=${i} class="song-item search-song-item"><p>${results[i]["name"]}</p><button type="button" class="add-item">+</button></div> <!-- .song-item -->`;
		}
		updateAddListeners();
	});
}


function renderCheckboxes(instruments){
	var checkboxWrappers = document.getElementsByClassName('select-wrapper'); // find checkbox wrappers
	for (var i=checkboxWrappers.length -1;i>=0;i--) { // remove all current checkboxes
		checkboxWrappers[i].remove();
	}
	var form = document.getElementById("form");
	for (var i=0; i < instruments.length; i++) {  // add a checkbox for each new instrument
		instrument = instruments[i];
		form.innerHTML += `<div class="select-wrapper"><input class="instrument-checkbox" type="checkbox" name="instrument${i+1}" value="${instrument}"></input><label for="instrument${i+1}">${instrument}</label></div>`;
	}
	updateCheckboxListeners();
}


function updateInstruments() {
	/*
	update instrument list in form (hidden input)
	*/
	currentInstrument = this.value;
	if (allSelectedInstruments.includes(currentInstrument)) {
		allSelectedInstruments.splice(allSelectedInstruments.indexOf(currentInstrument), 1);
	}
	else {
		allSelectedInstruments.push(currentInstrument);
	}
	console.log(allSelectedInstruments);
}

function updateCheckboxListeners() {
	// add listeners (checks for being clicked, runs function) to checkboxes
	var checkboxes = document.getElementsByClassName('instrument-checkbox');
	Array.from(checkboxes).forEach(function(element){
		element.addEventListener("click", updateInstruments)
	});
}

function retrieve_instruments() {
	selectedSongs = [];
	for (var i=0; i<allSelectedSongs.length; i++) {
		selectedSongs.push(results[allSelectedSongs[i]]);
	}
	send_post("/retrieve_instruments", {"selected_songs": selectedSongs}, function(response) {
		instruments = response["instruments"];
		renderCheckboxes(instruments);
	})
}

function savex() {
	selectedSongs = [];
	for (var i=0; i<allSelectedSongs.length; i++) {
		selectedSongs.push(results[allSelectedSongs[i]["name"]]);
	}
	send_post("/save", {"selected_songs": selectedSongs, "instruments": allSelectedInstruments}, function(response) {
		status = response["success"];
	})
}

function playx() {
	selectedSongs = [];
	for (var i=0; i<allSelectedSongs.length; i++) {
		selectedSongs.push(results[allSelectedSongs[i]]["name"]);
	}
	send_post("/play", {"selected_songs": selectedSongs, "instruments": allSelectedInstruments}, function(response) {
		status = response["success"];
	})
}
