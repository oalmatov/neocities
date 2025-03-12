export const Direction = {
    RIGHT: true,
    LEFT: false,
};

export function toBoolDirection(direction) {
    return direction === 1;
}

export function toNumDirection(direction) {
    return direction ? 1 : -1;
}

export function isWithinRadius(x1, y1, x2, y2, radius) {
    const distance = Math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);
    return distance <= radius && distance >= -radius;
}
