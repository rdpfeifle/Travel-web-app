// // -------- trip details page -------- //

// add event listener to the reservation's delete button
let deleteReservationBtns = document.querySelectorAll(".reservation-btn");
for (const button of deleteReservationBtns) {
  button.addEventListener("click", () => {
    console.log(button);
    fetch("/delete-reservation", {
      method: "POST",
      body: JSON.stringify({ reservation_to_delete: button.value }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.text())
      .then((status) => {
        // button.value is the reservation id
        document.querySelector(`#reservation-card-${button.value}`).remove();
      });
  });
}

// add event listener to the activity's delete button
let deleteActivityBtns = document.querySelectorAll(".activity-btn");
for (const button of deleteActivityBtns) {
  button.addEventListener("click", () => {
    console.log(button);
    fetch("/delete-activity", {
      method: "POST",
      body: JSON.stringify({ activity_to_delete: button.value }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.text())
      .then((status) => {
        // button.value is the activity id
        document.querySelector(`#activity-card-${button.value}`).remove();
      });
  });
}
