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
var transactionChannel = varsFromDjango.transaction_channel;



//////////////////////////////////////////////////////////////
// rivets init
//////////////////////////////////////////////////////////////
rivets.bind(document.getElementById('app-view'), {app: app});

app.user = new User(varsFromDjango.nickname);

//////////////////////////////////////////////////////////////
// User
//////////////////////////////////////////////////////////////
function User(username) {
    this.name = username + " Group " + varsFromDjango.group;

    var letterObjs = varsFromDjango.letters[username];
    if (username === varsFromDjango.nickname) {
        this.letters = letterObjs.map(function (letter) {
            return letter.letter;
        });
    } else {
        this.letters = letterObjs.map(function (letter) {
            return new UserLetter(letter);
        });
    }

    this.transactions = [];
};

//////////////////////////////////////////////////////////////
// UserLetter
//////////////////////////////////////////////////////////////

function UserLetter(obj) {
    this.letter = obj.letter;
    this.pk = obj.pk;
}

UserLetter.prototype.requestLetter = function (event, model) {
    console.log("request a letter yo", model.letter.pk);

    var data = {
        'requested_letter': model.letter.pk,
        'participant_code': participantCode,
        'channel': transactionChannel
    };
    tSocket.send(JSON.stringify(data));

    app.user.transactions.push(new LetterTransaction({
        letter: model.letter,
        borrower: app.user,
    }));
};

UserLetter.prototype.toString = function () {
    return this.letter;
};

//////////////////////////////////////////////////////////////
// LetterTransaction
//////////////////////////////////////////////////////////////
function LetterTransaction(obj) {
    this.letter = obj.letter;
    this.pk = obj.pk;
    this.borrower = obj.borrower;
    this.approved = ('approved' in obj) ? obj.approved : false;
}

LetterTransaction.prototype.approve = function (event, model) {
    console.log("Need to approve this transaction yo");
    // msg = {
    //   stream: "lettertransactions",
    //   payload: {
    //     action: "update",
    //     pk: model.transaction.pk,
    //     data: {
    //         borrower: model.transaction.borrower,
    //         letter: model.transaction.letter.pk,
    //         approved: true,
    //     }
    //   }
    // };

    // socket.send(JSON.stringify(msg));
}

LetterTransaction.prototype.toString = function () {
    return this.letter.toString();
};


//////////////////////////////////////////////////////////////
// Startup
//////////////////////////////////////////////////////////////

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


////////////////////////////////////////////////////////////////////////
// TRANSACTION CHANNEL WEBSOCKET STUFF
////////////////////////////////////////////////////////////////////////
var ws_path = ws_scheme + '://' + window.location.host + "/transactions/" + transactionChannel + "/";

console.log("Connecting to " + ws_path);
var tSocket = new ReconnectingWebSocket(ws_path);


// Handle incoming messages
tSocket.onmessage = function (message) {

    console.log("Got transaction message ");
    var message = JSON.parse(message.data);
    console.log(message);

    // if (message.type === "error") {
    //     app.wordError = message.msg;
    // } else {
    //     app.wordError = '';
    // }

    // if (message.type === "word") {
    //     for (var i = 0; i < message.words.length; i++) {
    //         app.successWords.push(message.words[i]);
    //     }
    // }
};

tSocket.onopen = function () {
    console.log("Connected to transaction tSocket");
    // clear message history so we can re-populate
};

tSocket.onclose = function () {
    console.log("Disconnected from transaction tSocket");
};

// function sendWord() {
//     var body = $wordsInput.val();
//     if (!body) {
//         return;
//     }
//     var data = {
//         'word': $wordsInput.val(),
//         'participant_code': participantCode,
//         'channel': wordChannel
//     };
//     tSocket.send(JSON.stringify(data));
//     $wordsInput.val('');
// }

// $wordsWidget.find('button').click(function(e) {
//     sendWord();
// });

// $wordsInput.on('keypress', function (e) {
//     if (e.which == 13) {
//         e.preventDefault();
//         sendWord();
//     }
// });
