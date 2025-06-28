// level1.js
window.addEventListener("DOMContentLoaded", () => {
  const startButton = document.getElementById("start-button");
  const welcomeScreen = document.getElementById("welcome-screen");
  const gameCanvas = document.getElementById("game-canvas");
  const messageDiv = document.getElementById("message");

  const ctx = gameCanvas.getContext("2d");
  gameCanvas.width = 1510;
  gameCanvas.height = 835;

  const bgImage = new Image();
  const marioImage = new Image();
  const goombaImage = new Image();
  const flagImage = new Image();

  let imagesLoaded = 0;
  const totalImages = 4;

  [bgImage, marioImage, goombaImage, flagImage].forEach((img) => {
    img.onload = () => {
      imagesLoaded++;
      if (imagesLoaded === totalImages) {
        startButton.disabled = false;
        console.log("All images loaded");
      }
    };
  });

  bgImage.src = "bgd.jpg";
  marioImage.src = "classic_mario.jpeg";
  goombaImage.src = "goomba.jpg";
  flagImage.src = "flag.jpeg";

  const themeSong = new Audio("mario_theme_song.mp3");
  const dieSound = new Audio("../sounds/mario_loses_life.mp3");
  const winSound = new Audio("../sounds/level_complete.mp3");
  const gameOverSound = new Audio("../sounds/game_over.mp3");
  themeSong.loop = true;

  let player, playerVelX, playerVelY, gravity, jumpPower, speed, onGround;
  let coins = [];
  let enemies = [];
  let enemyDirs = [];
  let platforms = [];
  let ground, goal;
  let coinCollected = 0;
  let lives = 3;
  let isGameOver = false;

  function startLevel1() {
    initLevel1();
  }

  startButton.addEventListener("click", () => {
    welcomeScreen.style.display = "none";
    gameCanvas.style.display = "block";
    messageDiv.textContent = "Level 1 Started";

    themeSong.play().catch((error) => {
      console.warn("⚠️ Music autoplay blocked:", error);
    });

    startLevel1();
  });

  function initLevel1() {
    console.log("Level 1 started");
    isGameOver = false;
    

    player = { x: 50, y: 400, width: 40, height: 60 };
    playerVelX = 0;
    playerVelY = 0;
    gravity = 0.5;
    jumpPower = -10;
    speed = 3;
    onGround = false;

    ground = { x: 0, y: 795, width: gameCanvas.width, height: 40 };

    platforms = [
      { x: 200, y: 685, width: 120, height: 20 },
      { x: 400, y: 615, width: 120, height: 20 },
      { x: 600, y: 555, width: 120, height: 20 },
      { x: 800, y: 615, width: 120, height: 20 },
      { x: 1000, y: 685, width: 120, height: 20 },
    ];

    coins = [
      { x: 250, y: 645, radius: 10 },
      { x: 460, y: 575, radius: 10 },
      { x: 650, y: 515, radius: 10 },
      { x: 850, y: 575, radius: 10 },
      { x: 1050, y: 645, radius: 10 },
    ];

    enemies = [];
    enemyDirs = [];
    for (let i = 0; i < 3; i++) {
      const x = Math.floor(Math.random() * (1300 - 200 + 1)) + 200;
      enemies.push({ x, y: 755, width: 40, height: 40 });
      enemyDirs.push(1);
    }

    goal = { x: 1300, y: 735, width: 20, height: 60 };

    update();
  }

  let keys = {};
  document.addEventListener("keydown", (e) => (keys[e.code] = true));
  document.addEventListener("keyup", (e) => (keys[e.code] = false));

  function update() {
    if (isGameOver) return;

    if (keys["ArrowLeft"]) playerVelX = -speed;
    else if (keys["ArrowRight"]) playerVelX = speed;
    else playerVelX = 0;

    if (keys["Space"] && onGround) {
      playerVelY = jumpPower;
      onGround = false;
    }

    player.x += playerVelX;
    playerVelY += gravity;
    player.y += playerVelY;

    if (player.x < 0) player.x = 0;
    if (player.x + player.width > gameCanvas.width)
      player.x = gameCanvas.width - player.width;

    onGround = false;
    for (const plat of [...platforms, ground]) {
      if (rectCollision(player, plat) && playerVelY >= 0) {
        player.y = plat.y - player.height;
        playerVelY = 0;
        onGround = true;
      }
    }
    

    enemies.forEach((enemy, i) => {
      enemy.x += enemyDirs[i] * 2;
      if (enemy.x < 100 || enemy.x > 1300) enemyDirs[i] *= -1;

      if (rectCollision(player, enemy)) {
        lives--;
        themeSong.pause();
        dieSound.currentTime = 0;
        dieSound.play();

        if (lives <= 0) {
          isGameOver = true;
          gameCanvas.style.display = "none";
          messageDiv.textContent = "💀 GAME OVER — Press R to restart.";
          messageDiv.style.fontSize = "48px";
          messageDiv.style.color = "red";
          messageDiv.style.textAlign = "center";
          messageDiv.style.marginTop = "350px";

          // DieSound stops after 0.5s, then gameOverSound plays
          setTimeout(() => {
            dieSound.pause();
            gameOverSound.currentTime = 0;
            gameOverSound.play();
          }, 1750); // 500ms = 0.5 seconds

          document.addEventListener("keydown", function restartGame(event) {
            if (event.key === "r" || event.key === "R") {
              document.removeEventListener("keydown", restartGame);
              lives = 3;
              coinCollected = 0;
              messageDiv.textContent = "";
              gameCanvas.style.display = "block";
              themeSong.currentTime = 0;
              themeSong.play();
              startLevel1();
            }
          });
          return;
        } else {
          dieSound.onended = () => {
            if (themeSong.paused && !isGameOver) {
              themeSong.play();
            }
          };
          player.x = 50;
          player.y = 400;
          playerVelY = 0;
        }
      }      
    });

    coins = coins.filter((coin) => {
      const dist = Math.hypot(
        player.x + player.width / 2 - coin.x,
        player.y + player.height / 2 - coin.y
      );
      if (dist < 30) {
        coinCollected++;
        console.log("Coins:", coinCollected);
        return false;
      }
      return true;
    });

    if (rectCollision(player, goal)) {
      if (coins.length === 0) {
        themeSong.pause();
        dieSound.pause();
        gameOverSound.pause();
        winSound.play();
        completeLevel1();
        return;
      } else {
        alert("Collect all coins to move to Level 2!");
      }
    }

    draw();
    requestAnimationFrame(update);
  }

  function draw() {
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);

    ctx.drawImage(
      bgImage,
      0,
      0,
      bgImage.width,
      bgImage.height - 50,
      0,
      0,
      gameCanvas.width,
      gameCanvas.height
    );

    ctx.drawImage(marioImage, player.x, player.y, player.width, player.height);

    enemies.forEach((enemy) =>
      ctx.drawImage(goombaImage, enemy.x, enemy.y, enemy.width, enemy.height)
    );

    ctx.drawImage(flagImage, goal.x, goal.y, goal.width, goal.height);

    ctx.fillStyle = "#32CD32";
    ctx.fillRect(ground.x, ground.y, ground.width, ground.height);

    ctx.fillStyle = "#8B4513";
    platforms.forEach((p) => ctx.fillRect(p.x, p.y, p.width, p.height));

    ctx.fillStyle = "#FFFF00";
    coins.forEach((coin) => {
      ctx.beginPath();
      ctx.arc(coin.x, coin.y, 10, 0, Math.PI * 2);
      ctx.fill();
    });

    drawText(
      `Lives: ${lives}   Coins: ${coinCollected}`,
      "#FFFF00",
      20,
      30,
      24
    );
  }

  function drawText(text, color, x, y, size = 48) {
    ctx.fillStyle = color;
    ctx.font = `${size}px Arial`;
    ctx.fillText(text, x, y);
  }

  function rectCollision(a, b) {
    return (
      a.x < b.x + b.width &&
      a.x + a.width > b.x &&
      a.y < b.y + b.height &&
      a.y + a.height > b.y
    );
  }

  function completeLevel1() {
    themeSong.pause();
    dieSound.pause();
    gameOverSound.pause();
    winSound.play();

    gameCanvas.style.display = "none";
    messageDiv.textContent = "🎉 Level 1 Completed!";
    messageDiv.style.fontSize = "48px";
    messageDiv.style.color = "gold";
    messageDiv.style.textAlign = "center";
    messageDiv.style.marginTop = "250px";

    winSound.onended = () => {
      window.location.href = "/mario-web/lvl1_to_lvl2_transition/lvl1_2.html";
    };
  }
});
