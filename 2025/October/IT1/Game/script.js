const [
    toggleModeButton,
    toggleLeaderboardButton,
    game,
    randomizeButton
] = [
        document.getElementById("toggle-mode"),
        document.getElementById("toggle-leaderboard"),
        document.getElementById("game"),
        document.getElementById("randomize")
    ];

const options = Array.from(document.querySelectorAll("#options > button"));
let correctIndex = -1;
let streak = -1;

toggleLeaderboardButton.onclick = () => {
    document.body.classList.toggle("hide-leaderboard")
}

function rand(range) {
    return Math.floor(Math.random() * (range ?? 256))
}

function getRandomColour() {
    return [rand(), rand(), rand()];
}

function getRandomColourString() {
    return getRandomColour().join(", ");
}

function randomize() {
    const colours = [getRandomColourString(), getRandomColourString(), getRandomColourString()];
    correctIndex = rand(3);

    if (streak == -1) streak = 0;

    game.style.background = `rgb(${colours[correctIndex]})`

    for (const [index, colour] of Object.entries(colours)) {
        const isAnswer = correctIndex == index;
        const elm = options[index];

        elm.innerHTML = `rgb(${colour})`;
        elm.style.background = "var(--background)";

        elm.onclick = () => {
            if (isAnswer) {
                options.filter(x => x != elm).forEach(option => {
                    option.style.background = "#CC3030";
                });
                
                elm.style.background = "#30AC30";
                if (streak != -1) {
                    streak++;

                }
            } else {
                elm.style.background = "#CC3030";
                if (streak != -1) streak = -1;
            }
        }
    }
}


randomizeButton.onclick = randomize;

randomize()