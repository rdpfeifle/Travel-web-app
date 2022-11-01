"use strict";

function initMap() {
  const newYorkCoords = {
    lat: 40.73061,
    lng: -73.935242,
  };

  const basicMap = new google.maps.Map(document.querySelector("#map"), {
    center: newYorkCoords,
    zoom: 11,
  });

  const nyMarker = new google.maps.Marker({
    position: newYorkCoords,
    title: "New York City",
    map: basicMap,
  });

  const nyInfo = new google.maps.InfoWindow({
    content: "<h1>New York City!</h1>",
  });

  nyInfo.open(basicMap, nyMarker);
}
