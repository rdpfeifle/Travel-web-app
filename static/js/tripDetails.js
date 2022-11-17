// -------- trip details page -------- //

// document.querySelector("#save-activity").addEventListener("submit", (evt) => {
//   evt.preventDefault();

//   const addActivity = () => {
//     const activityInputs = {
//       trip_id: document.querySelector("#trip_id").value,
//       activity_name: document.querySelector("#activity-name").value,
//       activity_type: document.querySelector("#activity-type").value,
//       address: document.querySelector("#activity-address").value,
//       phone_number: document.querySelector("#phone-number").value,
//       dateTime: document.querySelector("#date-time-activity").value,
//       comments: document.querySelector("#activity-comments").value,
//     };
// });

//   const url = `/add-activity`;

//   fetch(/add-activity, {
//     method: "POST",
//     body: JSON.stringify(activityInputs),
//     headers: {
//       "Content-Type": "application/json",
//     },
//   })
//     .then((response) => response.json())
//     .then((responseJson) => {
//       alert(responseJson.status);
//     });

///////////////////// map with marker here
// let map, infoWindow;
// function initMap() {
//   const map = new google.maps.Map(document.querySelector("#destination-map"), {
//     center: {
//       lat: 40.7128,
//       lng: 74.006,
//     },
//     zoom: 10,
//   });

//   // geocode
//   const chosenLocation = document.querySelector("#main-destination").innerText;

//   const geocoder = new google.maps.Geocoder();
//   geocoder.geocode({ address: chosenLocation }, (results, status) => {
//     if (status === "OK") {
//       // get the user's location by their coordinates
//       const userCurrentLoc = results[0].geometry.location;

//       // create marker here
//       new google.maps.Marker({
//         position: userCurrentLoc,
//         map,
//       });

//       // zoom in on the location
//       map.setCenter(userCurrentLoc);
//       map.setZoom(12);
//     } else {
//       alert(
//         `It was not possible to find your location for the following reason: ${status}`
//       );
//     }
//   });
// }

// marker.setMap(map);
