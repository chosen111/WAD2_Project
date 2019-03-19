$.fn.extend({
    replaceOrAdd($replace, $append) {
        if ($(this).length) {
            $(this).replaceWith($replace); 
        }
        else {
            $append.append($replace);
        }      
    }
})

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
        var response = JSON.parse(response.data);
        // Handle errors
        if (response.error) {
            return Error.display(response.error);
        }
        // Handle responses
        if (response.join) {
            Game.create(response.join);
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
    socket.onopen = function () {
        // If connection to game server is successful, ask the server to join the game
        socket.send(JSON.stringify({ "command": "join", "game": game.id }))
    }
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
            $('.loading .message span').text(LANG.get(err));            
        }
    }

    let Game = {
        create(data) {
            console.log(data);
            let user = data.user;
            let game = JSON.parse(data.game)[0].fields;
            let players = JSON.parse(data.players);
            console.log(user);
            console.log(game);
            console.log(players);


            let $game = $("<div>", { class: "game-wrapper" });
            let $colLeft = $("<section>", { class: "col-1" }).appendTo($game);
            let $colMiddle = $("<section>", { class: "col-2" }).appendTo($game);
            // Middle :: Game Info
            var $gameInfo = $("<div>", { class: "game-info" }).appendTo($colMiddle);
            $("<span>", { class: "name", text: data.game.name }).appendTo($gameInfo);

            //Game.Board.create($colMiddle, data);
            let $colRight = $("<section>", { class: "col-3" }).appendTo($game);

            // -- left column -- //
            var $gameInfo = $("<div>", { class: "panel game-info" }).appendTo($colLeft);
            $("<label>", { class: "title", text: "Game Info" }).appendTo($gameInfo);
            let $gameChat = $("<div>", { class: "panel game-chat" }).appendTo($colLeft);
            $("<label>", { class: "title", text: "Game Chat" }).appendTo($gameChat);
            Game.show($game);
        },
        show($game) {
            let $main = $("main").empty();
            $game.appendTo($main);
            $game.animate({ opacity: 1 }, 800);
        },
        Board: {
            create($el, data) {
                let $board = $("<ul>", { class: "board" });
                
                let game = JSON.parse(data.game);
                let players = JSON.parse(data.players);
                
                let gameData = JSON.parse(game[0].fields.data);
                let cards = gameData.cards;
                let moves = gameData.moves[gameData.moves.length-1];
                let isSpymaster = Game.Spymaster.isSpymaster(gameData, data.user);
                for (let i in cards) {
                    let $card = $("<li>", { class: "card" }).appendTo($board);
                    let $flipCard = $("<div>", { class: "flip-card" }).appendTo($card);
                    let $front = $("<div>", { class: "front" }).appendTo($flipCard);
                    $("<div>", { class: "word-upside", text: cards[i].word.toUpperCase() }).appendTo($front);
                    $("<div>", { class: "word", text: cards[i].word.toUpperCase() }).appendTo($front);                    
                    let $back = $("<div>", { class: "back" }).appendTo($flipCard);

                    if (moves.cards[i].guess) {
                        $card.addClass(Game.Cards.getTypeAsClass(cards[i].type))
                        $flipCard.addClass("reversed").addClass(`guess-${moves.cards[i].guess}`)
                    }

                    if (isSpymaster) {
                        $card.addClass(Game.Cards.getTypeAsClass(cards[i].type))
                        $("<div>", { class: "type" }).appendTo($front);
                    }
                }
                $el.children('.board').replaceOrAdd($board, $el)          
            }
        },
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