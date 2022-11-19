// // -------- trip details page -------- //

// add event listener to the toggle modal
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
