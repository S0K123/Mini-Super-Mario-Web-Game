document.addEventListener("DOMContentLoaded", function () {
  const animationScreen = document.getElementById("animation-screen");
  const mario = document.getElementById("mario");
  const fish = document.getElementById("fish");
  const danger = document.getElementById("danger");

  // Show screen
  animationScreen.style.display = "flex";

  // Mario swims in from far left — no fade
  mario.style.position = "absolute";
  mario.style.left = "-300px";
  mario.style.top = "50%";
  mario.style.opacity = "1"; // ✅ Always visible
  mario.style.transition = "none"; // ✅ No fade at all
  mario.style.transform = "translateY(-50%)";
  mario.style.animation = "swimToCenter 2.5s ease-out forwards";

  // Show danger icon above Mario after swim
  setTimeout(() => {
    danger.classList.remove("hidden");
    danger.style.opacity = "1";
  }, 2600);

  // Mario and danger dive
  setTimeout(() => {
    mario.style.left = "50%";
    mario.style.top = "50%";
    mario.style.transform = "translate(-50%, -50%) scale(1.1)";
    mario.style.animation = "diveTogetherFast 2.2s forwards";

    danger.style.animation = "diveTogether 2.5s forwards";
  }, 3600);

  // Fish appears and dives slowly
  setTimeout(() => {
    danger.classList.add("hidden");
    fish.classList.remove("hidden");
    fish.style.animation = "diveTogether 3.2s forwards";
  }, 3900);

  // Redirect after fish dive completes
  setTimeout(() => {
    window.location.href = "../lvl2/index_lvl2.html";
  }, 6700);
});
