import { lvl1Qs, lvl2Qs, lvl3Qs } from './levels.js';

const lvl1Btn = document.getElementById("lvl1-btn");
const lvl2Btn = document.getElementById("lvl2-btn");
const lvl3Btn = document.getElementById("lvl3-btn");
const currCardContainer = document.getElementById("curr-card-container");
const prevCardsContainer = document.getElementById("prev-cards-container");

let currLvl = lvl1Qs;
const cardHistory = [];

function getRandQuestion() {
    console.log(currLvl.length);
    if (currLvl.length == 0) {
        currCardContainer.innerHTML = `<h1>no more cards from this level</h1>`;
        return null;
    } else {
        const randIdx = Math.floor(Math.random() * currLvl.length);
        const question = currLvl[randIdx];
        currLvl.splice(randIdx, 1);
        currCardContainer.innerHTML = `<h1>${question}</h1>`;
        return question;
    }
}

cardHistory.push(getRandQuestion());

lvl1Btn.addEventListener("click", () => {
    lvl1Btn.classList.add("active");
    lvl2Btn.classList.remove("active");
    lvl3Btn.classList.remove("active");
    currLvl = lvl1Qs;
    const question = getRandQuestion();
    if (question) {
        cardHistory.push(question);
        prevCardsContainer.innerHTML = cardHistory.slice(0, -1).reverse().map(card => `<div class="card"><h1>${card}</h1></div>`).join('');
    }
})

lvl2Btn.addEventListener("click", () => {
    lvl1Btn.classList.remove("active");
    lvl2Btn.classList.add("active");
    lvl3Btn.classList.remove("active");

    currLvl = lvl2Qs;
    const question = getRandQuestion();
    if (question) {
        cardHistory.push(question);
        prevCardsContainer.innerHTML = cardHistory.slice(0, -1).reverse().map(card => `<div class="card"><h1>${card}</h1></div>`).join('');
    }
})

lvl3Btn.addEventListener("click", () => {
    lvl1Btn.classList.remove("active");
    lvl2Btn.classList.remove("active");
    lvl3Btn.classList.add("active");

    currLvl = lvl3Qs;
    const question = getRandQuestion();
    if (question) {
        cardHistory.push(question);
        prevCardsContainer.innerHTML = cardHistory.slice(0, -1).reverse().map(card => `<div class="card"><h1>${card}</h1></div>`).join('');
    }
})

