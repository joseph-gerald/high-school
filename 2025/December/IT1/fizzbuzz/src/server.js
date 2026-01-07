const RANGE_MAX = 1000;

let players = [];
let clients = [];

let gameState = {
    num: null
}

function fizzbuzz(n) {
    const div3 = n % 3 == 0;
    const div5 = n % 5 == 0;

    if (div3 && div5) return "fb";
    if (div3) return "f";
    if (div5) return "b";

    return "n";
}

function generateRandomFizzBuzz(max) {
    let n = -1;

    while (fizzbuzz(n) == "n") {
        n = Math.floor(Math.random() * max) + 1;
    }

    return n;
}

function randomizeQuestion() {
    const num = generateRandomFizzBuzz(RANGE_MAX);

    gameState.num = num
    gameState.answer = fizzbuzz(num)
}

randomizeQuestion();

function broadcast(type, data) {
    for (const player of players) {
        player.send(type, data);
    }
}

function handleConnection(client, request) {
    const headers = request.headers;

    clients.push(client);

    function getPosition() {
        return clients.indexOf(client);;
    }

    function onClose() {
        console.log(`Connection Closed`);

        const position = getPosition();

        clients.splice(position, 1);
        players.splice(position, 1);
    }

    function send(type, data) {
        client.send(JSON.stringify({
            type,
            data
        }));
    }

    players.push({ client, send, score: 0 });
    gameState.players = players;

    function onMessage(data) {
        if (data.indexOf("keepalive") == 0) {
            const count = data.split("/")[1];

            if (isNaN(parseInt(count))) throw Error("Invalid Keepalive");
            return;
        }

        const player = players[getPosition()];

        try {
            data = JSON.parse(data);
        } catch (e) {
            return
        }

        switch (data.type) {
            case "init":
                player.name = data.data.name;

                broadcast("update", gameState);
                break;
            case "answer":
                console.log(data, gameState)
                if (data.data == gameState.answer) {
                    randomizeQuestion();

                    player.score += 1;

                    broadcast("update", gameState);
                } else {
                    broadcast("update", gameState);
                    player.score -= 2;
                }
                break;
        }
    }

    client.on('message', data => {
        try {
            onMessage(data.toString())
        } catch (error) {
            client.close();
            console.log(error)
        }
    });

    client.on('close', onClose);
}

module.exports = handleConnection;