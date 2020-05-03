// side navbar scripts:
const mySliedbar = document.getElementById("mySidebar")
const main = document.getElementById("main")

function openNav() {
    mySliedbar.style.width = "250px";
    main.style.marginLeft = "250px";
}

function closeNav() {
    mySliedbar.style.width = "0";
    main.style.marginLeft = "0";
}