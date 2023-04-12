$(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })


function reveal() {
    var reveals = document.querySelectorAll(".reveal");
    for (var i = 0; i < reveals.length; i++) {
      var windowHeight = window.innerHeight;
      var elementTop = reveals[i].getBoundingClientRect().top;
      var elementVisible = 150;
      if (elementTop < windowHeight - elementVisible) {
        reveals[i].classList.add("active");
      } else {
        reveals[i].classList.remove("active");
      }
    }
}

window.addEventListener("scroll", reveal);

$(".mbti1").animate({
    width: "66%",
}, 1000);
    
$(".mbti2").animate({
    width: "54%",
}, 1000);

$(".mbti3").animate({
    width: "59%",
}, 1000);

$(".mbti4").animate({
    width: "94%",
}, 1000);