let copyDivs = document.querySelectorAll(".copy_div");

copyDivs.forEach(copyDiv => {
    let copyButton = copyDiv.querySelector(".copy_button");
    copyButton.addEventListener("click", function () {
        let input = copyDiv.querySelector(".copy_text");
        input.select();
        document.execCommand("copy");
        setTimeout(function () {
            window.getSelection().removeAllRanges();
        }, 2500);
    });
});