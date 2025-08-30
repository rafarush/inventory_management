
let element = document.getElementById("app-menu")
// Clonar el elemento sin eventos
let nuevoElemento = element.cloneNode(true);

// Reemplazar el elemento original con el nuevo
element.parentNode.replaceChild(nuevoElemento, element);

function toggleMenu() {

    let menu = document.getElementById("app-menu");
    if (menu.style.width < "100px" || menu.style.width === "") {
        menu.style.width = "200px"; // Ajusta el ancho según tus necesidades
    } else {
        menu.style.width = "0px";
    }
}