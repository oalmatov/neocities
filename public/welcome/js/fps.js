export class FPSManager {
    static PERIOD = 8000;

    constructor(fps) {
        this.lastTime = 0;
        this.fps = fps
    }

    get interval() {
        return FPSManager.PERIOD / this.fps;
    }

    shouldUpdate(currTime) {
        const elapsedTime = currTime - this.lastTime;
        if (elapsedTime > this.interval) {
            this.lastTime = currTime - (elapsedTime % this.interval);
            return true;
        }
        return false;
    }
}
