document.addEventListener("DOMContentLoaded", () => {
  const screen = document.getElementById("animation-screen");
  const mario = document.getElementById("mario");
  const peach = document.getElementById("peach");
  const bowser = document.getElementById("bowser");

  screen.style.display = "flex";

  // Mario rises
  setTimeout(() => {
    mario.classList.remove("hidden");
    mario.style.animation = "riseUp 2s forwards";
  }, 500);

  // Bowser and Peach enter from right
  // Bowser and Peach enter from right
  setTimeout(() => {
    peach.classList.remove("hidden");
    bowser.classList.remove("hidden");

    peach.style.left = "40%"; // ⬅️ slightly more to the left
    peach.style.top = "150px";

    bowser.style.left = "50%"; // ⬅️ slightly more to the left
    bowser.style.top = "150px";

    peach.style.animation = "enterRight 2s forwards";
    bowser.style.animation = "enterRight 2s forwards";
  }, 2700);
  
  // Peach cries, Bowser laughs
  setTimeout(() => {
    peach.style.animation = "peachCry 1.2s infinite";
    bowser.style.animation = "bowserLaugh 1.2s infinite";
  }, 5000);

  // Bowser & Peach exit left
  setTimeout(() => {
    peach.style.animation = "exitLeftFull 2.5s forwards";
    bowser.style.animation = "exitLeftFull 2.5s forwards";
  }, 7200);

  // Mario follows AFTER Bowser is gone
  setTimeout(() => {
    mario.style.animation = "marioFollowLeft 2.5s forwards";
  }, 10000);

  // Redirect to Level 3
  setTimeout(() => {
    window.location.href = "../lvl3/index_lvl3.html";
  }, 12600);
});
