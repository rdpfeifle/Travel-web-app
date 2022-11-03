// flatpickr for plan-trip page

flatpickr("input[type=datetime-local]", {
  mode: "range",
  //   dateFormat: "m-d-Y",
  dateFormat: "Y-m-d",
  altInput: true,
  altFormat: "F j, Y",
});

//---- Details Page ----//

// countdown for the trip
const timeLeft = document.getElementById("time-left");

// dayOfTrip selects the trip start_date given by the user
let dayOfTrip = new Date("2022-11-10T03:24:00");

const second = 1000;
const minute = second * 60;
const hour = minute * 60;
const day = hour * 24; // milliseconds
let timerId;

const countDown = () => {
  const today = new Date(); // subtract dayOfTrip by today's date
  console.log(today);
  const timeSpan = dayOfTrip - today;
  console.log(timeSpan);
  // checks if it has been a day since chosen start date
  if (timeSpan <= -day) {
    timeLeft.innerHTML = "I hope you arrived well in your destination!";
    clearInterval(timerId);
    return;
  }

  // checks if it is the trip day
  if (timeSpan <= 0) {
    timeLeft.innerHTML = "It's finally your trip day! Yay!";
    clearInterval(timerId);
    return;
  }

  const days = Math.floor(timeSpan / day);
  const hours = Math.floor((timeSpan % day) / hour);
  const minutes = Math.floor((timeSpan % hour) / minute);
  const seconds = Math.floor((timeSpan % minute) / second);

  timeLeft.innerHTML =
    timeLeft.innerHTML = `${days} days ${hours} hours ${minutes} minutes ${seconds} seconds left`;
};

timerId = setInterval(countDown, second);
