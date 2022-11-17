"use strict";

let map, infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 39.9682687, lng: -104.9973142 }, //lat: -34.397, lng: 150.644
    zoom: 6,
  });
  infoWindow = new google.maps.InfoWindow();

  const locationButton = document.createElement("button");

  locationButton.textContent = "Click here to see your Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
  locationButton.addEventListener("click", () => {
    // Try HTML geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };

          infoWindow.setPosition(pos);
          infoWindow.setContent("Here is your current location.");
          infoWindow.open(map);
          map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        }
      );
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );

  infoWindow.open(map);
}

window.initMap = initMap;

///////////////////////////////////// separate
// this was here before
// function initMap() {
//   const newYorkCoords = {
//     lat: 40.73061,
//     lng: -73.935242,
//   };

//   const basicMap = new google.maps.Map(document.querySelector("#map"), {
//     center: newYorkCoords,
//     zoom: 11,
//   });

//   const nyMarker = new google.maps.Marker({
//     position: newYorkCoords,
//     title: "New York City",
//     map: basicMap,
//   });

//   const nyInfo = new google.maps.InfoWindow({
//     content: "<h1>New York City!</h1>",
//   });

//   nyInfo.open(basicMap, nyMarker);
// }

// // autocomplete search bar

// let autocomplete;
// function initAutocomplete() {
//   autocomplete = new google.maps.places.Autocomplete(
//     document.getElementById("autocompleteSearchInput"),
//     {
//       types: ["establishment"],
//       componentRestrictions: { country: ["USA"] },
//       fields: ["place_id", "geometry", "name"],
//     }
//   );
//   autocomplete.addEventListener("place_changed", onPlaceChanged);
// }
// function onPlaceChanged() {
//   let place = autocomplete.getPlace();

//   if (!place.geometry) {
//     // user didn't select a prediction
//     document.getElementById("autocompleteSearchInput").placeholder =
//       "Enter a place";
//   } else {
//     // Display details about the valid place
//     document.getElementById("details").innerHTML = place.name;
//   }
// }
