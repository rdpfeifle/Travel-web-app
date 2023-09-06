"use strict";

//------------------------ Both login and sign up pages ------------------------//

const passwordVisibility = () => {
  let showPassword = document.getElementById("floatingPassword");
  if (showPassword.type === "password") {
    showPassword.type = "text";
  } else {
    showPassword.type = "password";
  }
};

//------------------------ flatpickr for plan-trip page ------------------------//

flatpickr("input[type=datetime-local]", {
  mode: "range",
  // dateFormat: "m-d-Y",
  dateFormat: "Y-m-d",
  altInput: true,
  altFormat: "F j, Y",
});

//---------------------- delete trip ----------------------//

// my trips page
let deleteTripBtns = document.querySelectorAll(".trip-btn");
for (const button of deleteTripBtns) {
  button.addEventListener("click", () => {
    console.log(button);
    fetch("/delete-trip", {
      method: "POST",
      body: JSON.stringify({ tripToDelete: button.value }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.text())
      .then((status) => {
        // button.value is the trip id
        document.querySelector(`#trip-card-${button.value}`).remove();
      });
  });
}
