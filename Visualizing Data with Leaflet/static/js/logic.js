// Different tile layers for background map selection
// light map layer
var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/256/{z}/{x}/{y}?" +
  "access_token=pk.eyJ1Ijoiam9obm55eW9vIiwiYSI6ImNqd3hwNHV5dTA5bDk0YXBva3IzNnQ3bDUifQ.ikBBJZvD796WNWr1guATzQ");
// satellite street layer
var satellitemap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/tiles/256/{z}/{x}/{y}?" +
  "access_token=pk.eyJ1Ijoiam9obm55eW9vIiwiYSI6ImNqd3hwNHV5dTA5bDk0YXBva3IzNnQ3bDUifQ.ikBBJZvD796WNWr1guATzQ");
// outdoor layer
var outdoormap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/256/{z}/{x}/{y}?" +
  "access_token=pk.eyJ1Ijoiam9obm55eW9vIiwiYSI6ImNqd3hwNHV5dTA5bDk0YXBva3IzNnQ3bDUifQ.ikBBJZvD796WNWr1guATzQ");

// Creating our initial map object
// This gets inserted into the div with an id of 'mapid'
// We set the longitude and latitude to see the US (full screen/browser), the starting zoom level, and our array of layers
var map = L.map("map", {
  center: [48, -105],
  zoom: 3.5,
  layers: [lightmap, satellitemap, outdoormap]
});

// Use the addTo method to add intial object to our map
outdoormap.addTo(map);

// overlayers for tectonicplate and earthquake data
var tectonicplates = new L.LayerGroup();
var earthquakes = new L.LayerGroup();

// base layers
var baseMaps = {
  Grayscale: lightmap,
  Satellite: satellitemap,
  Outdoor: outdoormap
};

// tetonicplates and earthquake data overlays 
var overlayMaps = {
  "Fault Lines": tectonicplates,
  "Earthquakes": earthquakes
};

// control tile layer selection
L
  .control
  .layers(baseMaps, overlayMaps)
  .addTo(map);

//  get earthquake GeoJSON data
d3.json("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson", function(data) {
  function getStyle(feature) {
    return {
      opacity: 1,
      fillOpacity: 1,
      fillColor: getColor(feature.properties.mag),
      radius: getRadius(feature.properties.mag),
      weight: 0.5
    };
  }

  // Color scheme of earthquakes determined by magnitude
  function getColor(magnitude) {
    switch (true) {
      case magnitude > 5:
        return "#ae00ff";
      case magnitude > 4:
        return "#ff0a0a";
      case magnitude > 3:
        return "#fffb00";
      case magnitude > 2:
        return "#00ff04";
      case magnitude > 1:
        return "#00ffea";
      default:
        return "#0059ff";
    }
  }

  // Radius of the earthquake marker determined by magnitude
  function getRadius(magnitude) {
    if (magnitude === 0) {
      return 1;
    }
    return magnitude * 2.5;
  }

  // Earthquake GeoJSON layer with pointer "click on" data function
  L.geoJson(data, {
    pointToLayer: function(feature, latlng) {
      return L.circleMarker(latlng);
    },
    style: getStyle,
    onEachFeature: function(feature, layer) {
      layer.bindPopup("Magnitude: " + feature.properties.mag + "<br>Location: " + feature.properties.place);
    }
  }).addTo(earthquakes);

  earthquakes.addTo(map);

// Render earthquake legend 
  var legend = L.control({
    position: "bottomright"
  });

  legend.onAdd = function() {
    var div = L
      .DomUtil
      .create("div", "info legend");
    var grades = [0, 1, 2, 3, 4, 5];
    var colors = ["#0059ff", "#00ffea", "#00ff04", "#fffb00", "#ff0a0a", "#ae00ff"];

    for (var i = 0; i < grades.length; i++) {
      div.innerHTML += "<i style='background: " + colors[i] + "'></i> " +
        grades[i] + (grades[i + 1] ? "&ndash;" + grades[i + 1] + "<br>" : "+");
    }
    return div;
  };

  legend.addTo(map);

//  get and add tectonic plates GeoJSON data layer
  d3.json("https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json",
    function(platedata) {
      L.geoJson(platedata, {
        color: "white",
        weight: 3
      })
      .addTo(tectonicplates);
      tectonicplates.addTo(map);
    });
});
