/////// Both login and sign up pages ///////

const passwordVisibility = () => {
  let showPassword = document.getElementById("floatingPassword");
  if (showPassword.type === "password") {
    showPassword.type = "text";
  } else {
    showPassword.type = "password";
  }
};

/////// Login ///////
