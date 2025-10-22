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
    }

    if (streakToSave <= 0) {
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
                if (streak != -1) {
                    streak++;
                }
            } else {
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