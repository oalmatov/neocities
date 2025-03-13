class LevelList {
    constructor(levels) {
        this.head = null;
        this.tail = null;

        levels.forEach((level) => {
            this.append(level);
        })
    }

    append(level) {
        if (this.head == null && this.tail == null) {
            this.head = level;
            this.tail = level;
        } else {
            this.tail.next = level;
            level.prev = this.tail;
            this.tail = this.tail.next;
        }
    }

    peek() {
        return this.head;
    }
}


class Level {
    constructor(src) {
        this.src = src;
        this.prev = null;
        this.next = null;
    }
}


export class LevelManager {
    static LEFT_EDGE = -50;
    static RIGHT_EDGE = 250;

    static LEVELS = new LevelList([
        new Level("assets/steppe_bg.png"),
        new Level("assets/beach.jpeg"),
    ]);

    constructor() {
        this.level = LevelManager.LEVELS.peek();
        this.bg = document.getElementById("bg");
    }

    render(horse, canvas) {
        if (horse.x > canvas.width + LevelManager.RIGHT_EDGE && this.level.next != null) {
            this.level = this.level.next;
            horse.x = LevelManager.LEFT_EDGE;
            this.bg.src = this.level.src;
            return;
        }

        if (horse.x < LevelManager.LEFT_EDGE && this.level.prev != null) {
            this.level = this.level.prev;
            horse.x = canvas.width + LevelManager.RIGHT_EDGE;
            this.bg.src = this.level.src;
        }
    }
}
