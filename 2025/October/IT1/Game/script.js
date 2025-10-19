const [
    toggleModeButton,
    toggleLeaderboardButton
] = [
    document.getElementById("toggle-mode"),
    document.getElementById("toggle-leaderboard"),
];

toggleLeaderboardButton.onclick = () => {
    document.body.classList.toggle("hide-leaderboard")
}