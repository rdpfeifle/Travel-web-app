// flatpickr for plan-trip page

flatpickr("input[type=datetime-local]", {
  mode: "range",
  //   dateFormat: "m-d-Y",
  dateFormat: "Y-m-d",
  altInput: true,
  altFormat: "F j, Y",
});
