document.addEventListener("DOMContentLoaded", function () {
  const startButton = document.getElementById("start-button");
  const welcomeScreen = document.getElementById("welcome-screen");
  const animationScreen = document.getElementById("animation-screen");

  const peach = document.getElementById("peach");
  const bowser = document.getElementById("bowser");
  const mario = document.getElementById("mario");

  startButton.addEventListener("click", function () {
    // Show animation screen
    welcomeScreen.style.display = "none";
    animationScreen.style.display = "flex";

    // Peach shakes
    peach.classList.add("shake");

    // Bowser enters after 1s
    setTimeout(() => {
      bowser.classList.remove("hidden");
      bowser.classList.add("slide-in");
    }, 1000);

    // Peach and Bowser move right together at 2.5s
    setTimeout(() => {
      peach.classList.remove("shake");
      peach.classList.add("move-away");

      bowser.classList.remove("slide-in");
      bowser.classList.add("exit");
    }, 2500);

    // Mario runs at 4s
    setTimeout(() => {
      mario.classList.remove("jump");
      mario.classList.add("run");
    }, 4000);

    // Redirect after 6s
    setTimeout(() => {
      document.body.style.transition = "opacity 0.3s ease";
      document.body.style.opacity = "0";
      setTimeout(() => {
        window.location.href = "lvl1/index_lvl1.html";
      }, 300);
    }, 6000);
  });
});
