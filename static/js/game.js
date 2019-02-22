$(document).ready(function() {
    let path = window.location.pathname.split('/');
    let game = {
        id: path[path.indexOf('game') + 1]
    }

    let scheme = window.location.protocol == "https:" ? "wss" : "ws";
    let socket = new ReconnectingWebSocket(scheme + '://' + window.location.host + "/codenamez/game/");

    // Handle incoming messages
    socket.onmessage = function (response) {
        // Decode the JSON
        console.log("Got websocket message " + response.data);
        var response = JSON.parse(response.data);
        // Handle errors
        if (response.error) {
            return Error.display(response.error);
        }

        if (response.join) {
            let data = response.join;
            let $main = $("main").empty();
            let $gameWrapper = $("<div>", { class: "gameWrapper" });
            let $colLeft = $("<section>", { class: "col-l" }).appendTo($gameWrapper);
            let $colBoard = $("<section>", { class: "col-board" }).appendTo($gameWrapper);
            let $colRight = $("<section>", { class: "col-r" }).appendTo($gameWrapper);

            let $board = $("<ul>", { class: "board" }).appendTo($colBoard);
            let game = JSON.parse(data.game);
            let players = JSON.parse(data.players);
            
            let gameData = JSON.parse(game[0].fields.data);
            let cards = gameData.cards;
            let moves = gameData.moves[gameData.moves.length-1];
            let isSpymaster = Game.Spymaster.isSpymaster(gameData, data.user);
            for (let i in cards) {
                let $card = $("<li>", { class: "card" }).addClass(Game.Cards.getTypeAsClass(cards[i].type)).appendTo($board);
                let $flipCard = $("<div>", { class: "flip-card" }).appendTo($card);
                if (moves.cards[i].guess) $flipCard.addClass("reversed");
                let $front = $("<div>", { class: "front" }).appendTo($flipCard);
                $("<div>", { class: "word-upside", text: cards[i].word.toUpperCase() }).appendTo($front);
                $("<div>", { class: "word", text: cards[i].word.toUpperCase() }).appendTo($front);
                if (isSpymaster) {
                    $("<div>", { class: "type" }).appendTo($front);
                }
                let $back = $("<div>", { class: "back" }).appendTo($flipCard);
            }
            $gameWrapper.appendTo($main);
            $gameWrapper.animate({ opacity: 1 }, 800);
        } 
        else if (response.leave) {
            console.log("Leaving game " + response.leave);
        } 
        else if (response.message) {
            console.log("chat message")
            /*var msgdiv = $("#room-" + data.room + " .messages");
            var ok_msg = "";
            // msg types are defined in chat/settings.py
            // Only for demo purposes is hardcoded, in production scenarios, consider call a service.
            switch (data.msg_type) {
                case 0:
                    // Message
                    ok_msg = "<div class='message'>" +
                            "<span class='username'>" + data.username + "</span>" +
                            "<span class='body'>" + data.message + "</span>" +
                            "</div>";
                    break;
                case 1:
                    // Warning / Advice messages
                    ok_msg = "<div class='contextual-message text-warning'>" + data.message +
                            "</div>";
                    break;
                case 2:
                    // Alert / Danger messages
                    ok_msg = "<div class='contextual-message text-danger'>" + data.message +
                            "</div>";
                    break;
                case 3:
                    // "Muted" messages
                    ok_msg = "<div class='contextual-message text-muted'>" + data.message +
                            "</div>";
                    break;
                case 4:
                    // User joined room
                    ok_msg = "<div class='contextual-message text-muted'>" + data.username +
                            " joined the room!" +
                            "</div>";
                    break;
                case 5:
                    // User left room
                    ok_msg = "<div class='contextual-message text-muted'>" + data.username +
                            " left the room!" +
                            "</div>";
                    break;
                default:
                    console.log("Unsupported message type!");
                    return;
            }
            msgdiv.append(ok_msg);
            msgdiv.scrollTop(msgdiv.prop("scrollHeight")); */
        } else {
            console.log("Cannot handle message!");
        }
    };
    // Says if we joined a room or not by if there's a div for it
    let inRoom = function(room) {
        return $("#room-" + roomId).length > 0;
    };

    /* Room join/leave
    $("li.room-link").click(function () {
        roomId = $(this).attr("data-room-id");
        if (inRoom(roomId)) {
            // Leave room
            $(this).removeClass("joined");
            socket.send(JSON.stringify({
                "command": "leave",
                "room": roomId
            }));
        } else {
            // Join room
            $(this).addClass("joined");
            socket.send(JSON.stringify({
                "command": "join",
                "room": roomId
            }));
        }
    }*/
    // Helpful debugging
    socket.onopen = function () {
        console.log("Connected to game socket");
        socket.send(JSON.stringify({
            "command": "join",
            "game": game.id
        }));
    };
    socket.onclose = function () {
        console.log("Disconnected from game socket");
    }

    $(document).on('contextmenu', '.card', function(e) {
        let $flipCard = $(this).children();
        let toggle = $flipCard.hasClass('reversed') ? true : false;
        if (toggle) {
            $flipCard.removeClass('reversed').addClass('normal');
        }
        else {
            $flipCard.removeClass('normal').addClass('reversed');
        }

        e.preventDefault();
    })

    let Error = {
        display(err) {
            $('.loading').addClass('fail');
            $('.loading .icon span').text("Error");
            $('.loading .message').prepend($("<div>", { class: "icon-warning" }))
            $('.loading .message span').text(err);            
        }
    }

    let Game = {
        Cards: {
            getTypeAsClass(type) {
                let rand = Math.round(Math.random()) + 1;
                switch(type) {
                    case "team-orange": case "team-purple": case "bystander": return type + "-" + rand;
                    default: return type;
                }
            }
        },
        Spymaster: {
            isSpymaster(game, user) {
                return (game.spymaster["team-orange"].player === user || game.spymaster["team-purple"].player === user)
            }
        }
    }
});