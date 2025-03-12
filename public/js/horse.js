import { toBoolDirection } from "./helpers.js";

export class Horse {
    static SPEED = 3;
    static HEIGHT = 66;
    static WIDTH = 82;

    static STATE = {
        RIGHT: {
            IDLE: {
                image: (() => {
                    const img = new Image();
                    img.src = "assets/horse/horse_idle_right_cycle.png";
                    return img;
                })(),
                direction: 1,
                frameCount: 7,
            },

            RUNNING: {
                image: (() => {
                    const img = new Image();
                    img.src = "assets/horse/horse_run_right_cycle.png";
                    return img;
                })(),
                direction: 1,
                frameCount: 5,
            },
        },

        LEFT: {
            IDLE: {
                image: (() => {
                    const img = new Image();
                    img.src = "assets/horse/horse_idle_left_cycle.png";
                    return img;
                })(),
                direction: -1,
                frameCount: 7,
            },
            
            RUNNING: {
                image: (() => {
                    const img = new Image();
                    img.src = "assets/horse/horse_run_left_cycle.png";
                    return img;
                })(),
                direction: -1,
                frameCount: 5,
            }
        },
    };

    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.moving = false;
        this.frameIndex = 0;
        this.state = Horse.STATE.RIGHT.IDLE;
    }

    run(direction) {
        this.state = direction ? Horse.STATE.RIGHT.RUNNING : Horse.STATE.LEFT.RUNNING;
        this.x += Horse.SPEED * this.state.direction;
    }

    idle(direction) {
        if (direction == null) {
            direction = toBoolDirection(this.state.direction);
        }
        this.state = direction ? Horse.STATE.RIGHT.IDLE : Horse.STATE.LEFT.IDLE;
    }

    render(ctx, canvas) {
        this.frameIndex = (this.frameIndex  + 1) % this.state.frameCount;
        this.draw(ctx, canvas);
    }

    draw(ctx, canvas) {
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx.save()
        ctx.scale(0.5, 0.5)
        ctx.drawImage(
            this.state.image,
            this.frameIndex * Horse.WIDTH,
            0,
            Horse.WIDTH,
            Horse.HEIGHT,
            this.x,
            this.y,
            Horse.WIDTH,
            Horse.HEIGHT,
        )
        ctx.restore()
    }


}
