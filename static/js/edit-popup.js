const editButtons = document.querySelectorAll(".contact-edit-button");
const popup = document.querySelector(".edit-popup-wrapper");
const close = document.querySelector(".edit-popup-close");

editButtons.forEach(button => {
    const id = button.id;
    const name = document.getElementById(id).querySelector(".contact-name").textContent;

    button.addEventListener("click", () => {
        popup.style.display = "flex";
        popup.querySelector("form").action = "/contacts/edit/"+id;
        popup.querySelector(".edit-name").value = name;
        popup.querySelector(".edit-id").value = id;
    })

    close.addEventListener("click", () => {
        popup.style.display = "none";
    })
});