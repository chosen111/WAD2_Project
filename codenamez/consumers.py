### This file is used with channels, disabled for this project
import json, uuid, time

import codenamez.game as gameUtil
from codenamez.models import UserProfile, Chat, PrivateMessage, Game, GamePlayer

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from django.core import serializers

class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.accept()
        self.game = None

    async def receive_json(self, data):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        try:
            command = data.get("command", None)
            if command == "join":
                await self.join_game(data["game"])
            elif command == "leave":
                await self.leave_game(data["game"])
            elif command == "send":
                await self.chat(data["game"], data["message"], data["team"])
        except gameUtil.Error as e:
            await self.send_json({"error": e.code })

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        if self.game:
            await self.leave_game(self.game)

    @database_sync_to_async
    def get_game(self, game_id):
        # Check if the player is in an active game thats different from the current one
        alreadyPlaying = gameUtil.isPlaying(self.scope['user'])
        if alreadyPlaying is not False and alreadyPlaying['id'] != game_id:
            raise gameUtil.Error("E_ALREADY_PLAYING")
        else:
            # Player is not in any game, try to join the game
            try: 
                game = Game.objects.get(id=uuid.UUID(game_id))
                players = GamePlayer.objects.filter(game=game)
                playing = GamePlayer.objects.get(game=game, player=self.scope['user'])  
            # The game is invalid or the value found in url is invalid
            except (Game.DoesNotExist, ValueError):
                raise game.Error("E_GAME_NOT_FOUND")
            # The user is not a player of this game yet... checking if allowed to participate
            except GamePlayer.DoesNotExist:    
                if game.started != None:
                    raise gameUtil.Error("E_GAME_STARTED")
                if len(players) >= game.max_players:
                    raise gameUtil.Error("E_GAME_FULL")

                # Add player to the game
                player = GamePlayer(game=game, player=self.scope['user'], joined=time.time())
                player.save()
            finally:
                response = {
                    'user': self.scope['user'].username,
                    'game': serializers.serialize('json', [game]),
                    'players': serializers.serialize('json', players),
                }   
        return response
       
    async def join_game(self, game_id):
        """
        Called by receive_json when someone sent a join command.
        """
        game = await self.get_game(game_id)
        response = {
            'join': game
        }

        # Send a join message
        await self.channel_layer.group_send(game_id,
            {
                "type": "game.join",
                "game": game,
                "player": self.scope["user"],
            }
        )
        
        self.game = game_id
        await self.channel_layer.group_add(
            game_id,
            self.channel_name,
        )
        await self.send_json(response)

    @database_sync_to_async
    async def leave_game(self, game_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        game = Game.objects.get(id=uuid.UUID(game_id))
        await self.channel_layer.group_send(
            game.id,
            {
                "type": "game.leave",
                "game": game.id,
                "username": self.scope["user"].username,
            }
        )
        self.game = None
        await self.channel_layer.group_discard(
            game.id,
            self.channel_name,
        )
        await self.send_json({
            "leave": game.id,
        })

    async def send_room(self, gameId, message, team):
        """
        Called by receive_json when someone sends a message to a room.
        """
        if gameId != self.game:
            print("access denied")
    
        await self.channel_layer.group_send(
            gameId,
            {
                "type": "game.message",
                "game": gameId,
                "username": self.scope["user"].username,
                "message": message,
                "team": team
            }
        )

    # These helper methods are named by the types we send - so game.join becomes game_join
    async def game_join(self, event):
        """
        Called when someone has joined our chat.
        """
        await self.send_json(
            {
                "game": event["game"],
                "username": event["username"],
            },
        )

    async def game_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "game": event["game"],
                "username": event["username"],
            },
        )

    async def game_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "game": event["game"],
                "username": event["username"],
                "message": event["message"],
                "team": event["team"],
            },
        )