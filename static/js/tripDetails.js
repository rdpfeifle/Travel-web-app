// -------- trip details page -------- //

document.querySelector("#save-activity").addEventListener("click", (evt) => {
  evt.preventDefault();
  console.log("In the event handler");

  const activityInputs = {
    trip_id: document.querySelector("#trip_id").value,
    activity_name: document.querySelector("#activity-name").value,
    activity_type: document.querySelector("#activity-type").value,
    address: document.querySelector("#activity-address").value,
    phone_number: document.querySelector("#phone-number").value,
    dateTime: document.querySelector("#date-time-activity").value,
    comments: document.querySelector("#activity-comments").value,
  };

  fetch("/add-activity", {
    method: "POST",
    body: JSON.stringify(activityInputs),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((responseJson) => {
      alert(responseJson.status);
    });
});
