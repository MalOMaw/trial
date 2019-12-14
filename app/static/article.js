function avatarsExist() {
    let avatars = document.querySelectorAll(".posteravatar");
    avatars.forEach((avatar) => {
        const request = new Request(avatar.getAttribute("src"));
            fetch(request).then(response => {
                if (response.status === 404) {
                    avatar.setAttribute("src", "/static/default_avatar.png");
                }
            })
    })
}

avatarsExist();