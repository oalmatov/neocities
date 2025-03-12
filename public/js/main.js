import { Horse } from './horse.js';
import { Yurt } from './rooms.js';
import { Direction } from './helpers.js';
import { FPSManager } from './fps.js';
import { LevelManager } from './levels.js';

const canvas = document.getElementById("steppe");
const ctx = canvas.getContext("2d");

const levelManager = new LevelManager();
const fpsManager = new FPSManager(60);
const horse = new Horse(canvas.width * 0.3, canvas.height * 1.2);
const yurt = new Yurt(320, 120, 75, "/yurt", "yurt-message");

window.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
        const direction = (e.key === "ArrowRight") === Direction.RIGHT;
        horse.run(direction);
    }

    if ((e.key === "e" || e.key === "E") && yurt.canEnter(horse.x, horse.y)) {
        horse.idle();
        yurt.enter();
    }
});

window.addEventListener("keyup", (e) => {
    if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
        const direction = (e.key === "ArrowRight") === Direction.RIGHT;
        horse.idle(direction);
    }
});


function update(time) {
    requestAnimationFrame(update)
    if (fpsManager.shouldUpdate(time)) {
        horse.render(ctx, canvas);
        yurt.render(horse);
        levelManager.render(horse, canvas);
    }
}

update();
