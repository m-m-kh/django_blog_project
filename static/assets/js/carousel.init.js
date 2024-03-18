/**
 * Theme: Blogloo - Tailwind Blogs Template
 * Author: Mannatthemes
 * Carousel Js
 */
var swiper = new Swiper(".defaultSwiper", {
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
  });
  var swiper = new Swiper(".paginationSwiper", {
    pagination: {
        el: ".swiper-pagination",
    },
     navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
  });    
  