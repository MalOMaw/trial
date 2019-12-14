let flashes = document.querySelectorAll('.flash');
let actualTimeOut = 1000;
let delay = 3000;
flashes.forEach((flash) => {
    setTimeout(() => {
        flash.classList.add("hidden-flash")
    }, actualTimeOut);
    setTimeout(() => {
        flash.remove()
    }, actualTimeOut+delay);
    actualTimeOut += 1000;
});