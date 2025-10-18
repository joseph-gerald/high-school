function getCard(cardIndex) {
    switch (cardIndex) {
        case 14:
            return "A";
        case 13:
            return "K";
        case 12:
            return "Q";
        case 11:
            return "J";
        default:
            return cardIndex;
    }
}

suits = ["C", "H", "S", "D"];1

cards = [];

for (const suit of suits) {
    for (let i = 1; i <= 14; i++) {
        cards.push([getCard(i), suit]);
    }
}

cards = cards.sort(x => 0.5 - Math.random())
console.log(cards);