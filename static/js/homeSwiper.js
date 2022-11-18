document.addEventListener("DOMContentLoaded", () => {
  const mySwiper = new Swiper(".swiper", {
    spaceBetween: 5,
    // freeMode: true,
    grabCursor: true,
    // direction: "horizontal",
    loop: true,
    centeredSlides: true,
    slidesPerView: 1.5,

    // pagination
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },

    // autoplay
    autoplay: {
      delay: 3000,
    },

    centeredSlides: true,
    // right and left arrows
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });
});
