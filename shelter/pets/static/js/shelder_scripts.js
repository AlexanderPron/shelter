$(document).ready(function () {
    const links = document.querySelectorAll(".link");
    // let currActiveLink = document.querySelector(".active-elem");
    links.forEach(link => addEventListener('click', function (e) {
        if ((link == e.target) && (link.classList.contains("active-elem") == false)){
            link.classList.add("active-elem");
            // currActiveLink = link
        }
        else if ((link == e.target) && (link.classList.contains("active-elem") == true)){
        }
        else{
            link.classList.remove("active-elem");
        }
    }));
});
