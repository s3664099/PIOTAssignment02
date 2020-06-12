var map;

function initMap() { //start initMap
  
    var request = new XMLHttpRequest();
  
  // DeviceIP goes here if running app on separate device
  // e.g. var url = "http://192.168.0.1:5000/cars"
  // If running on locally, leave unchanged
  var url = "http://localhost:5000/findallocatedcars/"+session['email']
 
  
  var carsArray = [];
  request.open('GET', url);
  request.onload = function() {
    carsArray = JSON.parse(request.responseText);

    for (var i = 0; i < carsArray.length; i++) {

      // Create a string for every object in the array which will be used populate the infoWindow for each car
      var carDetails = '<div id="content" style="width:400px; background-color:white;">' +
            "Colour: " + carsArray[i].colour.substring(0, 1).toUpperCase() + carsArray[i].colour.slice(1) + '</br>' +
            "Latitude: " + carsArray[i].locationlat + '</br>' +
            "Longitude: " + carsArray[i].locationlong + '</br>' +
            "Make: " + carsArray[i].make + '</br>' +
            "Model: " + carsArray[i].model + '</br>' +
            "Registration: " + carsArray[i].rego + '</br>' +
              '</div>';

      addMarker({
        coords:{lat:carsArray[i].locationlat, lng:carsArray[i].locationlong}, 
        content:carDetails});
      }


  };
request.send();



//Map options
var options = {
  zoom:13,
  center: {lat:-37.8136,lng:144.9631}
}

// Initialising new map
map = new google.maps.Map(document.getElementById('map'), options);

// Variable to store whether an infoWindow is open
var activeInfoWindow;

// Create marker object and add to map
function addMarker(props) {
  var marker = new google.maps.Marker({
    position:props.coords,
    map:map,
    icon:'https://img.icons8.com/android/24/000000/car.png',
    content:props.content
  });
  
  // If valid data is supplied then create an infoWindow object
  if(props.content) {
    var infoWindow = new google.maps.InfoWindow({
      content:props.content
    });

    // Add a listener to the marker to open the infoWindow when clicked
    marker.addListener('click', function() {
      infoWindow.open(map, marker);
    });

    // Add a listener to the marker to close if a separate infoWindow is active
    // This will ensure that only one infoWindow is open at a time
    marker.addListener('click', function() {
      if (activeInfoWindow) { 
        activeInfoWindow.close();
      }
        infoWindow.open(map, marker);
        activeInfoWindow = infoWindow;
    });

    // Add a listener to the map to close all infoWindows when clicked
    map.addListener("click", function(event) {
    infoWindow.close();
    });

  }

}

} //end initMap
