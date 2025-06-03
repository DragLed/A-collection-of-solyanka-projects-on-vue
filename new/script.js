let btn = document.getElementById("btn1");
btn.addEventListener("click", () => {
    if (btn.className == "btn-Blue") {
        btn.className = "btn-Red"
    }
    else {
        btn.className = "btn-Blue"
    }
});
