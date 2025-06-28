function startLevel3() {
  // 🟡 Level 3: Boss Battle Setup
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");
  canvas.width = 1400;
  canvas.height = 600;

  // Load images
  const bg3 = new Image();
  bg3.src = "bgd3.jpg";
  const marioImg = new Image();
  marioImg.src = "../lvl1/classic_mario.jpeg";
  const bowserImg = new Image();
  bowserImg.src = "bowser.jpeg";
  const princessPeachImg = new Image();
  princessPeachImg.src = "princess_peach.jpg";
  const toadImg = new Image();
  toadImg.src = "toad.jpg";
  const redMushroomImg = new Image();
  redMushroomImg.src = "red_mushroom.jpg";
  const blueMushroomImg = new Image();
  blueMushroomImg.src = "blue_mushroom.jpg";
  const greenMushroomImg = new Image();
  greenMushroomImg.src = "green_mushroom.jpg";
  const starImg = new Image();
  starImg.src = "star.jpg";
  const flagImg3 = new Image();
  flagImg3.src = "../lvl1/flag.jpeg";

  // Load audio
  const finalBattleMusic = new Audio("final_battle.mp3");
  const levelCompleteMusic = new Audio("../sounds/level_complete.mp3"); // ✅ New music
  const winSound = new Audio("win.mp3");
  const gameOverSound = new Audio("../sounds/mario_loses_life.mp3");

  // Constants
  const WIDTH = canvas.width,
    HEIGHT = canvas.height,
    GROUND_Y = 320;
  const FIRE_WATER_DURATION = 50;
  const DAMAGE_AMOUNT = 5,
    FIRE_DAMAGE = 1, // 🔥 Less fireball damage
    WATER_DAMAGE = 1, // 💧 Less waterball damage
    STAR_DAMAGE = 0.5; // ⭐ Very little star damage

  // Game state variables
  let mario = { x: 50, y: GROUND_Y, width: 40, height: 60, vy: 0, speed: 10 }; // 🟢 Faster Mario
  let bowser = { x: 1000, y: GROUND_Y - 5, width: 60, height: 80 };
  let marioHealth = 500,
    bowserHealth = 600;
  let fireballsMario = [],
    waterballsMario = [],
    bowserFireballs = [],
    fallingSpikes = [],
    powerups = [];
  let firedPowerupKeys = { f: false, w: false, g: false, s: false };
  let marioFire = false,
    marioWater = false,
    marioStar = false,
    marioShielded = false,
    marioInvincible = false,
    marioBig = false;
  let marioFireTimer = 0,
    marioWaterTimer = 0,
    starTimer = 0,
    shieldTimer = 0,
    invincibleTimer = 0;
  let bowserFireTimer = 0,
    bowserFireballTimer = 0,
    bowserInvincible = false,
    bowserInvincibleTimer = 0;
  let bowserJumping = false,
    bowserJumpTimer = 0,
    bowserHitBack = false,
    bowserBackTimer = 0;
  let bowserAlive = true,
    gameOver = false,
    gameWon = false,
    finalBattleMusicPlaying = false,
    winSoundPlayed = false,
    levelCompleteMusicPlayed = false;
  let flagReached = false,
    flag = { x: 1300, y: GROUND_Y - 60, width: 20, height: 60 };
  let animationTimer = 0;
  let marioHitCooldown = 0;
  let flagReachedTime = 0;
  let showCongrats = false;
  let levelCompleteOver = false;
  let showPeachToad = false;
  let showCongratsScreen = false;
  let congratsFrameTimer = 0;

  let keys = {};
  window.addEventListener("keydown", (e) => (keys[e.key.toLowerCase()] = true));
  window.addEventListener("keyup", (e) => {
    keys[e.key.toLowerCase()] = false;
    if (["f", "w", "g", "s"].includes(e.key.toLowerCase()))
      firedPowerupKeys[e.key.toLowerCase()] = false;
  });

  function collides(a, b) {
    return (
      a.x < b.x + b.width &&
      a.x + a.width > b.x &&
      a.y < b.y + b.height &&
      a.y + a.height > b.y
    );
  }

  function drawHealthBar(x, y, w, h, percent, label) {
    ctx.fillStyle = "black";
    ctx.fillRect(x, y, w, h);
    ctx.fillStyle = "red";
    ctx.fillRect(x, y, w * percent, h);
    ctx.fillStyle = "white";
    ctx.font = "16px Comic Sans MS";
    ctx.fillText(label, x, y - 5);
  }

  function handlePowerup(type) {
    if (!bowserAlive) return; // ✅ Don't allow power-ups after Bowser defeat
    switch (type) {
      case "green":
        marioHealth = Math.min(500, marioHealth + 20);
        marioShielded = true;
        shieldTimer = 180;
        marioInvincible = true;
        invincibleTimer = 60;
        marioBig = true;
        mario.width = 70;
        mario.height = 70;
        break;
      case "red":
        marioFire = true;
        marioWater = false;
        marioFireTimer = 0;
        break;
      case "blue":
        marioWater = true;
        marioFire = false;
        marioWaterTimer = 0;
        break;
      case "star":
        marioStar = true;
        starTimer = 100;
        marioBig = true;
        mario.width = 90;
        mario.height = 100;
        mario.speed = 10;
        break;
    }
  }

  function updateBowser() {
    if (!bowserAlive) return; // ✅ Stop Bowser actions after defeat

    // Movement
    if (!bowserHitBack) {
      if (bowser.x > mario.x) bowser.x -= 5; // 🔴 Faster Bowser
      else if (bowser.x < mario.x) bowser.x += 5;
    } else {
      bowser.x += 8;
      bowserBackTimer++;
      if (bowserBackTimer > 60) {
        bowserHitBack = false;
        bowserBackTimer = 0;
      }
    }

    // ✅ Prevent Bowser from leaving screen bounds
    bowser.x = Math.max(0, Math.min(WIDTH - bowser.width, bowser.x));

    // Fireball attack
    bowserFireTimer++;
    if (bowserFireTimer >= 120 && Math.abs(bowser.x - mario.x) < 600) {
      bowserFireballs.push({
        x: bowser.x,
        y: bowser.y + 30,
        width: 25,
        height: 10,
      });
      bowserFireTimer = 0;
    }

    // Invincibility
    if (!bowserInvincible && Math.random() < 0.002) {
      bowserInvincible = true;
      bowserInvincibleTimer = 120;
    }
    if (bowserInvincible) {
      bowserInvincibleTimer--;
      if (bowserInvincibleTimer <= 0) bowserInvincible = false;
    }

    // Fireball update
    bowserFireballs.forEach((bfb, i) => {
      bfb.x -= 8;
      ctx.fillStyle = "orange";
      ctx.fillRect(bfb.x, bfb.y, bfb.width, bfb.height);
      if (collides(bfb, mario)) {
        if (!marioStar) marioHealth -= marioShielded ? 2 : 5;
        bowserFireballs.splice(i, 1);
      } else if (bfb.x + bfb.width < 0) {
        bowserFireballs.splice(i, 1);
      }
    });

    // Falling spikes
    if (!bowserJumping && Math.random() < 0.0025) {
      bowserJumping = true;
      bowserJumpTimer = 60;
      bowser.y -= 50;
    }
    if (bowserJumping) {
      bowserJumpTimer--;
      if (bowserJumpTimer <= 0) {
        bowserJumping = false;
        bowser.y = GROUND_Y;
        fallingSpikes.push({
          x: bowser.x + bowser.width / 2,
          y: 0,
          width: 20,
          height: 40,
        });
      }
    }

    // Random spikes
    if (Math.random() < 0.015) {
      fallingSpikes.push({
        x: 100 + Math.random() * 1000,
        y: 0,
        width: 20,
        height: 40,
      });
    }

    fallingSpikes.forEach((s, i) => {
      s.y += 7;
      ctx.fillStyle = "gray";
      ctx.fillRect(s.x, s.y, s.width, s.height);
      if (collides(s, mario)) {
        marioHealth -= 7;
        fallingSpikes.splice(i, 1);
      } else if (s.y > HEIGHT) fallingSpikes.splice(i, 1);
    });

    // Heal Bowser slightly
    if (bowserHealth < 150 && Math.random() < 0.002) {
      bowserHealth = Math.min(600, bowserHealth + 30);
    }
  }
  function checkGameState() {
    if (bowserHealth <= 0 && bowserAlive) {
      bowserAlive = false;
      finalBattleMusic.pause();
      finalBattleMusic.currentTime = 0; // ✅ rewind it
      finalBattleMusicPlaying = false;
    }

    if (marioHealth <= 0 && bowserAlive) {
      gameOver = true;
      finalBattleMusic.pause();
      finalBattleMusicPlaying = false;
      gameOverSound.play();
      ctx.fillStyle = "black";
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = "red";
      ctx.font = "40px Comic Sans MS";
      const gameOverText = "💀 Game Over - Bowser Wins! Press R to restart...";
      const textWidth = ctx.measureText(gameOverText).width;
      ctx.fillText(gameOverText, (WIDTH - textWidth) / 2, HEIGHT / 2);
    }

    // Add the restart logic here
    if (gameOver && (keys["r"] || keys["R"])) {
      // Reset game state variables
      marioHealth = 500;
      bowserHealth = 600;
      mario.x = 50;
      mario.y = GROUND_Y;
      mario.width = 40;
      mario.height = 60;
      marioHitCooldown = 0;
      bowserAlive = true;
      gameOver = false;
      finalBattleMusicPlaying = false;
      bowserFireballs = [];
      fallingSpikes = [];
      powerups = [];
      flagReached = false;
      // Reset any other necessary variables here

      // Restart the game loop
      gameLoop();
    }
  }
  

  function showFlagWin() {
    // ✅ When Mario reaches the flag and Bowser is already defeated
    if (!flagReached && collides(mario, flag) && !bowserAlive) {
      flagReached = true;
      gameWon = true;
      animationTimer = 0;

      // 🛑 Stop final battle music NOW
      if (finalBattleMusicPlaying) {
        finalBattleMusic.pause();
        finalBattleMusic.currentTime = 0;
        finalBattleMusicPlaying = false;
      }

      // ▶️ Start level complete music
      levelCompleteMusic.play();
    }

    // 🟡 Show "Level 3 Complete!" during levelCompleteMusic
    if (flagReached && !showCongratsScreen) {
      animationTimer++;

      ctx.fillStyle = "black";
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = "gold";
      ctx.font = "60px Comic Sans MS";
      ctx.fillText("🎉 Level 3 Complete!", WIDTH / 2 - 250, HEIGHT / 2);
    }
  }

  function gameLoop() {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);

    if (!finalBattleMusicPlaying && !gameOver && !flagReached) {
      finalBattleMusic.loop = true;
      finalBattleMusic.play();
      finalBattleMusicPlaying = true;
    }

    // Background
    ctx.drawImage(bg3, 0, 0, canvas.width, canvas.height);

    // Movement
    if (keys["arrowleft"]) mario.x -= mario.speed;
    if (keys["arrowright"]) mario.x += mario.speed;
    if (keys["arrowup"] && mario.y === GROUND_Y) mario.vy = -13; // 🟢 Higher jump

    // Physics
    mario.vy += 0.5;
    mario.y += mario.vy;
    if (mario.y > GROUND_Y) {
      mario.y = GROUND_Y;
      mario.vy = 0;
    }
    mario.x = Math.max(0, Math.min(WIDTH - mario.width, mario.x));

    // Deploy powerups (only if Bowser is alive)
    if (bowserAlive) {
      ["f", "w", "g", "s"].forEach((key) => {
        if (keys[key] && !firedPowerupKeys[key]) {
          powerups.push({
            type:
              key === "f"
                ? "red"
                : key === "w"
                ? "blue"
                : key === "g"
                ? "green"
                : "star",
            x: mario.x,
            y: 0,
            width: 30,
            height: 30,
          });
          firedPowerupKeys[key] = true;
        }
      });
    }

    // Shooting
    if (keys[" "] && !marioStar) {
      if (marioFire && marioFireTimer < FIRE_WATER_DURATION) {
        fireballsMario.push({
          x: mario.x + mario.width,
          y: mario.y + mario.height / 2,
          width: 20,
          height: 10,
        });
      } else if (marioWater && marioWaterTimer < FIRE_WATER_DURATION) {
        waterballsMario.push({
          x: mario.x + mario.width,
          y: mario.y + mario.height / 2,
          width: 20,
          height: 10,
        });
      }
    }

    // Fireballs
    fireballsMario.forEach((fb, i) => {
      fb.x += 10;
      ctx.fillStyle = "orange";
      ctx.fillRect(fb.x, fb.y, fb.width, fb.height);
      if (collides(fb, bowser) && bowserAlive && !bowserInvincible) {
        bowserHealth -= FIRE_DAMAGE;
        bowserHitBack = true;
        bowserBackTimer = 0;
        fireballsMario.splice(i, 1);
      }
    });

    waterballsMario.forEach((wb, i) => {
      wb.x += 12;
      ctx.fillStyle = "deepskyblue";
      ctx.fillRect(wb.x, wb.y, wb.width, wb.height);
      if (collides(wb, bowser) && bowserAlive && !bowserInvincible) {
        bowserHealth -= WATER_DAMAGE;
        bowserHitBack = true;
        bowserBackTimer = 0;
        waterballsMario.splice(i, 1);
      }
    });

    // Powerups
    powerups.forEach((p, i) => {
      p.y += 3;
      let img =
        p.type === "red"
          ? redMushroomImg
          : p.type === "blue"
          ? blueMushroomImg
          : p.type === "green"
          ? greenMushroomImg
          : starImg;
      ctx.drawImage(img, p.x, p.y, p.width, p.height);
      if (collides(p, mario)) {
        handlePowerup(p.type);
        powerups.splice(i, 1);
      }
    });

    // Star-powered Mario collides with Bowser
    if (
      bowserAlive &&
      !bowserInvincible &&
      marioStar &&
      collides(mario, bowser)
    ) {
      bowserHealth -= STAR_DAMAGE;
      bowserHitBack = true;
      bowserBackTimer = 0;
    }

    // Regular Bowser hit on Mario (with cooldown)
    if (bowserAlive && collides(mario, bowser) && marioHitCooldown === 0) {
      if (!marioInvincible) {
        marioHealth -= marioShielded ? 1 : 2;
        marioHitCooldown = 60;

        // ✅ Push Bowser slightly back after hitting Mario
        if (bowser.x > mario.x) {
          bowser.x += 30; // move right if to Mario’s right
        } else {
          bowser.x -= 30; // move left if to Mario’s left
        }
      }
    }

    if (marioHitCooldown > 0) marioHitCooldown--;

    // Draw Characters
    ctx.drawImage(marioImg, mario.x, mario.y, mario.width, mario.height);
    if (bowserAlive)
      ctx.drawImage(bowserImg, bowser.x, bowser.y, bowser.width, bowser.height);

    // UI
    drawHealthBar(50, 30, 500, 20, marioHealth / 500, "Mario");
    drawHealthBar(850, 30, 500, 20, bowserHealth / 600, "Bowser");

    // Update logic
    updateBowser();
    checkGameState();

    // Draw Flag
    if (!flagReached && !bowserAlive)
      ctx.drawImage(flagImg3, flag.x, flag.y, flag.width, flag.height);

    // Victory logic
    showFlagWin();
    // ✅ Wait for levelCompleteMusic to finish, then show Congratulations
    if (flagReached && !showCongratsScreen) {
      if (
        levelCompleteMusic.ended ||
        levelCompleteMusic.currentTime >= levelCompleteMusic.duration
      ) {
        showCongratsScreen = true;
        startCongratsScreen();
      }
    }

    // Power-up timers
    if (marioShielded) {
      shieldTimer--;
      if (shieldTimer <= 0) marioShielded = false;
    }
    if (marioInvincible) {
      invincibleTimer--;
      if (invincibleTimer <= 0) {
        marioInvincible = false;
        marioBig = false;
        mario.width = 40;
        mario.height = 60;
      }
    }
    if (marioFire) marioFireTimer++;
    if (marioWater) marioWaterTimer++;
    if (marioStar) {
      starTimer--;
      if (starTimer <= 0) {
        marioStar = false;
        marioBig = false;
        mario.width = 40;
        mario.height = 60;
        mario.speed = 5;
      }
    }

    // Next frame
    if (!gameOver && !showCongratsScreen) {
      requestAnimationFrame(gameLoop);
    }
  }
  function startCongratsScreen() {
    winSound.play();

    function drawCongratsFrame() {
      ctx.clearRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = "black";
      ctx.fillRect(0, 0, WIDTH, HEIGHT);

      if (congratsFrameTimer < 180) {
        // Show Peach, Toad and Mario for 3 seconds
        ctx.drawImage(
          princessPeachImg,
          WIDTH / 2 - 60,
          HEIGHT / 2 - 60,
          40,
          40
        );
        ctx.drawImage(toadImg, WIDTH / 2 + 20, HEIGHT / 2 - 60, 40, 40);
        ctx.drawImage(
          marioImg,
          WIDTH / 2 - 20,
          HEIGHT / 2,
          mario.width,
          mario.height
        );
      }

      ctx.fillStyle = "white";
      ctx.font = "60px Comic Sans MS";
      ctx.fillText("🎉Congratulations🎉!", WIDTH / 2 - 270, HEIGHT / 2 + 100);

      // 🟥 Removed restart instruction text
      // ctx.font = "30px Comic Sans MS";
      // ctx.fillText("Press R to Restart", WIDTH / 2 - 130, HEIGHT / 2 + 150);

      congratsFrameTimer++;

      // After ~5 seconds (300 frames at 60fps), go to ending
      if (congratsFrameTimer < 300) {
        requestAnimationFrame(drawCongratsFrame);
      } else {
        window.location.href = "../ending/ending.html"; // ⬅ Go to your final animation
      }
    }

    requestAnimationFrame(drawCongratsFrame);
  }  

  // 🚀 Start the game
  gameLoop();
}
