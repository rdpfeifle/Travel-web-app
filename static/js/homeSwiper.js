// document.addEventListener("DOMContentLoaded", () => {
//   const mySwiper = new Swiper(".swiper", {
//     spaceBetween: 5,
//     // freeMode: true,
//     grabCursor: true,
//     // direction: "horizontal",
//     loop: true,
//     centeredSlides: true,
//     slidesPerView: 1.5,

//     // pagination
//     pagination: {
//       el: ".swiper-pagination",
//       clickable: true,
//     },

//     // autoplay
//     autoplay: {
//       delay: 3000,
//     },

//     centeredSlides: true,
//     // right and left arrows
//     navigation: {
//       nextEl: ".swiper-button-next",
//       prevEl: ".swiper-button-prev",
//     },
//   });
// });
// document.addEventListener("DOMContentLoaded", () => {
//   let swiper = new Swiper(".swiper-container", {
//     slidesPerView: "auto",
//     loop: true,
//     centeredSlides: true,
//     grabCursor: true,
//   });
// });

document.addEventListener("DOMContentLoaded", () => {
  const swiper = new Swiper(".swiper-container", {
    centeredSlides: true,
    slidesPerView: 1,
    loop: true,
    speed: 600,
    effect: "coverflow",

    coverflowEffect: {
      stretch: 0,
      depth: 80,
      rotate: 50,
      modifier: 1,
      slideShadows: true,
    },

    autoplay: {
      delay: 2500,
    },

    breakpoints: {
      320: {
        slidesPerView: "auto",
      },
      560: {
        slidesPerView: 2,
      },
      990: {
        slidesPerView: 3,
      },
    },

    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },

    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });
});
