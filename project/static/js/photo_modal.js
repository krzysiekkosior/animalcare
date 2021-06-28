let modal = document.querySelector(".modal")
let images = document.querySelectorAll("#caseImg");
let modalImg = document.getElementById("modalId");
let body = document.querySelector("body");

for (let img of images) {
    img.addEventListener("click", e => {
        modal.style.display = "block";
        modalImg.src = img.src;
    })
}

let closeButton = document.querySelector(".close");
closeButton.addEventListener("click", () => modal.style.display = "none");

body.addEventListener("keydown", e => {
    if (e.key === "Escape") {
        modal.style.display = "none";
    }
})
