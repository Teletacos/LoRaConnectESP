const popup = document.querySelector(".add-popup-wrapper");
const close = document.querySelector(".add-popup-close");
const button = document.querySelector(".header-add-button")

button.addEventListener("click", () => {
  popup.style.display = "flex";
})

close.addEventListener("click", () => {
  popup.style.display = "none";
})
