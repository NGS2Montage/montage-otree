var app = {
    user: {},
    friends: [],
    chats: [],
    newChat: "",
    successWords: [],
    countDict: {},
    requests: [],
    subscribed: false,
    letters: {},
    wordError: "",
    wordCount: "",
    sentWord: "",
}

var channel = varsFromDjango.channel;
var participantCode = varsFromDjango.participant_code;
var wordChannel = varsFromDjango.word_channel;
var transactionChannel = varsFromDjango.transaction_channel;


//////////////////////////////////////////////////////////////
// rivets init
//////////////////////////////////////////////////////////////
rivets.bind(document.getElementById('app-view'), {app: app});
rivets.binders.addclass = function(el, value){
	if (el.addedClass){
		$(el).removeClass(el.addedClass);
		delete el.addedClass;
	}
	if (value){
		$(el).addClass(value);
		el.addedClass = value;
	}
}

app.user = new User(varsFromDjango.nickname);

//////////////////////////////////////////////////////////////
// User
//////////////////////////////////////////////////////////////
function User(username) {
    this.name = username; //+ " Group " + varsFromDjango.group;

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
        'type': 'letter_request',
        'requested_letter': model.letter.pk,
        'participant_code': participantCode,
        'channel': transactionChannel,
    };
    tSocket.send(JSON.stringify(data));
};

UserLetter.prototype.toString = function () {
    return this.letter;
};

//////////////////////////////////////////////////////////////
// LetterTransaction
//////////////////////////////////////////////////////////////
function LetterTransaction(obj) {
    console.log("makeing a new transaction", obj);
    this.letter = obj.letter;
    this.owner = obj.owner;
    this.pk = obj.pk;
    this.borrower = obj.borrower;
    this.approved = ('approved' in obj) ? obj.approved : false;
}

LetterTransaction.prototype.approve = function (event, model) {
    console.log("Need to approve this transaction yo");

    model.transaction.approved = true;

    var data = {
        'type': 'request_approved',
        'transaction_pk': model.transaction.pk,
        'participant_code': participantCode,
        'channel': transactionChannel
    };
    console.log("about to send this as approval message");
    console.log(data)
    tSocket.send(JSON.stringify(data));
}

LetterTransaction.prototype.toString = function () {
    return this.letter;
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
    	  var output = [];
    	  var wordClass = {};
        for (var i = 0; i < message.words.length; i++) {
            var newWord = message.words[i].toUpperCase();
            if (newWord in app.countDict){
            	app.countDict[newWord] += 1;
            } else {
            	app.countDict[newWord] = 1;
            }
            wordClass[newWord] = ((newWord == app.sentWord) ? 'word-sent' : 'word-new');
        }
        var keys = Object.keys(app.countDict);
        keys.sort();
        for (var i=0, len=keys.length; i < len; i++){
        		var key = keys[i];
            output.push({
            	'id': 'word-'+key,
            	'class': ((key in wordClass) ? wordClass[key] : 'word'),
            	'word': key,
            	'freq': app.countDict[key],
            });
        }
        app.successWords = output;
        app.wordCount = output.length;
        
        if (!(app.sentWord == "")){
        		el = $(".word-sent");
        		el.css({backgroundColor: '#00ffcc'})
        		.goTo(el.animate({backgroundColor: '#EEEEEE'},750))
        		.removeClass(".word-sent");
        		app.sentWord = "";
        	} else {
        		el = $(".word-new");
        		el.css({backgroundColor: 'orange'})
        		.animate({backgroundColor: '#EEEEEE'},750)
        		.removeClass(".word-new");
        		app.sentWord = "";
        	}
    }
};

socket.onopen = function () {
    console.log("Connected to words socket");
    // clear message history so we can re-populate
    app.successWords = [];
    app.countDict = {};
};

socket.onclose = function () {
    console.log("Disconnected from words socket");
};

function sendWord() {
    var body = $wordsInput.val();
    if (!body) {
        return;
    }
    app.sentWord = $wordsInput.val().toUpperCase();
    var data = {
        'word': $wordsInput.val().toLowerCase(),
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

    if (message.type === "request_success") {
        message.requested_letters.forEach(function (transaction) {
            app.user.transactions.push(new LetterTransaction(transaction));
        });
    }

    if (message.type === "error") {
        app.transactionError = message.msg;
    } else {
        app.transactionError = '';
    }

    if (message.type === "new_transaction") {
        message.requested_letters.forEach(function (transaction) {
            app.requests.push(new LetterTransaction(transaction));
        });
    }

    if (message.type === "transaction_approved") {
        var transaction = app.user.transactions.find(function (transaction) {
            return transaction.pk === message.transaction_pk;
        });

        if (transaction) {
            transaction.approved = true;
        }
    }
};

tSocket.onopen = function () {
    console.log("Connected to transaction tSocket");
    // clear message history so we can re-populate
    app.requests = [];
    app.user.transactions = [];
};

tSocket.onclose = function () {
    console.log("Disconnected from transaction tSocket");
};
