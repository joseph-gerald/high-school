const [
    toggleModeButton,
    toggleLeaderboardButton,
    game,
    randomizeButton,
    leaderboard,
    nameInput,
    saveButton,
    question
] = [
        document.getElementById("toggle-mode"),
        document.getElementById("toggle-leaderboard"),
        document.getElementById("game"),
        document.getElementById("randomize"),
        document.getElementById("leaderboard"),
        document.getElementById("name"),
        document.getElementById("save"),
        document.getElementById("spørsmål")
    ];

const BUTTON_ALTS = {
    "RANDOMIZE": `
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-dices-icon lucide-dices">
                        <rect width="12" height="12" x="2" y="10" rx="2" ry="2" />
                        <path d="m17.92 14 3.5-3.5a2.24 2.24 0 0 0 0-3l-5-4.92a2.24 2.24 0 0 0-3 0L10 6" />
                        <path d="M6 18h.01" />
                        <path d="M10 14h.01" />
                        <path d="M15 6h.01" />
                        <path d="M18 9h.01" />
                    </svg>

                    Ny Farge`,
    "WAIT": `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-mouse-pointer-click-icon lucide-mouse-pointer-click">
                        <path d="M14 4.1 12 6" />
                        <path d="m5.1 8-2.9-.8" />
                        <path d="m6 12-1.9 2" />
                        <path d="M7.2 2.2 8 5.1" />
                        <path
                            d="M9.037 9.69a.498.498 0 0 1 .653-.653l11 4.5a.5.5 0 0 1-.074.949l-4.349 1.041a1 1 0 0 0-.74.739l-1.04 4.35a.5.5 0 0 1-.95.074z" />
                    </svg>

                    Start ved å velge en av fargene`,
    "GAME_OVER": `
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-heart-crack-icon lucide-heart-crack"><path d="M12.409 5.824c-.702.792-1.15 1.496-1.415 2.166l2.153 2.156a.5.5 0 0 1 0 .707l-2.293 2.293a.5.5 0 0 0 0 .707L12 15"/><path d="M13.508 20.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5a5.5 5.5 0 0 1 9.591-3.677.6.6 0 0 0 .818.001A5.5 5.5 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5z"/></svg>

                    Du tapte, plis lagre scoren din!`
}

const COLOUR_CORRECT = "#26AC26";
const COLOUR_FAIL = "#CC2020";

const options = Array.from(document.querySelectorAll("#options > button"));
let correctIndex = -1;
let streak = -1;
let streakToSave = 0;
let mode = "CTR"; // RTC = RGB TO COLOUR    CTR = COLOUR TO RGB

// leaderboard data/utils

let leaderboardData = [];

if (localStorage.getItem('leaderboard')) {
    leaderboardData = JSON.parse(localStorage.getItem('leaderboard'));
} else {
    leaderboardData = [
        { name: "Joe", streak: 999 }
    ];
}

toggleLeaderboardButton.onclick = () => {
    document.body.classList.toggle("hide-leaderboard")
}

function loadLeaderboard() {
    leaderboardData.sort((a, b) => b.streak - a.streak);

    leaderboard.innerHTML = "";

    for (const [index, entry] of leaderboardData.entries()) {
        const row = document.createElement('tr');
        const newRow = document.createElement('tr');
        const rankCell = document.createElement('td');
        const nameCell = document.createElement('td');
        const streakCell = document.createElement('td');

        rankCell.innerText = index + 1;
        nameCell.innerText = entry.name;
        streakCell.innerText = entry.streak;

        row.appendChild(rankCell);
        row.appendChild(nameCell);
        row.appendChild(streakCell);

        leaderboard.appendChild(row);
    }
}

function pushLeaderboard() {
    const name = nameInput.value.trim().substring(0, 20);

    if (name.length == 0) {
        alert("Navn må være litt lengre plis");
        return;
    }

    if (streak != -1) {
        alert("Du må spille ferdig først plis");
    } else if (streakToSave <= 0) {
        alert("Streak må være litt større plis");
        return;
    }

    leaderboardData.push({ name, streak: streakToSave });
    loadLeaderboard();

    localStorage.setItem('leaderboard', JSON.stringify(leaderboardData));

    streak = 0;

    randomize();
}

saveButton.onclick = pushLeaderboard;




// spill logikk


function rand(range) {
    // hvis range er null eller undefined, bruk 256
    return Math.floor(Math.random() * (range ?? 256))
}

// generer en random rgb-farge (3 bytes)
function getRandomColour() {
    return [rand(), rand(), rand()];
}

// bruk getRandomColour og join til r, g, b format
function getRandomColourString() {
    return getRandomColour().join(", ");
}

function randomize() {
    loadLeaderboard();

    randomizeButton.innerHTML = BUTTON_ALTS.WAIT;
    randomizeButton.disabled = true;

    // tre farger for valgene
    const colours = [getRandomColourString(), getRandomColourString(), getRandomColourString()];
    correctIndex = rand(3); // velg hvilken farge som er riktig

    if (streak == -1) {
        streak = 0;
    }

    if (mode == "RTC") {
        game.style.background = `var(--border)`;
        question.innerText = `rgb(${colours[correctIndex]})`;
    } else {
        game.style.background = `rgb(${colours[correctIndex]})`;
    }

    for (const [index, colour] of Object.entries(colours)) {
        const isAnswer = correctIndex == index;
        const elm = options[index];

        elm.style.filter = "none";

        if (mode == "RTC") {
            elm.innerText = "-";
            elm.style.background = `rgb(${colour})`;
        } else {
            elm.innerHTML = `rgb(${colour})`;
            elm.style.background = "var(--background)";
        }
        elm.disabled = false;

        elm.onclick = () => {
            // farge alle knappene og deaktiver dem etter svar
            options.forEach(option => {
                const isAnswer = option == options[correctIndex];

                if (mode == "RTC") {
                    option.innerText = isAnswer ? "RIKTIG" : "FEIL";
                    option.style.filter = isAnswer ? "brightness(100%)" : "brightness(30%)";
                    option.disabled = true;
                } else {
                    option.style.background = isAnswer ? COLOUR_CORRECT : COLOUR_FAIL;
                    option.disabled = true;
                }
            });

            if (isAnswer) {
                randomizeButton.innerHTML = BUTTON_ALTS.RANDOMIZE;
                randomizeButton.disabled = false;

                if (streak != -1) {
                    streak++;
                }
            } else {
                if (streak > 0) {
                    randomizeButton.innerHTML = BUTTON_ALTS.GAME_OVER;
                } else {
                    randomizeButton.innerHTML = BUTTON_ALTS.RANDOMIZE;
                    randomizeButton.disabled = false;
                }

                if (streak != -1) {
                    streakToSave = streak;
                    streak = -1;
                }
            }
        }
    }
}

toggleModeButton.onclick = () => {
    mode = mode == "RTC" ? "CTR" : "RTC";

    if (mode == "RTC") {
        question.style.fontSize = "5rem";
    } else {
        question.style.fontSize = "0rem";
    }

    randomize();
}

// hook knappen til randomize functionen
randomizeButton.onclick = randomize;

// init
randomize()