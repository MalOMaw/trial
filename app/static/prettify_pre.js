function prettifyPreparation() {
    let codeblocks = document.querySelectorAll("article code");
    codeblocks.forEach((block) => {
        block.classList.add('prettyprint')
    });
    let preblocks = document.querySelectorAll("article pre");
    preblocks.forEach((block) => {
        block.classList.add('prettyprint')
    })
}


prettifyPreparation();