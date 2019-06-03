// from data.js
var tableData = data;

// YOUR CODE HERE!
// Reference the tbody, user input by user and buttons
var $tbody = d3.select("tbody");
var $dateInput = d3.select("#date");
var $searchBtn = d3.select("#search");
var $resetBtn = d3.select("#reset");

// Event listener for search and reset buttons
$searchBtn.addEventListener("click", handleSearchButtonClick);
$resetBtn.addEventListener("click", handleResetButtonClick);

// Render the table from data.js
function renderTable() {
  $tbody.innerHTML = "";
  for (var i = 0; i < tableData.length; i++) {
    var sighting = tableData[i];
    var fields = Object.keys(sighting);
    var $row = $tbody.insertRow(i);
    for (var j = 0; j < fields.length; j++) {
      var field = fields[j];
      var $cell = $row.insertCell(j);
      $cell.innerText = sighting[field];
    }
  }
}

// Filter data using the user input date/time
function handleSearchButtonClick() {
  var filterDate = $dateInput.value;
  if (filterDate != "") {
    tableData = data.filter(function (sighting) {
      var sightingDate = sighting.datetime;
      return sightingDate === filterDate;
    });
  };
  renderTable();
};


// Reset data and search input
function handleResetButtonClick() {
  tableData = data;
  $dateInput.value = "";
  renderTable();
}

// Render the initial table
renderTable();