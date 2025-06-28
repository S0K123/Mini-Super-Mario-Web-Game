document.addEventListener("DOMContentLoaded", () => {
  const screen = document.getElementById("ending-screen");
  const peach = document.getElementById("peach");
  const toad = document.getElementById("toad");
  const mario = document.getElementById("mario");
  const congrats = document.getElementById("congrats-text");
  const finalMsg = document.getElementById("final-message");

  screen.style.display = "block";

  // Step 1: Slide in from left
  peach.classList.add("enter");
  toad.classList.add("enter");
  mario.classList.add("enter");

  // Step 2: Pause and celebrate
  setTimeout(() => {
    peach.classList.remove("enter");
    toad.classList.remove("enter");
    mario.classList.remove("enter");

    peach.classList.add("celebrate");
    toad.classList.add("celebrate");
    mario.classList.add("celebrate");
  }, 1600);

  // Step 3: Show text
  setTimeout(() => {
    congrats.style.display = "block";
    finalMsg.style.display = "block";
  }, 2000);

  // Step 4: Slide out to right after celebration
  setTimeout(() => {
    peach.classList.remove("celebrate");
    toad.classList.remove("celebrate");
    mario.classList.remove("celebrate");

    peach.classList.add("exit");
    toad.classList.add("exit");
    mario.classList.add("exit");

    // ✅ Move text to center after characters exit
    setTimeout(() => {
      congrats.classList.add("center-text");
      finalMsg.classList.add("center-text");
    }, 1500); // wait for exit animation
  }, 5000);

  // Step 5: Confetti setup
  const canvas = document.getElementById("confetti-canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const confetti = [];
  for (let i = 0; i < 100; i++) {
    confetti.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 6 + 2,
      d: Math.random() * 5 + 1,
      color: `hsl(${Math.random() * 360}, 100%, 70%)`,
    });
  }

  function drawConfetti() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    confetti.forEach((c) => {
      ctx.beginPath();
      ctx.arc(c.x, c.y, c.r, 0, Math.PI * 2);
      ctx.fillStyle = c.color;
      ctx.fill();
      c.y += c.d;
      if (c.y > canvas.height) {
        c.y = -10;
        c.x = Math.random() * canvas.width;
      }
    });
    requestAnimationFrame(drawConfetti);
  }

  drawConfetti();

  // Step 6: Press R to return
  document.addEventListener("keydown", (e) => {
    if (e.key === "r" || e.key === "R") {
      window.location.href = "../index.html";
    }
  });
});
