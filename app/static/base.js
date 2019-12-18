function displayFlashes() {
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
}

function avatarsExist() {
    let avatars = document.querySelectorAll(".avatar");
    avatars.forEach((avatar) => {
        const request = new Request(avatar.getAttribute("src"));
            fetch(request).then(response => {
                if (response.status === 404) {
                    avatar.setAttribute("src", "/static/default_avatar.png");
                }
            })
    })
}

displayFlashes();
avatarsExist();