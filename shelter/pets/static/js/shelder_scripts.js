$(document).ready(function () {
    const links = document.querySelectorAll(".link");
    links.forEach(link => addEventListener('click', function (e) {
        if ((link == e.target) && (link.classList.contains("active-elem") == false)){
            link.classList.add("active-elem");
        }
        else if ((link == e.target) && (link.classList.contains("active-elem") == true)){
        }
        else{
            link.classList.remove("active-elem");
        }
    }));
});
