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
