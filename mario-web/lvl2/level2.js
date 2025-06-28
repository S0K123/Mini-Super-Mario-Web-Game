// 📏 Setup canvas
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const messageDiv = document.getElementById("message");


// Set canvas to full screen dimensions
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Resize canvas whenever the window is resized
window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});

// ▶️ Start button logic to begin the game
document.getElementById("start-button").addEventListener("click", () => {
  // Hide the welcome screen and display the canvas
  document.getElementById("welcome-screen").style.display = "none";
  canvas.style.display = "block";
  messageDiv.style.display = "none"

  // 🖼️ Load all required images
  const bgImage = new Image();
  bgImage.src = "bgd2.jpg";

  const blooperImg = new Image();
  blooperImg.src = "blooper.jpg";

  const fishImg = new Image();
  fishImg.src = "fish.jpg";

  const flagImg = new Image();
  flagImg.src = "../lvl1/flag.jpeg";

  const marioImg = new Image();
  marioImg.src = "../lvl1/classic_mario.jpeg";

  // 🔊 Load all required audio files
  const underwaterTheme = new Audio("underwater_theme.mp3");
  const dieSound = new Audio("../sounds/mario_loses_life.mp3");
  const winSound = new Audio("../sounds/level_complete.mp3");
  const gameOverSound = new Audio("../sounds/game_over.mp3");

  // Start game only after background image is fully loaded
  bgImage.onload = () => {
    startLevel2(
      bgImage,
      blooperImg,
      fishImg,
      flagImg,
      marioImg,
      underwaterTheme,
      dieSound,
      winSound,
      gameOverSound
    );
  };
});

