const addPopup = document.querySelector(".add-popup-wrapper");
const addClose = document.querySelector(".add-popup-close");
const addButton = document.querySelector(".header-add-button")

addButton.addEventListener("click", () => {
  addPopup.style.display = "flex";
})

addClose.addEventListener("click", () => {
  addPopup.style.display = "none";
})
