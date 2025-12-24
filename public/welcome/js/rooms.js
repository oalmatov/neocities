import { isWithinRadius } from './helpers.js';

class Room {
    static ENTER_KEY = "e";

    constructor(x, y, radius, href) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.href = href;
    }

    enter() {
        window.location.href = this.href;
    }

    canEnter(x, y) {
        return isWithinRadius(x, y, this.x, this.y, this.radius);
    }
}

export class Yurt extends Room {
    constructor(x, y, radius, href, id) {
        super(x, y, radius, href);
        this.message = document.getElementById(id);
        this.message.style.display = "none";
    }

    displayMessage() {
        this.message.style.display = "block";
    }

    hideMessage() {
        this.message.style.display = "none";
    }

    render(player) {
        if (this.canEnter(player.x, player.y)) {
            this.displayMessage();
        } else {
            this.hideMessage();
        }
    }
}

