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

function prettifyPreparation() {
    let codeblocks = document.querySelectorAll("article code")
    codeblocks.forEach((block) => {
        block.classList.add('prettyprint')
    })
    let preblocks = document.querySelectorAll("article pre")
    preblocks.forEach((block) => {
        block.classList.add('prettyprint')
    })
}

avatarsExist();
prettifyPreparation();