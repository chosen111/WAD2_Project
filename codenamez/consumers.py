from codenamez.game import GameError
from codenamez.models import UserProfile, Chat, PrivateMessage, Game, GameList

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from django.core import serializers

import json, uuid

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
        except GameError as e:
            await self.send_json({ 'error', e.code })

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        if self.game:
            await self.leave_game(self.game)

    @database_sync_to_async
    def get_game(self, game_id):
        try:
            game = Game.objects.get(id=uuid.UUID(game_id))
            playing = GameList.objects.get(game=game, user=self.scope['user'])
            players = GameList.objects.filter(game=game)            
            response = {
                'game': serializers.serialize('json', [game]),
                'players': serializers.serialize('json', players),
            }

        except (Game.DoesNotExist, ValueError):
            raise GameError("GAME_IS_INVALID")
            #response['error'] = "The game you are trying to access does not exist!"
        except GameList.DoesNotExist:
            raise GameError("GAME_NOT_INVITED")
            #response['error'] = "You are not currently invited to play in " + game.name
        return response
       
    async def join_game(self, game_id):
        """
        Called by receive_json when someone sent a join command.
        """
        response = {
            'join': await self.get_game(game_id)
        }

        # Send a join message
        await self.channel_layer.group_send(game_id,
            {
                "type": "game.join",
                "game": game_id,
                "username": self.scope["user"].username,
            }
        )
        self.game = game_id
        await self.channel_layer.group_add(
            game_id,
            self.channel_name,
        )
        await self.send_json(response)

    async def leave_game(self, gameId):
        """
        Called by receive_json when someone sent a leave command.
        """
        game = Game.objects.get(game=uuid.UUID(gameId))
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
                "game": event["gameId"],
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
                "game": event["gameId"],
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
                "game": event["gameId"],
                "username": event["username"],
                "message": event["message"],
                "team": event["team"],
            },
        )