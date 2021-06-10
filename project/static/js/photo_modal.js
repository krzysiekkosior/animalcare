let modal = document.querySelector(".modal")
let images = document.querySelectorAll("#caseImg");
let modalImg = document.getElementById("modalId");

for (let img of images) {
    img.addEventListener("click", e => {
        modal.style.display = "block";
        modalImg.src = img.src;
    })
}

let closeButton = document.querySelector(".close");
closeButton.addEventListener("click", () => modal.style.display = "none");