// 🎮 Main game function
function startLevel2(
  bgImage,
  blooperImg,
  fishImg,
  flagImg,
  marioImg,
  underwaterTheme,
  dieSound,
  winSound,
  gameOverSound
) {
  const WIDTH = canvas.width;
  const HEIGHT = canvas.height;

  // 👨 Mario setup
  let player = { x: 50, y: 600, width: 40, height: 60, xVel: 0, yVel: 0 };
  const gravity = 0.2;
  const jumpPower = -7;
  const speed = 3;
  let onGround = false;
  let coinCount = 0;
  let lives = 3;
  let isGameOver = false;
  let recentlyHit = false; // 🛡️ Prevent rapid life loss
  let animationId;
  // Sound control variable
  let soundTimeout = null;

  // 🎮 Keyboard input tracking
  const keys = {};
  document.onkeydown = (e) => (keys[e.key] = true);
  document.onkeyup = (e) => (keys[e.key] = false);

  // 🎵 Background music setup
  underwaterTheme.loop = true;
  underwaterTheme.play();

  // 🌊 Ground setup to always be at the bottom
  const ground = { x: 0, y: HEIGHT - 40, width: WIDTH, height: 40 };

  // 🪵 Platforms - static
  const platforms = [
    { x: 200, y: 620, width: 120, height: 20 },
    { x: 400, y: 500, width: 120, height: 20 },
    { x: 600, y: 400, width: 120, height: 20 },
    { x: 800, y: 300, width: 120, height: 20 },
    { x: 1000, y: 200, width: 120, height: 20 },
  ];

  // 🛝 Platforms - moving
  const movingPlatforms = [
    { x: 50, y: 520, width: 100, height: 20, dir: 1 },
    { x: 1100, y: 400, width: 100, height: 20, dir: -1 },
    { x: 1250, y: 600, width: 100, height: 20, dir: 1 },
  ];

  // 🪙 Coins the player can collect
  const coins = [
    { x: 245, y: 580 },
    { x: 445, y: 460 },
    { x: 645, y: 360 },
    { x: 845, y: 260 },
    { x: 1040, y: 160 },
  ];

  // 🚩 Level end goal
  const goal = { x: 1300, y: HEIGHT - 100, width: 20, height: 60 };

  // 🦑 Enemies
  let bloopers = [],
    fishEnemies = [];

  // Randomized enemy movement
  for (let i = 0; i < 3; i++) {
    bloopers.push({
      x: 500 + i * 300,
      y: 500,
      width: 40,
      height: 40,
      dx: Math.random() < 0.5 ? -1 : 1,
      dy: Math.random() < 0.5 ? -1 : 1,
    });

    fishEnemies.push({
      x: 600 + i * 300,
      y: 620,
      width: 40,
      height: 40,
      dx: Math.random() < 0.5 ? -1 : 1,
      dy: Math.random() < 0.5 ? -1 : 1,
    });
  }

  // 🧱 Utility to draw image or fallback color
  function drawImageOrRect(img, obj, fallbackColor) {
    if (img.complete) {
      ctx.drawImage(img, obj.x, obj.y, obj.width, obj.height);
    } else {
      drawRect(obj, fallbackColor);
    }
  }

  // 🟦 Draw rectangle
  function drawRect(obj, color) {
    ctx.fillStyle = color;
    ctx.fillRect(obj.x, obj.y, obj.width, obj.height);
  }

  // 🔘 Draw circle
  function drawCircle(x, y, r, color) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
  }

  // 📦 Collision detection
  function rectsCollide(a, b) {
    return (
      a.x < b.x + b.width &&
      a.x + a.width > b.x &&
      a.y < b.y + b.height &&
      a.y + a.height > b.y
    );
  }

  // ⏮️ Reset Mario position
  function resetPlayer() {
    player.x = 50;
    player.y = 600;
    player.yVel = 0;
  }

  // 🌀 Main game loop
  function gameLoop() {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);

    // 🛑 If game is over, show only black screen and Game Over text
    if (isGameOver) {
      ctx.fillStyle = "black";
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = "red";
      ctx.font = "48px Comic Sans MS";
      ctx.textAlign = "center"; // Center the text
      ctx.fillText(
        "💀 GAME OVER — Press R to Restart",
        WIDTH / 2, // Center horizontally
        HEIGHT / 2 // Center vertically
      );
      return;
    }

    ctx.drawImage(bgImage, 0, 0, WIDTH, HEIGHT);

    // 🎮 Player movement logic
    if (keys["ArrowLeft"]) player.xVel = -speed;
    else if (keys["ArrowRight"]) player.xVel = speed;
    else player.xVel *= 0.9;

    if (keys[" "] && onGround) {
      player.yVel = jumpPower;
      onGround = false;
    }

    // 📐 Update player position
    player.x += player.xVel;
    player.yVel += gravity;
    player.y += player.yVel;

    // ⛔ Prevent going outside the screen
    if (player.x < 0) player.x = 0;
    if (player.x + player.width > WIDTH) player.x = WIDTH - player.width;

    onGround = false;

    // 🧱 Check collisions with platforms and ground
    function checkCollision(plat) {
      if (
        player.x < plat.x + plat.width &&
        player.x + player.width > plat.x &&
        player.y + player.height > plat.y &&
        player.y < plat.y + plat.height
      ) {
        player.y = plat.y - player.height;
        player.yVel = 0;
        onGround = true;
      }
    }

    checkCollision(ground);
    platforms.forEach(checkCollision);
    movingPlatforms.forEach((p) => {
      checkCollision(p);
      p.x += p.dir * 2;
      if (p.x < 20 || p.x > WIDTH - 120) p.dir *= -1;
    });

    // 🦑 Move enemies and bounce off edges
    [...bloopers, ...fishEnemies].forEach((e) => {
      e.x += e.dx * 2;
      e.y += e.dy * 2;
      if (e.x < 0 || e.x > WIDTH - 40) e.dx *= -1;
      if (e.y < 0 || e.y > HEIGHT - 40) e.dy *= -1;
    });

    // 💥 Enemy collisions
    // 💥 Enemy collisions
    [...bloopers, ...fishEnemies].forEach((e) => {
      if (rectsCollide(player, e) && !recentlyHit) {
        recentlyHit = true;
        lives--;

        // Clear any existing sound timeouts
        if (soundTimeout) clearTimeout(soundTimeout);

        underwaterTheme.pause();
        dieSound.currentTime = 0;
        dieSound.play().catch((e) => console.log("Audio error:", e));

        if (lives <= 0) {
          isGameOver = true;
          cancelAnimationFrame(animationId);

          // Delay game over sound by 0.5s after die sound starts
          soundTimeout = setTimeout(() => {
            gameOverSound.currentTime = 0;
            gameOverSound.play();
          }, 500);

          // Display red "GAME OVER — Press R to Restart" like Level 1
          messageDiv.style.display = "block";
          messageDiv.innerText = "💀 GAME OVER — Press R to Restart";
          messageDiv.style.position = "absolute";
          messageDiv.style.top = "45%";
          messageDiv.style.left = "50%";
          messageDiv.style.transform = "translate(-50%, -50%)";
          messageDiv.style.fontSize = "48px";
          messageDiv.style.color = "red";
          messageDiv.style.textAlign = "center";

          return;
        }        

        resetPlayer();

        // Allow next hit only after 1.5 seconds
        soundTimeout = setTimeout(() => {
          recentlyHit = false;
          if (!isGameOver) underwaterTheme.play();
        }, 1500);

        return;
      }
    });

    // 🪙 Coin collection logic
    for (let i = coins.length - 1; i >= 0; i--) {
      const c = coins[i];
      if (
        player.x < c.x + 20 &&
        player.x + player.width > c.x &&
        player.y < c.y + 20 &&
        player.y + player.height > c.y
      ) {
        coins.splice(i, 1);
        coinCount++;
      }
    }

    // 🎯 Goal logic
    if (
      player.x < goal.x + goal.width &&
      player.x + player.width > goal.x &&
      player.y < goal.y + goal.height &&
      player.y + player.height > goal.y
    ) {
      if (coins.length === 0) {
        isGameOver = true;
        underwaterTheme.pause();
        winSound.play();
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, WIDTH, HEIGHT);
        ctx.fillStyle = "gold";
        ctx.font = "36px Comic Sans MS";
        ctx.fillText("🎉 Level 2 Complete!", WIDTH / 2 - 150, HEIGHT / 2);
        setTimeout(() => {
          window.location.href = "../lvl2_to_lvl3_transition/lvl2_3.html"; // ✅ navigate from lvl2 to lvl3
        }, 4000);
        return;
      } else {
        ctx.fillStyle = "red";
        ctx.font = "20px Comic Sans MS";
        ctx.fillText("Collect all coins first!", player.x - 50, player.y - 20);
      }
    }

    // 🖍️ Draw all game objects
    drawRect(ground, "#3282b8");
    platforms.forEach((p) => drawRect(p, "#72a0c1"));
    movingPlatforms.forEach((p) => drawRect(p, "#20c997"));
    coins.forEach((c) => drawCircle(c.x + 10, c.y + 10, 10, "gold"));
    bloopers.forEach((e) => drawImageOrRect(blooperImg, e, "white"));
    fishEnemies.forEach((e) => drawImageOrRect(fishImg, e, "orange"));
    drawImageOrRect(flagImg, goal, "#ffff00");
    drawImageOrRect(marioImg, player, "red");

    // 📊 Display lives and coins
    ctx.fillStyle = "white";
    ctx.font = "24px Comic Sans MS";
    ctx.fillText(`Lives: ${lives}   Coins: ${coinCount}`, 20, 30);

    animationId = requestAnimationFrame(gameLoop);
  }

  // 🚀 Start the first frame
gameLoop();

// ⌨️ Restart logic like Level 1
document.addEventListener("keydown", function restartLevel2(e) {
  if ((e.key === "r" || e.key === "R") && isGameOver) {
    // Clear message and restart
    messageDiv.innerText = "";
    messageDiv.style.display = "none";
    canvas.style.display = "block";

    // Restart level
    startLevel2(
      bgImage,
      blooperImg,
      fishImg,
      flagImg,
      marioImg,
      underwaterTheme,
      dieSound,
      winSound,
      gameOverSound
    );
  }
});
}
