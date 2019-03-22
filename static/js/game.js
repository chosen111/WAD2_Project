$(document).ready(function() {
  let path = window.location.pathname.split('/');
  let game = {
    id: path[path.indexOf('game') + 1]
  }

  //Pusher.logToConsole = true;
  let pusher = new Pusher('f7e0c5de422f69bb8d14', {
    cluster: 'eu',
    forceTLS: true
  });

  let gameChannel = pusher.subscribe(`game=${game.id}`);
  const vcButton = Vue.component('vc-button', {
    props: [ 'id', 'text', 'fn' ],
    template: `
      <div class="button" :class="id" @click="fn">
        <span class="text"><slot></slot></span>
      </div>`
  })
  
  new Vue({
    delimiters: ['[[', ']]'],
    components: {
      'vc-button': vcButton
    },
    el: '.vue-game',
    data: {
      player: {},
      game: {
        data: {},
        players: [],
        cards: {},
      },
      cards: [],
      loading: {
        status: true,
        message: "Searching for game",
        error: false
      },
      notifications: [],
      //
      clue: {
        word: "",
        num: 0
      },
      display: {
        board: true,
      }
    },
    async mounted() {
      try {
        let result = await $.post({
            headers: { "X-CSRFToken": csrf_token },
            url: '/codenamez/connectgame/',
            data: game
        })

        if (result.error) {
          this.loading.error = true;
          this.loading.message = LANG.get(result.error);
        }
        // Update board
        this.updateBoard(result.game);
        this.updatePlayers(result.players);
        // Update self
        this.updatePlayer(result.player);

        this.loading.status = false;
        this.gameNotification(undefined, `Welcome to ${this.game.data.name} game room!`);
        this.startRound(result.game.current_round);
      }
      catch(e) {
        console.error(e);
      }

      gameChannel.bind('game_started', (data) => {
        // Update board
        this.updateBoard(data.game);
        this.updatePlayers(data.players);
        // Update self
        for(let i in data.players) {
          if(data.players[i].user.id == this.player.user.id) {
            this.updatePlayer(data.players[i]);
            break;
          }
        }
        this.gameNotification(undefined, `Game has now started!`);
        this.startRound(data.game.current_round);
      })

      gameChannel.bind('game_cancelled', (data) => {
        // Update board
        this.updateBoard(data.game);

        this.loading.status = true
        this.loading.error = true;
        this.loading.message = LANG.get("E_GAME_CANCELLED");
      })

      gameChannel.bind('game_round_end', (data) => {
        this.updateBoard(data.game);        
        this.startRound();
      })

      gameChannel.bind('player_switched_team', (data) => {
        for(let i in this.game.players) {
          if(this.game.players[i].user.id == data.player.user.id) {
            this.game.players.splice(i, 1, data.player);

            this.gameNotification(this.getTeamColor(data.player.team), `Player ${data.player.user.username} (${data.player.user.profile.ranking}) has switched to ${this.getTeamName(data.player.team)}`);
            break;
          }
        }
      })

      gameChannel.bind('player_locked_in', (data) => {
        if (data.clue) {
          let clue = JSON.parse(data.clue);
          this.$set(this.game.data, 'current_clue', clue);
          this.gameNotification(this.getTeamColor(data.player.team), `Spymaster ${data.player.user.username} (${data.player.user.profile.ranking}) has revealed the clue as: ${clue.word.toLowerCase()} (${clue.num})`);
        }
        if (data.selected) {
          let selected = JSON.parse(data.selected);
          this.gameNotification(this.getTeamColor(data.player.team), `Player ${data.player.user.username} (${data.player.user.profile.ranking}) has locked in the cards ${this.formatSelectedCards(selected)}`);
        }
      })

      gameChannel.bind('player_joined_game', (data) => {
        let flag = false;
        for(let i in this.game.players) {
          if(this.game.players[i].user.id == data.player.user.id) {
            flag = true;
            break;
          }
        }
        if(!flag) {
          self.gameNotification("#a68e42", `Player ${data.player.user.username} (${data.player.user.profile.ranking}) has joined the game`);
          self.game.players.push(data.player);
        }
      });

      gameChannel.bind('player_left_game', (data) => {
        for(let i in this.game.players) {
          if(this.game.players[i].user.id == data.player.user.id) {
            self.gameNotification("#a68e42", `Player ${data.player.user.username} (${data.player.user.profile.ranking}) has left the game`);
            self.game.players.splice(i, 1);
          }
        }
      });
    },
    computed: {
      lockTurnCondition() {
        return !this.game.data.ended && (this.game.data.current_team == this.player.team && ((this.player.is_spymaster && !this.game.data.current_clue.word) || (!this.player.is_spymaster && this.game.data.current_clue.word)));
      },
      gameHeader() {
        if (this.game.data.ended) {
          return `Game Over! ${this.game.data.name}`;
        }
        else if (this.game.data.started) {
          return `Turn ${this.game.data.current_round}: ${this.game.data.name}`;
        }
        else {
          return `Preparing: ${this.game.data.name}`;
        }
      },
      gameStatus() {
        return (this.game.data.ended) ? "GAME ENDED" : (!this.game.data.started) ? "PREPARING" : "IN PROGRESS";
      },
      gameStatusSlug() {
        return (this.game.data.ended) ? "ended" : (!this.game.data.started) ? "preparing" : "in-progress";
      },
      teamOrange() {
        return this.game.players.filter((p) => { return p.team == 1 });
      },
      teamPurple() {
        return this.game.players.filter((p) => { return p.team == 2 });
      },
      teamNeutral() {
        return this.game.players.filter((p) => { return p.team == 0 });
      },
    },
    methods: {
      async asyncAjax(url, method, data) {
        try {
          let result = await $.ajax({
            headers: { "X-CSRFToken": csrf_token },
            url, method, data
          })
          if (result.error) {
            throw new Error(LANG.get(result.error));
          }
          return result;
        }
        catch(e) {
          throw e.message || e.statusText;
        }
      },
      gameNotification(color, message, spacing) {
        let date = new Date();
        let dateString = `[${date.getFullYear()}/${(date.getMonth()+1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')} \
                           ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}]`

        this.notifications.unshift(Object.assign({}, { 
          date: dateString,
          color: color || "inherit",
          message,
          spacing
        }))
      },
      getTeamColor(team) {
        return (team == 1) ? "#ff6600" : "#660066";
      },
      getTeamName(team) {
        if (team == 1) return "Orange Team";
        else if (team == 2) return "Purple Team";
        else return "Neutral Team";
      },
      getTeamSlug(team) {
        if (team == 1) return "team-orange";
        else if (team == 2) return "team-purple";
        else return "default";
      },
      getTypeSlug(type) {
        let rand = Math.round(Math.random()) + 1;
        if (type == 0) return `assassin`;
        if (type == 1) return `team-orange-${rand}`;
        if (type == 2) return `team-purple-${rand}`;
        if (type == 5) return `bystander-${rand}`;
        else return `default`;
      },
      evFlipCard(id) {
        this.$set(this.cards[id], 'reversed', !this.cards[id].reversed);
      },
      evSelectCard(id) {
        if (this.player.locked_in || this.player.is_spymaster) return;
        this.$set(this.cards[id], 'selected', !this.cards[id].selected);
      },
      formatSelectedCards(cards) {
        return `[${cards.map((c) => this.game.cards[c].word).join(', ')}]`;
      },
      getSelectedCards() {
        let selected = [];
        for(let i = 0; i < this.cards.length; i++) {
          if (this.cards[i].selected) {
            selected.push(i);
          }
        }
        return (selected.length) ? selected : null;
      },
      startRound(turn) {
        if (!this.game.data.started) return;
        if (this.game.data.ended) {
          this.display.board = false;
          return this.gameNotification(this.getTeamColor(this.game.data.winner), `The ${this.getTeamName(this.game.data.winner)} has won the game!`, true);
        }
        this.gameNotification(this.getTeamColor(this.game.data.current_team), `Turn ${this.game.data.current_round}: Is ${this.getTeamName(this.game.data.current_team)}'s turn!`, true);
        if (turn == 1) {
          if (this.player.is_spymaster) {
            this.gameNotification(this.getTeamColor(this.player.team), `You are the spymaster for the ${this.getTeamName(this.player.team)}!`);
          }
        }
        if (this.game.data.current_clue.word) {
          this.gameNotification(this.getTeamColor(this.game.data.current_team), `The ${this.getTeamName(this.game.data.current_team)} has revealed the current clue as: ${this.game.data.current_clue.word.toLowerCase()} (${this.game.data.current_clue.num})`);
        }
      },
      toggleBoard() {
        this.display.board = !this.display.board;
      },
      async lockTurn() {
        try {
          let response = await this.asyncAjax('/codenamez/lockturn/', "POST", {
            gameId: this.game.data.id,
            clue: (this.player.is_spymaster) ? JSON.stringify(this.clue) : null,
            selected: JSON.stringify(this.getSelectedCards()),
          })
          this.updatePlayer(response.player)
        }
        catch(e) {
          this.gameNotification('#ff6347', e);
        }
      },
      async switchTeam(team) {
        try {
          let response = await this.asyncAjax('/codenamez/switchteam/', "POST", {
            gameId: this.game.data.id,
            team
          })
          this.updatePlayer(response.player)
        }
        catch(e) {
          this.gameNotification('#ff6347', e);
        }
      },
      async startGame() {
        try {
          let response = await this.asyncAjax('/codenamez/startgame/', "POST", {
            gameId: this.game.data.id,
          })
        }
        catch(e) {
          this.gameNotification('#ff6347', e);
        }
      },
      async cancelGame() {
        try {
          let response = await this.asyncAjax('/codenamez/cancelgame/', "POST", {
            gameId: this.game.data.id,
          })
        }
        catch(e) {
          this.gameNotification('#ff6347', e);
        }
      },
      updatePlayer(player) {
        this.player = player;
      },
      updateBoard(game) {
        this.$set(this.game, 'data', game);
        this.$set(this.game, 'cards', JSON.parse(game.cards));
        this.$set(this.game.data, 'current_clue', JSON.parse(game.current_clue));
      },
      updatePlayers(players) {
        this.game.players = players;
      },
      initVueCards(game) {
        cards = JSON.parse(game.cards);
        for(const [i, card] of cards.entries()) {
          this.setVueCards(i, card);
        }
      },
      setVueCards(id, card) {
        this.cards.splice(id, 1, {
          reversed: (card.guess) ? true : false,
          selected: false,
          face: (card.guess || this.player.is_spymaster) ? this.getTypeSlug(card.type) : null,
          guess: (card.guess) ? `guess-${this.getTeamSlug(card.guess)}` : null
        })
      },
    },
    watch: {
      'game.cards': function(newVal, oldVal) {
        if (!newVal.length) return;

        if (oldVal.length) {
          for (let i = 0; i < newVal.length; i++) {
            if (!_.isEqual(newVal[i], oldVal[i])) {
              this.setVueCards(i, newVal[i]);
            }
          }
        }
        else {
          this.initVueCards(this.game.data);
        }
      }
    }
  })
  $(".vue-game").css({ display: "flex" });
})