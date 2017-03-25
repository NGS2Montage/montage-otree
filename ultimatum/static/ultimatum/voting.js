var app = {
    votes: {},
    votedOn: []
};


rivets.bind(document.getElementById('vote-view'), {app: app});


var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path = ws_scheme + '://' + window.location.host + "/votes/" + channel + "/";

console.log("Connecting to " + ws_path);
var socket = new ReconnectingWebSocket(ws_path);


// Handle incoming messages
socket.onmessage = function (message) {

    console.log("Got voting message ");
    var message = JSON.parse(message.data);
    console.log(message);

    if (message.type === "error") {
        app.voteError = message.msg;
    } else {
        app.voteError = '';
    }

    if (message.type === "vote") {
        for (var i = 0; i < message.votes.length; i++) {
            app.votes.push(message.votes[i]);
        }
    }
};

socket.onopen = function () {
    console.log("Connected to votes socket");
    // clear message history so we can re-populate
    app.votes = [];
};

socket.onclose = function () {
    console.log("Disconnected from votes socket");
};

function sendVote(neighborId, userId, voteUp) {
    if (app.votedOn.indexOf(neighborId) !== -1) {
        return;
    }

    app.votedOn.push(neighborId);

    var data = {
        'neighbor_id': neighborId,
        'participant_code': participantCode,
        'channel': channel,
        'voteUp': voteUp,
    };
    socket.send(JSON.stringify(data));
}
