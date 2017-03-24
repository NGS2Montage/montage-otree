var app = {
    user: {},
    friends: [],
    chats: [],
    newChat: "",
    successWords: [],
    newWord: "",
    subscribed: false,
    letters: {},
    wordError: "",
}

var channel = varsFromDjango.channel;
var participantCode = varsFromDjango.participant_code;
var wordChannel = varsFromDjango.word_channel;

app.user = new User(varsFromDjango.nickname);


//////////////////////////////////////////////////////////////
// rivets init
//////////////////////////////////////////////////////////////
rivets.bind(document.getElementById('app-view'), {app: app});


//////////////////////////////////////////////////////////////
// User
//////////////////////////////////////////////////////////////
function User(username) {
    this.name = username + " Group " + varsFromDjango.group;
    // this.pk = user.pk;
    this.letters = varsFromDjango.letters[username];
    this.transactions = [];
};

app.friends = Object.keys(varsFromDjango.letters).filter(function (nickname) {
        return nickname !== varsFromDjango.nickname
    }).map(function (nickname) {
        return new User(nickname);
    });

var $wordsWidget = $('#anagrams-words-' + wordChannel);
var $wordsInput = $wordsWidget.find('input');

var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path = ws_scheme + '://' + window.location.host + "/anagrams/" + wordChannel + "/";

console.log("Connecting to " + ws_path);
var socket = new ReconnectingWebSocket(ws_path);


// Handle incoming messages
socket.onmessage = function (message) {

    console.log("Got words message ");
    var message = JSON.parse(message.data);
    console.log(message);

    if (message.type === "error") {
        app.wordError = message.msg;
    } else {
        app.wordError = '';
    }

    if (message.type === "word") {
        for (var i = 0; i < message.words.length; i++) {
            app.successWords.push(message.words[i]);
        }
    }
};

socket.onopen = function () {
    console.log("Connected to words socket");
    // clear message history so we can re-populate
    app.successWords = [];
};

socket.onclose = function () {
    console.log("Disconnected from words socket");
};

function sendWord() {
    var body = $wordsInput.val();
    if (!body) {
        return;
    }
    var data = {
        'word': $wordsInput.val(),
        'participant_code': participantCode,
        'channel': wordChannel
    };
    socket.send(JSON.stringify(data));
    $wordsInput.val('');
}

$wordsWidget.find('button').click(function(e) {
    sendWord();
});

$wordsInput.on('keypress', function (e) {
    if (e.which == 13) {
        e.preventDefault();
        sendWord();
    }
});
